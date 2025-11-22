package com.notulen.presentation.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.notulen.domain.model.Meeting
import com.notulen.domain.model.Result
import com.notulen.domain.usecase.DeleteMeetingUseCase
import com.notulen.domain.usecase.GetMeetingsUseCase
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class MeetingsViewModel @Inject constructor(
    private val getMeetingsUseCase: GetMeetingsUseCase,
    private val deleteMeetingUseCase: DeleteMeetingUseCase
) : ViewModel() {

    private val _uiState = MutableStateFlow<MeetingsUiState>(MeetingsUiState.Loading)
    val uiState: StateFlow<MeetingsUiState> = _uiState.asStateFlow()

    init {
        loadMeetings()
    }

    fun loadMeetings() {
        getMeetingsUseCase()
            .onEach { result ->
                _uiState.value = when (result) {
                    is Result.Success -> {
                        if (result.data.isEmpty()) {
                            MeetingsUiState.Empty
                        } else {
                            MeetingsUiState.Success(result.data)
                        }
                    }
                    is Result.Error -> MeetingsUiState.Error(result.message ?: "Unknown error")
                    is Result.Loading -> MeetingsUiState.Loading
                }
            }
            .launchIn(viewModelScope)
    }

    fun deleteMeeting(meetingId: String) {
        viewModelScope.launch {
            when (deleteMeetingUseCase(meetingId)) {
                is Result.Success -> {
                    // Meeting will be automatically removed from the list via Flow
                }
                is Result.Error -> {
                    // Handle error if needed
                }
                else -> {}
            }
        }
    }
}

sealed class MeetingsUiState {
    object Loading : MeetingsUiState()
    object Empty : MeetingsUiState()
    data class Success(val meetings: List<Meeting>) : MeetingsUiState()
    data class Error(val message: String) : MeetingsUiState()
}
