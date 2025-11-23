package com.notulen.domain.model

data class TranscriptionResult(
    val text: String,
    val segments: List<TranscriptionSegment>,
    val language: String?,
    val duration: Float
)

data class TranscriptionSegment(
    val id: Int,
    val start: Float,
    val end: Float,
    val text: String
)
