package com.notulen.domain.usecase

import com.notulen.domain.model.Meeting
import com.notulen.domain.model.Result
import com.notulen.domain.repository.MeetingRepository
import javax.inject.Inject

class GetMeetingDetailsUseCase @Inject constructor(
    private val repository: MeetingRepository
) {
    suspend operator fun invoke(meetingId: String): Result<Meeting> {
        return repository.getMeetingById(meetingId)
    }
}
