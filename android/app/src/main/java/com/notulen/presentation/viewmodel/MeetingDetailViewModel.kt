package com.notulen.presentation.viewmodel

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.notulen.domain.model.Meeting
import com.notulen.domain.model.Result
import com.notulen.domain.usecase.GetMeetingDetailsUseCase
import com.notulen.domain.usecase.RequestSummaryUseCase
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class MeetingDetailViewModel @Inject constructor(
    private val getMeetingDetailsUseCase: GetMeetingDetailsUseCase,
    private val requestSummaryUseCase: RequestSummaryUseCase,
    savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val meetingId: String = checkNotNull(savedStateHandle["meetingId"])

    private val _uiState = MutableStateFlow<MeetingDetailUiState>(MeetingDetailUiState.Loading)
    val uiState: StateFlow<MeetingDetailUiState> = _uiState.asStateFlow()

    private val _isSummarizing = MutableStateFlow(false)
    val isSummarizing: StateFlow<Boolean> = _isSummarizing.asStateFlow()

    init {
        loadMeetingDetails()
    }

    fun loadMeetingDetails() {
        viewModelScope.launch {
            _uiState.value = MeetingDetailUiState.Loading

            when (val result = getMeetingDetailsUseCase(meetingId)) {
                is Result.Success -> {
                    _uiState.value = MeetingDetailUiState.Success(result.data)
                }
                is Result.Error -> {
                    _uiState.value = MeetingDetailUiState.Error(
                        result.message ?: "Failed to load meeting"
                    )
                }
                else -> {}
            }
        }
    }

    fun requestSummary() {
        viewModelScope.launch {
            _isSummarizing.value = true

            when (val result = requestSummaryUseCase(meetingId)) {
                is Result.Success -> {
                    _uiState.value = MeetingDetailUiState.Success(result.data)
                }
                is Result.Error -> {
                    // Keep current state but show error
                }
                else -> {}
            }

            _isSummarizing.value = false
        }
    }
}

sealed class MeetingDetailUiState {
    object Loading : MeetingDetailUiState()
    data class Success(val meeting: Meeting) : MeetingDetailUiState()
    data class Error(val message: String) : MeetingDetailUiState()
}
