package com.notulen.domain.usecase

import com.notulen.domain.model.Result
import com.notulen.domain.repository.MeetingRepository
import javax.inject.Inject

class DeleteMeetingUseCase @Inject constructor(
    private val repository: MeetingRepository
) {
    suspend operator fun invoke(meetingId: String): Result<Unit> {
        return repository.deleteMeeting(meetingId)
    }
}
