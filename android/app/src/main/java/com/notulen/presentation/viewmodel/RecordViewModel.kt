package com.notulen.presentation.viewmodel

import android.content.Context
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.notulen.domain.model.Result
import com.notulen.domain.usecase.CreateMeetingUseCase
import com.notulen.domain.usecase.RecordAudioUseCase
import dagger.hilt.android.lifecycle.HiltViewModel
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.launch
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import javax.inject.Inject

@HiltViewModel
class RecordViewModel @Inject constructor(
    private val recordAudioUseCase: RecordAudioUseCase,
    private val createMeetingUseCase: CreateMeetingUseCase,
    @ApplicationContext private val context: Context
) : ViewModel() {

    private val _isRecording = MutableStateFlow(false)
    val isRecording: StateFlow<Boolean> = _isRecording.asStateFlow()

    private val _recordingDuration = MutableStateFlow(0L)
    val recordingDuration: StateFlow<Long> = _recordingDuration.asStateFlow()

    private val _hasPermission = MutableStateFlow(false)
    val hasPermission: StateFlow<Boolean> = _hasPermission.asStateFlow()

    private val _recordingState = MutableStateFlow<RecordingState>(RecordingState.Idle)
    val recordingState: StateFlow<RecordingState> = _recordingState.asStateFlow()

    private var currentRecordingFile: File? = null

    init {
        checkPermission()
        observeRecordingState()
    }

    private fun checkPermission() {
        viewModelScope.launch {
            _hasPermission.value = recordAudioUseCase.hasPermission()
        }
    }

    private fun observeRecordingState() {
        recordAudioUseCase.isRecording()
            .onEach { _isRecording.value = it }
            .launchIn(viewModelScope)

        recordAudioUseCase.getRecordingDuration()
            .onEach { _recordingDuration.value = it }
            .launchIn(viewModelScope)
    }

    fun startRecording() {
        viewModelScope.launch {
            val timestamp = SimpleDateFormat("yyyyMMdd_HHmmss", Locale.getDefault()).format(Date())
            val fileName = "recording_$timestamp.m4a"
            val recordingFile = File(context.filesDir, fileName)
            currentRecordingFile = recordingFile

            when (recordAudioUseCase.startRecording(recordingFile)) {
                is Result.Success -> {
                    _recordingState.value = RecordingState.Recording
                }
                is Result.Error -> {
                    _recordingState.value = RecordingState.Error("Failed to start recording")
                }
                else -> {}
            }
        }
    }

    fun stopRecording() {
        viewModelScope.launch {
            _recordingState.value = RecordingState.Saving

            when (val result = recordAudioUseCase.stopRecording()) {
                is Result.Success -> {
                    val audioFile = result.data
                    createMeeting(audioFile)
                }
                is Result.Error -> {
                    _recordingState.value = RecordingState.Error("Failed to stop recording")
                }
                else -> {}
            }
        }
    }

    private suspend fun createMeeting(audioFile: File) {
        val timestamp = SimpleDateFormat("MMM dd, yyyy HH:mm", Locale.getDefault()).format(Date())
        val title = "Meeting $timestamp"

        when (createMeetingUseCase(title, audioFile)) {
            is Result.Success -> {
                _recordingState.value = RecordingState.Saved
            }
            is Result.Error -> {
                _recordingState.value = RecordingState.Error("Failed to save meeting")
            }
            else -> {}
        }
    }

    fun resetState() {
        _recordingState.value = RecordingState.Idle
        _recordingDuration.value = 0L
    }

    fun updatePermission(granted: Boolean) {
        _hasPermission.value = granted
    }
}

sealed class RecordingState {
    object Idle : RecordingState()
    object Recording : RecordingState()
    object Saving : RecordingState()
    object Saved : RecordingState()
    data class Error(val message: String) : RecordingState()
}
