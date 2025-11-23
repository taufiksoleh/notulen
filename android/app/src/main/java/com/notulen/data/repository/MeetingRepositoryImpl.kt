package com.notulen.data.repository

import com.notulen.data.local.dao.MeetingDao
import com.notulen.data.local.entity.toDomain
import com.notulen.data.local.entity.toEntity
import com.notulen.data.remote.api.NotulenApiService
import com.notulen.data.remote.api.SummarizeRequest
import com.notulen.data.remote.dto.toDomain
import com.notulen.domain.model.Meeting
import com.notulen.domain.model.MeetingStatus
import com.notulen.domain.model.Result
import com.notulen.domain.model.TranscriptionResult
import com.notulen.domain.repository.MeetingRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.catch
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.asRequestBody
import okhttp3.RequestBody.Companion.toRequestBody
import timber.log.Timber
import java.io.File
import java.util.Date
import java.util.UUID
import javax.inject.Inject

class MeetingRepositoryImpl @Inject constructor(
    private val apiService: NotulenApiService,
    private val meetingDao: MeetingDao
) : MeetingRepository {

    override fun getAllMeetings(): Flow<Result<List<Meeting>>> {
        return meetingDao.getAllMeetings()
            .map<List<com.notulen.data.local.entity.MeetingEntity>, Result<List<Meeting>>> { entities ->
                Result.Success(entities.map { it.toDomain() })
            }
            .catch { e ->
                Timber.e(e, "Error getting meetings from local database")
                emit(Result.Error(e, "Failed to load meetings") as Result<List<Meeting>>)
            }
    }

    override suspend fun getMeetingById(id: String): Result<Meeting> {
        return try {
            val entity = meetingDao.getMeetingById(id)
            if (entity != null) {
                Result.Success(entity.toDomain())
            } else {
                // Try to fetch from API
                val response = apiService.getMeetingById(id)
                if (response.isSuccessful && response.body() != null) {
                    val meeting = response.body()!!.toDomain()
                    meetingDao.insertMeeting(meeting.toEntity())
                    Result.Success(meeting)
                } else {
                    Result.Error(Exception("Meeting not found"))
                }
            }
        } catch (e: Exception) {
            Timber.e(e, "Error getting meeting by ID")
            Result.Error(e, "Failed to load meeting")
        }
    }

    override suspend fun createMeeting(title: String, audioFile: File): Result<Meeting> {
        return try {
            // Create a temporary meeting in local database
            val tempMeeting = Meeting(
                id = UUID.randomUUID().toString(),
                title = title,
                transcription = "",
                summary = null,
                actionItems = emptyList(),
                keyPoints = emptyList(),
                audioPath = audioFile.absolutePath,
                duration = 0,
                createdAt = Date(),
                updatedAt = Date(),
                status = MeetingStatus.PROCESSING
            )
            meetingDao.insertMeeting(tempMeeting.toEntity())

            // Upload for transcription
            val transcriptionResult = uploadAudioFile(audioFile)

            when (transcriptionResult) {
                is Result.Success -> {
                    val updatedMeeting = tempMeeting.copy(
                        transcription = transcriptionResult.data.text,
                        duration = transcriptionResult.data.duration.toLong(),
                        status = MeetingStatus.TRANSCRIBING
                    )
                    meetingDao.updateMeeting(updatedMeeting.toEntity())
                    Result.Success(updatedMeeting)
                }
                is Result.Error -> {
                    val failedMeeting = tempMeeting.copy(status = MeetingStatus.FAILED)
                    meetingDao.updateMeeting(failedMeeting.toEntity())
                    Result.Error(transcriptionResult.exception, "Transcription failed")
                }
                else -> Result.Error(Exception("Unexpected result"))
            }
        } catch (e: Exception) {
            Timber.e(e, "Error creating meeting")
            Result.Error(e, "Failed to create meeting")
        }
    }

    override suspend fun uploadAudioFile(file: File): Result<TranscriptionResult> {
        return try {
            val requestFile = file.asRequestBody("audio/*".toMediaTypeOrNull())
            val body = MultipartBody.Part.createFormData("file", file.name, requestFile)
            val title = "Meeting ${Date()}".toRequestBody("text/plain".toMediaTypeOrNull())

            val response = apiService.transcribeAudio(body, title)

            if (response.isSuccessful && response.body() != null) {
                Result.Success(response.body()!!.toDomain())
            } else {
                Result.Error(Exception("Transcription failed: ${response.message()}"))
            }
        } catch (e: Exception) {
            Timber.e(e, "Error uploading audio file")
            Result.Error(e, "Failed to upload audio file")
        }
    }

    override suspend fun requestSummary(meetingId: String): Result<Meeting> {
        return try {
            val response = apiService.summarizeMeeting(SummarizeRequest(meetingId))

            if (response.isSuccessful && response.body() != null) {
                val meeting = response.body()!!.toDomain()
                meetingDao.updateMeeting(meeting.toEntity())
                Result.Success(meeting)
            } else {
                Result.Error(Exception("Summary request failed: ${response.message()}"))
            }
        } catch (e: Exception) {
            Timber.e(e, "Error requesting summary")
            Result.Error(e, "Failed to generate summary")
        }
    }

    override suspend fun deleteMeeting(id: String): Result<Unit> {
        return try {
            meetingDao.deleteMeetingById(id)
            // Try to delete from server as well
            try {
                apiService.deleteMeeting(id)
            } catch (e: Exception) {
                Timber.w(e, "Failed to delete from server, but deleted locally")
            }
            Result.Success(Unit)
        } catch (e: Exception) {
            Timber.e(e, "Error deleting meeting")
            Result.Error(e, "Failed to delete meeting")
        }
    }

    override suspend fun syncMeetings(): Result<List<Meeting>> {
        return try {
            val response = apiService.getMeetings()

            if (response.isSuccessful && response.body() != null) {
                val meetings = response.body()!!.map { it.toDomain() }
                meetingDao.insertMeetings(meetings.map { it.toEntity() })
                Result.Success(meetings)
            } else {
                Result.Error(Exception("Sync failed: ${response.message()}"))
            }
        } catch (e: Exception) {
            Timber.e(e, "Error syncing meetings")
            Result.Error(e, "Failed to sync meetings")
        }
    }

    override suspend fun updateMeetingStatus(id: String, status: MeetingStatus): Result<Unit> {
        return try {
            val meeting = meetingDao.getMeetingById(id)
            if (meeting != null) {
                val updatedMeeting = meeting.copy(
                    status = status.name,
                    updatedAt = Date()
                )
                meetingDao.updateMeeting(updatedMeeting)
                Result.Success(Unit)
            } else {
                Result.Error(Exception("Meeting not found"))
            }
        } catch (e: Exception) {
            Timber.e(e, "Error updating meeting status")
            Result.Error(e, "Failed to update status")
        }
    }
}
