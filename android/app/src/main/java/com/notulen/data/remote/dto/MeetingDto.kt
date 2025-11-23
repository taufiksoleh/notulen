package com.notulen.data.remote.dto

import com.google.gson.annotations.SerializedName
import com.notulen.domain.model.Meeting
import com.notulen.domain.model.MeetingStatus
import java.util.Date

data class MeetingDto(
    @SerializedName("id")
    val id: String,
    @SerializedName("title")
    val title: String,
    @SerializedName("transcription")
    val transcription: String,
    @SerializedName("summary")
    val summary: String?,
    @SerializedName("action_items")
    val actionItems: List<String>?,
    @SerializedName("key_points")
    val keyPoints: List<String>?,
    @SerializedName("audio_path")
    val audioPath: String?,
    @SerializedName("duration")
    val duration: Long,
    @SerializedName("created_at")
    val createdAt: String,
    @SerializedName("updated_at")
    val updatedAt: String,
    @SerializedName("status")
    val status: String
)

fun MeetingDto.toDomain(): Meeting {
    return Meeting(
        id = id,
        title = title,
        transcription = transcription,
        summary = summary,
        actionItems = actionItems ?: emptyList(),
        keyPoints = keyPoints ?: emptyList(),
        audioPath = audioPath,
        duration = duration,
        createdAt = parseDate(createdAt),
        updatedAt = parseDate(updatedAt),
        status = parseStatus(status)
    )
}

private fun parseDate(dateString: String): Date {
    return try {
        Date(dateString)
    } catch (e: Exception) {
        Date()
    }
}

private fun parseStatus(status: String): MeetingStatus {
    return when (status.lowercase()) {
        "recording" -> MeetingStatus.RECORDING
        "processing" -> MeetingStatus.PROCESSING
        "transcribing" -> MeetingStatus.TRANSCRIBING
        "summarizing" -> MeetingStatus.SUMMARIZING
        "completed" -> MeetingStatus.COMPLETED
        "failed" -> MeetingStatus.FAILED
        else -> MeetingStatus.PROCESSING
    }
}
