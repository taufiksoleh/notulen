package com.notulen.data.remote.dto

import com.google.gson.annotations.SerializedName
import com.notulen.domain.model.TranscriptionResult
import com.notulen.domain.model.TranscriptionSegment

data class TranscriptionDto(
    @SerializedName("text")
    val text: String,
    @SerializedName("segments")
    val segments: List<SegmentDto>?,
    @SerializedName("language")
    val language: String?,
    @SerializedName("duration")
    val duration: Float
)

data class SegmentDto(
    @SerializedName("id")
    val id: Int,
    @SerializedName("start")
    val start: Float,
    @SerializedName("end")
    val end: Float,
    @SerializedName("text")
    val text: String
)

fun TranscriptionDto.toDomain(): TranscriptionResult {
    return TranscriptionResult(
        text = text,
        segments = segments?.map { it.toDomain() } ?: emptyList(),
        language = language,
        duration = duration
    )
}

fun SegmentDto.toDomain(): TranscriptionSegment {
    return TranscriptionSegment(
        id = id,
        start = start,
        end = end,
        text = text
    )
}
