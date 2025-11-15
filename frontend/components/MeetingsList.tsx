'use client'

import { useState, useEffect } from 'react'
import { FileText, Clock, Trash2, Loader2 } from 'lucide-react'
import { listMeetings, deleteMeeting } from '@/lib/api'
import { format } from 'date-fns'

interface Meeting {
  id: string
  title: string
  created_at: string
  duration: number
  language: string
  has_summary: boolean
}

interface MeetingsListProps {
  onMeetingSelect: (meetingId: string) => void
  refreshTrigger: number
}

export default function MeetingsList({ onMeetingSelect, refreshTrigger }: MeetingsListProps) {
  const [meetings, setMeetings] = useState<Meeting[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [deletingId, setDeletingId] = useState<string | null>(null)

  useEffect(() => {
    loadMeetings()
  }, [refreshTrigger])

  const loadMeetings = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await listMeetings()
      setMeetings(data.meetings)
    } catch (err) {
      setError('Failed to load meetings')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (meetingId: string, e: React.MouseEvent) => {
    e.stopPropagation()

    if (!confirm('Are you sure you want to delete this meeting?')) {
      return
    }

    try {
      setDeletingId(meetingId)
      await deleteMeeting(meetingId)
      await loadMeetings()
    } catch (err) {
      setError('Failed to delete meeting')
      console.error(err)
    } finally {
      setDeletingId(null)
    }
  }

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
        {error}
      </div>
    )
  }

  if (meetings.length === 0) {
    return (
      <div className="text-center py-12">
        <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <p className="text-gray-600">No meetings yet</p>
        <p className="text-sm text-gray-500 mt-2">
          Record or upload an audio file to create your first meeting notes
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">
        Recent Meetings ({meetings.length})
      </h2>

      <div className="grid gap-4">
        {meetings.map((meeting) => (
          <div
            key={meeting.id}
            onClick={() => onMeetingSelect(meeting.id)}
            className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <h3 className="font-medium text-gray-900">{meeting.title}</h3>

                <div className="flex items-center space-x-4 mt-2 text-sm text-gray-500">
                  <div className="flex items-center space-x-1">
                    <Clock className="w-4 h-4" />
                    <span>{format(new Date(meeting.created_at), 'MMM d, yyyy h:mm a')}</span>
                  </div>

                  {meeting.duration > 0 && (
                    <div className="flex items-center space-x-1">
                      <span>{formatDuration(meeting.duration)}</span>
                    </div>
                  )}

                  <div className="flex items-center space-x-1">
                    <span className="uppercase text-xs font-medium">{meeting.language}</span>
                  </div>
                </div>

                {meeting.has_summary && (
                  <div className="mt-2">
                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      Summarized
                    </span>
                  </div>
                )}
              </div>

              <button
                onClick={(e) => handleDelete(meeting.id, e)}
                disabled={deletingId === meeting.id}
                className="ml-4 p-2 text-gray-400 hover:text-red-600 transition-colors"
              >
                {deletingId === meeting.id ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <Trash2 className="w-5 h-5" />
                )}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
