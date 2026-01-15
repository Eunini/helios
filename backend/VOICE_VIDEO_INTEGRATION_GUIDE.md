"""
Integration examples for using voice and video components in the dashboard.
This file shows how to integrate the new voice and video features into existing dashboard pages.
"""

# Example 1: Adding Voice Recorder to Dashboard Page

# File: frontend/app/dashboard/page.tsx

"""
'use client'

import { useState } from 'react'
import { VoiceRecorder } from '@/components/voice'
import { VideoChat } from '@/components/video'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

export default function DashboardPage() {
const [showVoice, setShowVoice] = useState(false)
const [showVideo, setShowVideo] = useState(false)
const [lastTaskId, setLastTaskId] = useState<string | null>(null)

const handleVoiceTaskCreated = (taskId: string) => {
setLastTaskId(taskId)
// Refresh tasks list or show notification
console.log(`New task created: ${taskId}`)
}

return (
<div className="space-y-6">
{/_ Existing dashboard content _/}

      {/* Voice & Video Features Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card className="p-4">
          <Button
            onClick={() => setShowVoice(!showVoice)}
            variant="primary"
            className="w-full"
          >
            {showVoice ? '🎤 Hide Voice Recorder' : '🎤 Show Voice Recorder'}
          </Button>
          {showVoice && (
            <div className="mt-4">
              <VoiceRecorder
                onTranscribed={(text) => console.log('Transcribed:', text)}
                onTaskSubmitted={handleVoiceTaskCreated}
              />
            </div>
          )}
        </Card>

        <Card className="p-4">
          <Button
            onClick={() => setShowVideo(!showVideo)}
            variant="primary"
            className="w-full"
          >
            {showVideo ? '📹 Hide Video Chat' : '📹 Show Video Chat'}
          </Button>
          {showVideo && (
            <div className="mt-4">
              <VideoChat />
            </div>
          )}
        </Card>
      </div>

      {lastTaskId && (
        <Card className="p-4 bg-green-50 border border-green-200">
          <p className="text-sm text-green-900">
            ✅ Task created: {lastTaskId}
          </p>
        </Card>
      )}
    </div>

)
}
"""

# Example 2: Dedicated Voice Interface Page

# File: frontend/app/dashboard/voice/page.tsx

"""
'use client'

import { useState, useEffect } from 'react'
import { VoiceRecorder } from '@/components/voice'
import { Card } from '@/components/ui/card'

interface VoiceTask {
id: string
transcript: string
createdAt: Date
status: 'pending' | 'processing' | 'complete'
}

export default function VoicePage() {
const [tasks, setTasks] = useState<VoiceTask[]>([])

const handleTaskSubmitted = async (taskId: string) => {
// Fetch task details from API
try {
const response = await fetch(`/api/tasks/${taskId}`)
const task = await response.json()

      setTasks((prev) => [
        {
          id: taskId,
          transcript: task.description,
          createdAt: new Date(),
          status: 'pending',
        },
        ...prev,
      ])
    } catch (error) {
      console.error('Failed to fetch task:', error)
    }

}

useEffect(() => {
// Periodically check task status
const interval = setInterval(async () => {
// Update task statuses
}, 5000)

    return () => clearInterval(interval)

}, [tasks])

return (
<div className="space-y-6">
<h1 className="text-3xl font-bold">🎤 Voice Tasks</h1>

      <VoiceRecorder onTaskSubmitted={handleTaskSubmitted} />

      {/* Recent Tasks */}
      <div className="space-y-2">
        <h2 className="text-xl font-semibold">Recent Tasks</h2>
        {tasks.length === 0 ? (
          <p className="text-gray-500">No voice tasks yet</p>
        ) : (
          <div className="space-y-2">
            {tasks.map((task) => (
              <Card key={task.id} className="p-4">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-medium">{task.transcript}</p>
                    <p className="text-xs text-gray-500">
                      {task.createdAt.toLocaleString()}
                    </p>
                  </div>
                  <span
                    className={`px-2 py-1 rounded text-xs font-semibold ${
                      task.status === 'complete'
                        ? 'bg-green-100 text-green-800'
                        : task.status === 'processing'
                        ? 'bg-blue-100 text-blue-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}
                  >
                    {task.status.charAt(0).toUpperCase() + task.status.slice(1)}
                  </span>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>

)
}
"""

