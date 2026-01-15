'use client'

import { useState, useRef } from 'react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'

interface VoiceRecorderProps {
  onTranscribed?: (text: string) => void
  onTaskSubmitted?: (taskId: string) => void
}

export function VoiceRecorder({ onTranscribed, onTaskSubmitted }: VoiceRecorderProps) {
  const [isRecording, setIsRecording] = useState(false)
  const [isTranscribing, setIsTranscribing] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [error, setError] = useState<string | null>(null)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const streamRef = useRef<MediaStream | null>(null)
  const chunksRef = useRef<BlobPart[]>([])

  const startRecording = async () => {
    try {
      setError(null)
      
      // Request microphone access
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      })

      streamRef.current = stream
      chunksRef.current = []

      // Create media recorder
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus',
      })

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data)
        }
      }

      mediaRecorder.onstop = async () => {
        await processAudio()
      }

      mediaRecorder.onerror = (event) => {
        setError(`Recording error: ${event.error}`)
      }

      mediaRecorder.start()
      mediaRecorderRef.current = mediaRecorder
      setIsRecording(true)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start recording')
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      
      // Stop all tracks
      streamRef.current?.getTracks().forEach((track) => track.stop())
      
      setIsRecording(false)
    }
  }

  const processAudio = async () => {
    try {
      setIsTranscribing(true)
      
      // Create blob from chunks
      const blob = new Blob(chunksRef.current, { type: 'audio/webm' })
      
      // Create FormData
      const formData = new FormData()
      formData.append('audio', blob, 'recording.webm')
      formData.append('language', 'en')

      // Send to backend for transcription
      const response = await fetch('/api/voice/transcribe', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Transcription failed')
      }

      const data = await response.json()
      setTranscript(data.text)
      
      if (onTranscribed) {
        onTranscribed(data.text)
      }

      // Optionally submit as task immediately
      if (data.text.trim()) {
        submitAsTask(data.text)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Transcription failed')
    } finally {
      setIsTranscribing(false)
    }
  }

  const submitAsTask = async (text: string) => {
    try {
      const response = await fetch('/api/tasks/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          description: text,
          priority: 'normal',
          source: 'voice',
        }),
      })

      if (!response.ok) {
        throw new Error('Task submission failed')
      }

      const data = await response.json()
      
      if (onTaskSubmitted) {
        onTaskSubmitted(data.task_id || data.id)
      }

      // Clear transcript after submission
      setTranscript('')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Task submission failed')
    }
  }

  return (
    <Card className="p-6 space-y-4">
      <div>
        <h3 className="font-semibold mb-2">🎤 Voice Instructions</h3>
        <p className="text-sm text-gray-600">
          Record a voice note to communicate with AI agents naturally.
        </p>
      </div>

      <div className="flex gap-2">
        <Button
          onClick={isRecording ? stopRecording : startRecording}
          variant={isRecording ? 'secondary' : 'primary'}
          disabled={isTranscribing}
        >
          {isRecording && (
            <span className="inline-block animate-pulse mr-2">●</span>
          )}
          {isRecording ? 'Stop Recording' : 'Start Recording'}
        </Button>

        {transcript && (
          <Button
            onClick={() => submitAsTask(transcript)}
            variant="outline"
            disabled={isTranscribing}
          >
            Send
          </Button>
        )}
      </div>

      {isTranscribing && (
        <div className="text-sm text-gray-500 animate-pulse">
          Transcribing audio...
        </div>
      )}

      {transcript && (
        <div className="p-3 bg-blue-50 rounded-lg border border-blue-200">
          <p className="text-sm font-medium text-blue-900">Transcription:</p>
          <p className="text-sm text-blue-800 mt-1">{transcript}</p>
        </div>
      )}

      {error && (
        <div className="p-3 bg-red-50 rounded-lg border border-red-200">
          <p className="text-sm text-red-900">{error}</p>
        </div>
      )}
    </Card>
  )
}
