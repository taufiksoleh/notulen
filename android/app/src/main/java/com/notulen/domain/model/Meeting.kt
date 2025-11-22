package com.notulen.domain.model

import java.util.Date

data class Meeting(
    val id: String,
    val title: String,
    val transcription: String,
    val summary: String?,
    val actionItems: List<String>,
    val keyPoints: List<String>,
    val audioPath: String?,
    val duration: Long,
    val createdAt: Date,
    val updatedAt: Date,
    val status: MeetingStatus
)

enum class MeetingStatus {
    RECORDING,
    PROCESSING,
    TRANSCRIBING,
    SUMMARIZING,
    COMPLETED,
    FAILED
}
