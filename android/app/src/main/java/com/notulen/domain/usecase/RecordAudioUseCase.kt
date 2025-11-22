package com.notulen.domain.usecase

import com.notulen.domain.model.Result
import com.notulen.domain.repository.AudioRepository
import kotlinx.coroutines.flow.Flow
import java.io.File
import javax.inject.Inject

class RecordAudioUseCase @Inject constructor(
    private val audioRepository: AudioRepository
) {
    suspend fun startRecording(outputFile: File): Result<Unit> {
        return audioRepository.startRecording(outputFile)
    }

    suspend fun stopRecording(): Result<File> {
        return audioRepository.stopRecording()
    }

    fun getRecordingDuration(): Flow<Long> {
        return audioRepository.getRecordingDuration()
    }

    fun isRecording(): Flow<Boolean> {
        return audioRepository.isRecording()
    }

    suspend fun hasPermission(): Boolean {
        return audioRepository.hasRecordingPermission()
    }
}
