package com.notulen.data.repository

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.media.MediaRecorder
import android.os.Build
import androidx.core.content.ContextCompat
import com.notulen.domain.model.Result
import com.notulen.domain.repository.AudioRepository
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import timber.log.Timber
import java.io.File
import javax.inject.Inject

class AudioRepositoryImpl @Inject constructor(
    @ApplicationContext private val context: Context
) : AudioRepository {

    private var mediaRecorder: MediaRecorder? = null
    private var recordingFile: File? = null
    private var startTime: Long = 0

    private val _isRecording = MutableStateFlow(false)
    private val _recordingDuration = MutableStateFlow(0L)

    override suspend fun startRecording(outputFile: File): Result<Unit> {
        return try {
            if (!hasRecordingPermission()) {
                return Result.Error(Exception("Recording permission not granted"))
            }

            recordingFile = outputFile

            mediaRecorder = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                MediaRecorder(context)
            } else {
                @Suppress("DEPRECATION")
                MediaRecorder()
            }.apply {
                setAudioSource(MediaRecorder.AudioSource.MIC)
                setOutputFormat(MediaRecorder.OutputFormat.MPEG_4)
                setAudioEncoder(MediaRecorder.AudioEncoder.AAC)
                setAudioEncodingBitRate(128000)
                setAudioSamplingRate(44100)
                setOutputFile(outputFile.absolutePath)

                prepare()
                start()
            }

            startTime = System.currentTimeMillis()
            _isRecording.value = true

            // Start duration tracking
            trackDuration()

            Timber.d("Recording started: ${outputFile.absolutePath}")
            Result.Success(Unit)
        } catch (e: Exception) {
            Timber.e(e, "Error starting recording")
            Result.Error(e, "Failed to start recording")
        }
    }

    override suspend fun stopRecording(): Result<File> {
        return try {
            mediaRecorder?.apply {
                stop()
                release()
            }
            mediaRecorder = null
            _isRecording.value = false
            _recordingDuration.value = 0

            val file = recordingFile ?: return Result.Error(Exception("No recording file"))
            Timber.d("Recording stopped: ${file.absolutePath}")

            Result.Success(file)
        } catch (e: Exception) {
            Timber.e(e, "Error stopping recording")
            Result.Error(e, "Failed to stop recording")
        }
    }

    override fun getRecordingDuration(): Flow<Long> {
        return _recordingDuration.asStateFlow()
    }

    override fun isRecording(): Flow<Boolean> {
        return _isRecording.asStateFlow()
    }

    override suspend fun hasRecordingPermission(): Boolean {
        return ContextCompat.checkSelfPermission(
            context,
            Manifest.permission.RECORD_AUDIO
        ) == PackageManager.PERMISSION_GRANTED
    }

    private suspend fun trackDuration() {
        while (_isRecording.value) {
            val elapsed = System.currentTimeMillis() - startTime
            _recordingDuration.value = elapsed
            delay(100) // Update every 100ms
        }
    }
}