# Example 3: Dedicated Video Chat Page

# File: frontend/app/dashboard/video/page.tsx

"""
'use client'

import { useState } from 'react'
import { VideoChat } from '@/components/video'
import { Card } from '@/components/ui/card'

export default function VideoChatPage() {
const [sessionId, setSessionId] = useState<string | null>(null)
const [sessionHistory, setSessionHistory] = useState<any[]>([])

const handleSessionStart = (id: string) => {
setSessionId(id)
}

const handleSessionEnd = () => {
setSessionId(null)
// Fetch session history from API
fetchSessionHistory()
}

const fetchSessionHistory = async () => {
try {
const response = await fetch('/api/ws/video-chat/sessions')
const data = await response.json()
setSessionHistory(data.sessions)
} catch (error) {
console.error('Failed to fetch session history:', error)
}
}

return (
<div className="space-y-6">
<h1 className="text-3xl font-bold">📹 Video Chat</h1>

      <VideoChat />

      {/* Session History */}
      <div className="space-y-2">
        <h2 className="text-xl font-semibold">Session History</h2>
        {sessionHistory.length === 0 ? (
          <p className="text-gray-500">No sessions yet</p>
        ) : (
          <div className="space-y-2">
            {sessionHistory.map((session) => (
              <Card key={session.session_id} className="p-4">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-medium">{session.session_id}</p>
                    <p className="text-xs text-gray-500">
                      Duration: {session.duration_seconds.toFixed(1)}s
                    </p>
                    <p className="text-xs text-gray-500">
                      Messages: {session.total_messages}
                    </p>
                  </div>
                  <span className="text-xs text-gray-500">
                    {new Date(session.connected_at).toLocaleString()}
                  </span>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>

)
}
"""

# Example 4: Environment Variables Setup

# File: .env.local (frontend)

"""
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENABLE_VOICE=true
NEXT_PUBLIC_ENABLE_VIDEO=true
"""

# File: .env (backend)

"""
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./helios.db
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
"""

# Example 5: API Client Utilities

# File: frontend/lib/api.ts (updated with voice/video helpers)

"""
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const voiceApi = {
async transcribeAudio(audioBlob: Blob, language: string = 'en') {
const formData = new FormData()
formData.append('audio', audioBlob)
formData.append('language', language)

    const response = await axios.post(
      `${API_URL}/api/voice/transcribe`,
      formData,
      {
        headers: { 'Content-Type': 'multipart/form-data' },
      }
    )
    return response.data

},

async getSupportedFormats() {
const response = await axios.get(
`${API_URL}/api/voice/supported-formats`
)
return response.data
},

async checkMicrophonePermission() {
const response = await axios.post(
`${API_URL}/api/voice/check-permission`
)
return response.data
},
}

export const videoChatApi = {
connectWebSocket(sessionId?: string) {
const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
return new WebSocket(`${protocol}//${window.location.host}/api/ws/video-chat`)
},

async listActiveSessions() {
const response = await axios.get(`${API_URL}/api/ws/video-chat/sessions`)
return response.data
},

async getSessionDetails(sessionId: string) {
const response = await axios.get(
`${API_URL}/api/ws/video-chat/session/${sessionId}`
)
return response.data
},

async endSession(sessionId: string) {
const response = await axios.post(
`${API_URL}/api/ws/video-chat/session/${sessionId}/end`
)
return response.data
},

async checkHealth() {
const response = await axios.get(`${API_URL}/api/ws/video-chat/health`)
return response.data
},
}
"""
