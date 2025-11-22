package com.notulen.domain.usecase

import com.notulen.domain.model.Meeting
import com.notulen.domain.model.Result
import com.notulen.domain.repository.MeetingRepository
import java.io.File
import javax.inject.Inject

class CreateMeetingUseCase @Inject constructor(
    private val repository: MeetingRepository
) {
    suspend operator fun invoke(title: String, audioFile: File): Result<Meeting> {
        return repository.createMeeting(title, audioFile)
    }
}
