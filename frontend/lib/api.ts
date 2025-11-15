/**
 * API client for Notulen backend
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function transcribeAudio(file: File, language = 'auto', modelPreference = 'auto') {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(
    `${API_URL}/api/transcribe?language=${language}&model_preference=${modelPreference}`,
    {
      method: 'POST',
      body: formData,
    }
  )

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Transcription failed')
  }

  return response.json()
}

export async function generateSummary(meetingId: string) {
  const response = await fetch(`${API_URL}/api/summarize`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ meeting_id: meetingId }),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Summary generation failed')
  }

  return response.json()
}

export async function listMeetings(limit = 50, offset = 0) {
  const response = await fetch(
    `${API_URL}/api/meetings?limit=${limit}&offset=${offset}`
  )

  if (!response.ok) {
    throw new Error('Failed to fetch meetings')
  }

  return response.json()
}

export async function getMeeting(meetingId: string) {
  const response = await fetch(`${API_URL}/api/meetings/${meetingId}`)

  if (!response.ok) {
    throw new Error('Failed to fetch meeting')
  }

  return response.json()
}

export async function deleteMeeting(meetingId: string) {
  const response = await fetch(`${API_URL}/api/meetings/${meetingId}`, {
    method: 'DELETE',
  })

  if (!response.ok) {
    throw new Error('Failed to delete meeting')
  }

  return response.json()
}

export async function healthCheck() {
  const response = await fetch(`${API_URL}/health`)

  if (!response.ok) {
    throw new Error('Health check failed')
  }

  return response.json()
}
