'use client'

import { useState } from 'react'
import AudioRecorder from '@/components/AudioRecorder'
import FileUploader from '@/components/FileUploader'
import MeetingsList from '@/components/MeetingsList'
import MeetingView from '@/components/MeetingView'
import { FileAudio, Mic } from 'lucide-react'

export default function Home() {
  const [activeTab, setActiveTab] = useState<'record' | 'upload' | 'meetings'>('record')
  const [selectedMeetingId, setSelectedMeetingId] = useState<string | null>(null)
  const [refreshTrigger, setRefreshTrigger] = useState(0)

  const handleTranscriptionComplete = () => {
    setRefreshTrigger(prev => prev + 1)
    setActiveTab('meetings')
  }

  const handleMeetingSelect = (meetingId: string) => {
    setSelectedMeetingId(meetingId)
  }

  const handleBackToList = () => {
    setSelectedMeetingId(null)
    setRefreshTrigger(prev => prev + 1)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            Notulen
          </h1>
          <p className="mt-1 text-sm text-gray-600">
            Indonesian Meeting Note Taker with AI-powered transcription
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {selectedMeetingId ? (
          <MeetingView
            meetingId={selectedMeetingId}
            onBack={handleBackToList}
          />
        ) : (
          <>
            {/* Tab Navigation */}
            <div className="bg-white rounded-lg shadow-sm mb-6">
              <nav className="flex space-x-1 p-1">
                <button
                  onClick={() => setActiveTab('record')}
                  className={`flex items-center px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                    activeTab === 'record'
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  <Mic className="w-4 h-4 mr-2" />
                  Record
                </button>
                <button
                  onClick={() => setActiveTab('upload')}
                  className={`flex items-center px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                    activeTab === 'upload'
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  <FileAudio className="w-4 h-4 mr-2" />
                  Upload
                </button>
                <button
                  onClick={() => setActiveTab('meetings')}
                  className={`flex items-center px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                    activeTab === 'meetings'
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  Meetings
                </button>
              </nav>
            </div>

            {/* Content */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              {activeTab === 'record' && (
                <AudioRecorder onComplete={handleTranscriptionComplete} />
              )}
              {activeTab === 'upload' && (
                <FileUploader onComplete={handleTranscriptionComplete} />
              )}
              {activeTab === 'meetings' && (
                <MeetingsList
                  onMeetingSelect={handleMeetingSelect}
                  refreshTrigger={refreshTrigger}
                />
              )}
            </div>
          </>
        )}
      </main>
    </div>
  )
}
