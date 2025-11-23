package com.notulen.domain.usecase

import com.notulen.domain.model.Meeting
import com.notulen.domain.model.Result
import com.notulen.domain.repository.MeetingRepository
import kotlinx.coroutines.flow.Flow
import javax.inject.Inject

class GetMeetingsUseCase @Inject constructor(
    private val repository: MeetingRepository
) {
    operator fun invoke(): Flow<Result<List<Meeting>>> {
        return repository.getAllMeetings()
    }
}
