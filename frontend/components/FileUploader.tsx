'use client'

import { useState, useRef } from 'react'
import { Upload, Loader2, FileAudio } from 'lucide-react'
import { transcribeAudio } from '@/lib/api'

interface FileUploaderProps {
  onComplete: () => void
}

export default function FileUploader({ onComplete }: FileUploaderProps) {
  const [isProcessing, setIsProcessing] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setSelectedFile(file)
      setError(null)
    }
  }

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    const file = e.dataTransfer.files?.[0]
    if (file) {
      if (isAudioFile(file)) {
        setSelectedFile(file)
        setError(null)
      } else {
        setError('Please upload an audio file (MP3, WAV, M4A, WebM)')
      }
    }
  }

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
  }

  const isAudioFile = (file: File) => {
    const audioTypes = ['audio/mpeg', 'audio/mp3', 'audio/wav', 'audio/x-m4a', 'audio/webm', 'audio/mp4']
    return audioTypes.includes(file.type) || /\.(mp3|wav|m4a|webm|mp4)$/i.test(file.name)
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file first')
      return
    }

    try {
      setIsProcessing(true)
      setError(null)

      await transcribeAudio(selectedFile)

      setSelectedFile(null)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }

      onComplete()
    } catch (err) {
      setError('Failed to process audio file. Please try again.')
      console.error(err)
    } finally {
      setIsProcessing(false)
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
  }

  return (
    <div className="flex flex-col items-center justify-center space-y-6 py-8">
      {/* Drop zone */}
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        className="w-full max-w-2xl border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-blue-400 transition-colors cursor-pointer"
        onClick={() => fileInputRef.current?.click()}
      >
        <Upload className="w-16 h-16 text-gray-400 mx-auto mb-4" />

        <input
          ref={fileInputRef}
          type="file"
          accept="audio/*,.mp3,.wav,.m4a,.webm,.mp4"
          onChange={handleFileSelect}
          className="hidden"
        />

        {selectedFile ? (
          <div className="space-y-2">
            <FileAudio className="w-12 h-12 text-blue-600 mx-auto" />
            <p className="text-lg font-medium text-gray-900">{selectedFile.name}</p>
            <p className="text-sm text-gray-500">{formatFileSize(selectedFile.size)}</p>
          </div>
        ) : (
          <div>
            <p className="text-lg font-medium text-gray-700 mb-2">
              Drop audio file here or click to browse
            </p>
            <p className="text-sm text-gray-500">
              Supports MP3, WAV, M4A, WebM (max 100MB)
            </p>
          </div>
        )}
      </div>

      {/* Error message */}
      {error && (
        <div className="w-full max-w-2xl bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {/* Upload button */}
      {selectedFile && !isProcessing && (
        <button
          onClick={handleUpload}
          className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg shadow-lg transition-colors"
        >
          <Upload className="w-5 h-5" />
          <span className="font-medium">Transcribe Audio</span>
        </button>
      )}

      {/* Processing status */}
      {isProcessing && (
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-blue-600 animate-spin mx-auto" />
          <p className="mt-4 text-gray-600">Processing your audio file...</p>
          <p className="text-sm text-gray-500 mt-2">This may take a few minutes depending on file size</p>
        </div>
      )}
    </div>
  )
}
