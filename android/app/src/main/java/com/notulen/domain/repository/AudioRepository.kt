package com.notulen.domain.repository

import com.notulen.domain.model.Result
import kotlinx.coroutines.flow.Flow
import java.io.File

interface AudioRepository {
    /**
     * Start recording audio
     */
    suspend fun startRecording(outputFile: File): Result<Unit>

    /**
     * Stop recording and return the audio file
     */
    suspend fun stopRecording(): Result<File>

    /**
     * Get recording duration in milliseconds
     */
    fun getRecordingDuration(): Flow<Long>

    /**
     * Check if currently recording
     */
    fun isRecording(): Flow<Boolean>

    /**
     * Check if recording permission is granted
     */
    suspend fun hasRecordingPermission(): Boolean
}
