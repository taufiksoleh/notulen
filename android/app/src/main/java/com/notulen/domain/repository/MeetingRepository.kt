package com.notulen.domain.repository

import com.notulen.domain.model.Meeting
import com.notulen.domain.model.Result
import com.notulen.domain.model.TranscriptionResult
import kotlinx.coroutines.flow.Flow
import java.io.File

interface MeetingRepository {
    /**
     * Get all meetings from local database
     */
    fun getAllMeetings(): Flow<Result<List<Meeting>>>

    /**
     * Get a specific meeting by ID
     */
    suspend fun getMeetingById(id: String): Result<Meeting>

    /**
     * Create a new meeting
     */
    suspend fun createMeeting(title: String, audioFile: File): Result<Meeting>

    /**
     * Upload audio file for transcription
     */
    suspend fun uploadAudioFile(file: File): Result<TranscriptionResult>

    /**
     * Request AI summary for a meeting
     */
    suspend fun requestSummary(meetingId: String): Result<Meeting>

    /**
     * Delete a meeting
     */
    suspend fun deleteMeeting(id: String): Result<Unit>

    /**
     * Sync meetings from server
     */
    suspend fun syncMeetings(): Result<List<Meeting>>

    /**
     * Update meeting status
     */
    suspend fun updateMeetingStatus(id: String, status: com.notulen.domain.model.MeetingStatus): Result<Unit>
}
