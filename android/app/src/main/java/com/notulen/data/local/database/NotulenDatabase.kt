package com.notulen.data.local.database

import androidx.room.Database
import androidx.room.RoomDatabase
import androidx.room.TypeConverters
import com.notulen.data.local.dao.MeetingDao
import com.notulen.data.local.entity.MeetingEntity

@Database(
    entities = [MeetingEntity::class],
    version = 1,
    exportSchema = false
)
@TypeConverters(Converters::class)
abstract class NotulenDatabase : RoomDatabase() {
    abstract fun meetingDao(): MeetingDao

    companion object {
        const val DATABASE_NAME = "notulen_database"
    }
}
