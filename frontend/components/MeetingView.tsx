'use client'

import { useState, useEffect } from 'react'
import { ArrowLeft, Loader2, FileText, CheckCircle, Clock } from 'lucide-react'
import { getMeeting, generateSummary } from '@/lib/api'
import { format } from 'date-fns'

interface MeetingData {
  id: string
  title: string
  transcription: string
  summary: string | null
  action_items: string[] | null
  key_points: string[] | null
  language: string
  model_used: string
  duration: number
  created_at: string
  segments: Array<{
    start: number
    end: number
    text: string
  }> | null
}

interface MeetingViewProps {
  meetingId: string
  onBack: () => void
}

export default function MeetingView({ meetingId, onBack }: MeetingViewProps) {
  const [meeting, setMeeting] = useState<MeetingData | null>(null)
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'transcription' | 'summary'>('summary')

  useEffect(() => {
    loadMeeting()
  }, [meetingId])

  const loadMeeting = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await getMeeting(meetingId)
      setMeeting(data)
    } catch (err) {
      setError('Failed to load meeting')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleGenerateSummary = async () => {
    try {
      setGenerating(true)
      setError(null)
      await generateSummary(meetingId)
      await loadMeeting()
      setActiveTab('summary')
    } catch (err) {
      setError('Failed to generate summary')
      console.error(err)
    } finally {
      setGenerating(false)
    }
  }

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const formatTimestamp = (seconds: number) => {
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

  if (error || !meeting) {
    return (
      <div>
        <button
          onClick={onBack}
          className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 mb-4"
        >
          <ArrowLeft className="w-5 h-5" />
          <span>Back to meetings</span>
        </button>
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error || 'Meeting not found'}
        </div>
      </div>
    )
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <button
          onClick={onBack}
          className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 mb-4"
        >
          <ArrowLeft className="w-5 h-5" />
          <span>Back to meetings</span>
        </button>

        <h1 className="text-2xl font-bold text-gray-900">{meeting.title}</h1>

        <div className="flex items-center space-x-4 mt-2 text-sm text-gray-500">
          <div className="flex items-center space-x-1">
            <Clock className="w-4 h-4" />
            <span>{format(new Date(meeting.created_at), 'MMM d, yyyy h:mm a')}</span>
          </div>

          {meeting.duration > 0 && (
            <span>{formatDuration(meeting.duration)}</span>
          )}

          <span className="uppercase font-medium">{meeting.language}</span>
          <span className="text-xs bg-gray-100 px-2 py-1 rounded">{meeting.model_used}</span>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow-sm mb-6">
        <nav className="flex space-x-1 p-1 border-b">
          <button
            onClick={() => setActiveTab('summary')}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              activeTab === 'summary'
                ? 'bg-blue-600 text-white'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            Summary
          </button>
          <button
            onClick={() => setActiveTab('transcription')}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              activeTab === 'transcription'
                ? 'bg-blue-600 text-white'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            Full Transcription
          </button>
        </nav>

        <div className="p-6">
          {activeTab === 'summary' && (
            <div>
              {meeting.summary ? (
                <div className="space-y-6">
                  {/* Summary */}
                  <div>
                    <h2 className="text-lg font-semibold text-gray-900 mb-3">Summary</h2>
                    <p className="text-gray-700 whitespace-pre-wrap">{meeting.summary}</p>
                  </div>

                  {/* Action Items */}
                  {meeting.action_items && meeting.action_items.length > 0 && (
                    <div>
                      <h2 className="text-lg font-semibold text-gray-900 mb-3">Action Items</h2>
                      <ul className="space-y-2">
                        {meeting.action_items.map((item, index) => (
                          <li key={index} className="flex items-start space-x-3">
                            <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                            <span className="text-gray-700">{item}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Key Points */}
                  {meeting.key_points && meeting.key_points.length > 0 && (
                    <div>
                      <h2 className="text-lg font-semibold text-gray-900 mb-3">Key Points</h2>
                      <ul className="list-disc list-inside space-y-2">
                        {meeting.key_points.map((point, index) => (
                          <li key={index} className="text-gray-700">{point}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-8">
                  <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-600 mb-4">No summary generated yet</p>
                  <button
                    onClick={handleGenerateSummary}
                    disabled={generating}
                    className="inline-flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-6 py-2 rounded-lg transition-colors"
                  >
                    {generating ? (
                      <>
                        <Loader2 className="w-5 h-5 animate-spin" />
                        <span>Generating...</span>
                      </>
                    ) : (
                      <span>Generate Summary</span>
                    )}
                  </button>
                </div>
              )}
            </div>
          )}

          {activeTab === 'transcription' && (
            <div>
              {meeting.segments && meeting.segments.length > 0 ? (
                <div className="space-y-4">
                  {meeting.segments.map((segment, index) => (
                    <div key={index} className="border-l-2 border-blue-500 pl-4">
                      <div className="text-xs text-gray-500 mb-1">
                        {formatTimestamp(segment.start)} - {formatTimestamp(segment.end)}
                      </div>
                      <p className="text-gray-700">{segment.text}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="prose max-w-none">
                  <p className="text-gray-700 whitespace-pre-wrap">{meeting.transcription}</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
