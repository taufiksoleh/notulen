package com.notulen.data.local.dao

import androidx.room.*
import com.notulen.data.local.entity.MeetingEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface MeetingDao {

    @Query("SELECT * FROM meetings ORDER BY created_at DESC")
    fun getAllMeetings(): Flow<List<MeetingEntity>>

    @Query("SELECT * FROM meetings WHERE id = :id")
    suspend fun getMeetingById(id: String): MeetingEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertMeeting(meeting: MeetingEntity)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertMeetings(meetings: List<MeetingEntity>)

    @Update
    suspend fun updateMeeting(meeting: MeetingEntity)

    @Delete
    suspend fun deleteMeeting(meeting: MeetingEntity)

    @Query("DELETE FROM meetings WHERE id = :id")
    suspend fun deleteMeetingById(id: String)

    @Query("DELETE FROM meetings")
    suspend fun deleteAllMeetings()
}
