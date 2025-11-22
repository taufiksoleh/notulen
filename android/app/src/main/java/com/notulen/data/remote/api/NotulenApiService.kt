package com.notulen.data.remote.api

import com.notulen.data.remote.dto.MeetingDto
import com.notulen.data.remote.dto.TranscriptionDto
import okhttp3.MultipartBody
import okhttp3.RequestBody
import retrofit2.Response
import retrofit2.http.*

interface NotulenApiService {

    @GET("/api/meetings")
    suspend fun getMeetings(): Response<List<MeetingDto>>

    @GET("/api/meetings/{id}")
    suspend fun getMeetingById(
        @Path("id") id: String
    ): Response<MeetingDto>

    @Multipart
    @POST("/api/transcribe")
    suspend fun transcribeAudio(
        @Part file: MultipartBody.Part,
        @Part("title") title: RequestBody
    ): Response<TranscriptionDto>

    @POST("/api/summarize")
    suspend fun summarizeMeeting(
        @Body request: SummarizeRequest
    ): Response<MeetingDto>

    @DELETE("/api/meetings/{id}")
    suspend fun deleteMeeting(
        @Path("id") id: String
    ): Response<Unit>

    @GET("/health")
    suspend fun healthCheck(): Response<HealthResponse>
}

data class SummarizeRequest(
    val meeting_id: String
)

data class HealthResponse(
    val status: String,
    val timestamp: String
)
