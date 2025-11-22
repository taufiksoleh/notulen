package com.notulen.data.local.entity

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey
import com.notulen.domain.model.Meeting
import com.notulen.domain.model.MeetingStatus
import java.util.Date

@Entity(tableName = "meetings")
data class MeetingEntity(
    @PrimaryKey
    @ColumnInfo(name = "id")
    val id: String,

    @ColumnInfo(name = "title")
    val title: String,

    @ColumnInfo(name = "transcription")
    val transcription: String,

    @ColumnInfo(name = "summary")
    val summary: String?,

    @ColumnInfo(name = "action_items")
    val actionItems: List<String>,

    @ColumnInfo(name = "key_points")
    val keyPoints: List<String>,

    @ColumnInfo(name = "audio_path")
    val audioPath: String?,

    @ColumnInfo(name = "duration")
    val duration: Long,

    @ColumnInfo(name = "created_at")
    val createdAt: Date,

    @ColumnInfo(name = "updated_at")
    val updatedAt: Date,

    @ColumnInfo(name = "status")
    val status: String
)

fun MeetingEntity.toDomain(): Meeting {
    return Meeting(
        id = id,
        title = title,
        transcription = transcription,
        summary = summary,
        actionItems = actionItems,
        keyPoints = keyPoints,
        audioPath = audioPath,
        duration = duration,
        createdAt = createdAt,
        updatedAt = updatedAt,
        status = MeetingStatus.valueOf(status)
    )
}

fun Meeting.toEntity(): MeetingEntity {
    return MeetingEntity(
        id = id,
        title = title,
        transcription = transcription,
        summary = summary,
        actionItems = actionItems,
        keyPoints = keyPoints,
        audioPath = audioPath,
        duration = duration,
        createdAt = createdAt,
        updatedAt = updatedAt,
        status = status.name
    )
}
