'use client'

import { useRef, useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Textarea } from '@/components/ui/textarea'

interface VideoChatMessage {
  role: 'user' | 'agent'
  text: string
  timestamp: Date
}

export function VideoChat() {
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const wsRef = useRef<WebSocket | null>(null)
  
  const [isActive, setIsActive] = useState(false)
  const [messages, setMessages] = useState<VideoChatMessage[]>([])
  const [currentInput, setCurrentInput] = useState('')
  const [isListening, setIsListening] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [stats, setStats] = useState({
    latency: 0,
    frameRate: 0,
    resolution: '0x0',
  })

  const recognitionRef = useRef<any>(null)

  // Initialize Speech Recognition
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const SpeechRecognition =
        (window as any).SpeechRecognition ||
        (window as any).webkitSpeechRecognition

      if (SpeechRecognition) {
        recognitionRef.current = new SpeechRecognition()
        recognitionRef.current.continuous = true
        recognitionRef.current.interimResults = true
        recognitionRef.current.lang = 'en-US'

        recognitionRef.current.onstart = () => setIsListening(true)
        recognitionRef.current.onend = () => setIsListening(false)

        recognitionRef.current.onresult = (event: any) => {
          let interim_transcript = ''

          for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript

            if (event.results[i].isFinal) {
              setCurrentInput((prev) => prev + transcript + ' ')
            } else {
              interim_transcript += transcript
            }
          }
        }
      }
    }

    return () => {
      recognitionRef.current?.abort()
    }
  }, [])

  const startVideoChat = async () => {
    try {
      setError(null)

      // Get media stream
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 1280 },
          height: { ideal: 720 },
          facingMode: 'user',
        },
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
        },
      })

      if (videoRef.current) {
        videoRef.current.srcObject = stream
      }

      // Initialize WebSocket
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const wsUrl = `${protocol}//${window.location.host}/api/ws/video-chat`

      wsRef.current = new WebSocket(wsUrl)

      wsRef.current.onopen = () => {
        console.log('Connected to video chat server')
        setIsActive(true)
        addSystemMessage('Connected to AI agent. Press "Listen" to start talking.')

        // Start sending frames periodically
        sendVideoFrames(stream)
      }

      wsRef.current.onmessage = (event) => {
        const data = JSON.parse(event.data)
        handleAgentMessage(data)
      }

      wsRef.current.onerror = (event) => {
        setError('WebSocket connection error')
        console.error('WebSocket error:', event)
      }

      wsRef.current.onclose = () => {
        setIsActive(false)
        addSystemMessage('Disconnected from agent.')
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start video chat')
    }
  }

  const sendVideoFrames = (stream: MediaStream) => {
    if (!canvasRef.current) return

    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const video = videoRef.current
    if (!video) return

    const sendFrame = () => {
      if (!isActive || !wsRef.current) return

      try {
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height)

        // Send frame every 1000ms (1 FPS for low bandwidth)
        canvas.toBlob((blob) => {
          if (blob && wsRef.current?.readyState === WebSocket.OPEN) {
            // Send as binary data
            wsRef.current?.send(
              JSON.stringify({
                type: 'frame',
                timestamp: Date.now(),
              })
            )

            // Update stats
            setStats((prev) => ({
              ...prev,
              resolution: `${canvas.width}x${canvas.height}`,
              frameRate: 1, // 1 FPS
            }))
          }
        }, 'image/jpeg')
      } catch (e) {
        console.error('Error sending frame:', e)
      }

      setTimeout(sendFrame, 1000) // Send frame every second
    }

    sendFrame()
  }

  const handleAgentMessage = (data: any) => {
    const message: VideoChatMessage = {
      role: 'agent',
      text: data.response || data.message || '',
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, message])

    // Speak response
    if (data.response) {
      speak(data.response)
    }

    // Update stats if included
    if (data.latency !== undefined) {
      setStats((prev) => ({
        ...prev,
        latency: data.latency,
      }))
    }
  }

  const addSystemMessage = (text: string) => {
    setMessages((prev) => [
      ...prev,
      {
        role: 'agent',
        text,
        timestamp: new Date(),
      },
    ])
  }

  const toggleListening = () => {
    if (!recognitionRef.current) {
      setError('Speech recognition not available in this browser')
      return
    }

    if (isListening) {
      recognitionRef.current.stop()
    } else {
      setCurrentInput('')
      recognitionRef.current.start()
    }
  }

  const sendMessage = async () => {
    if (!currentInput.trim() || !wsRef.current) return

    const userMessage: VideoChatMessage = {
      role: 'user',
      text: currentInput,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])

    // Send to WebSocket
    wsRef.current.send(
      JSON.stringify({
        type: 'message',
        text: currentInput,
        timestamp: Date.now(),
      })
    )

    setCurrentInput('')
  }

  const speak = (text: string) => {
    if (!('speechSynthesis' in window)) {
      console.log('Speech synthesis not available')
      return
    }

    const utterance = new SpeechSynthesisUtterance(text)
    utterance.rate = 1.0
    utterance.pitch = 1.0
    utterance.volume = 1.0

    speechSynthesis.speak(utterance)
  }

  const endCall = () => {
    if (videoRef.current?.srcObject) {
      (videoRef.current.srcObject as MediaStream)
        .getTracks()
        .forEach((track) => track.stop())
    }

    wsRef.current?.close()
    setIsActive(false)
    setMessages([])
    setCurrentInput('')
  }

  return (
    <div className="space-y-4">
      <Card className="p-6 space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Video Display */}
          <div>
            <h3 className="font-semibold mb-2">📹 Live Feed</h3>
            <div className="relative bg-black rounded-lg overflow-hidden">
              <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className="w-full aspect-video object-cover"
              />
              <canvas
                ref={canvasRef}
                className="hidden"
                width={1280}
                height={720}
              />

              {/* Stats Overlay */}
              {isActive && (
                <div className="absolute bottom-2 left-2 text-xs text-white bg-black/50 p-2 rounded">
                  <div>📊 {stats.resolution}</div>
                  <div>⏱️ {stats.latency}ms</div>
                  <div>📈 {stats.frameRate} FPS</div>
                </div>
              )}

              {/* Recording Indicator */}
              {isActive && (
                <div className="absolute top-2 right-2">
                  <div className="flex items-center gap-1 bg-red-500 text-white px-2 py-1 rounded text-xs font-semibold animate-pulse">
                    ● REC
                  </div>
                </div>
              )}
            </div>

            {/* Controls */}
            <div className="flex gap-2 mt-4">
              {!isActive ? (
                <Button onClick={startVideoChat} variant="primary" className="flex-1">
                  📹 Start Video Chat
                </Button>
              ) : (
                <Button onClick={endCall} variant="secondary" className="flex-1">
                  ❌ End Call
                </Button>
              )}

              {isActive && (
                <Button
                  onClick={toggleListening}
                  variant={isListening ? 'secondary' : 'outline'}
                  className="flex-1"
                >
                  {isListening ? '🎤 Listening...' : '🎤 Listen'}
                </Button>
              )}
            </div>
          </div>

          {/* Chat Interface */}
          <div className="flex flex-col">
            <h3 className="font-semibold mb-2">💬 Chat</h3>

            {/* Messages */}
            <div className="flex-1 bg-gray-50 rounded-lg p-4 mb-4 overflow-y-auto max-h-96 border border-gray-200">
              {messages.length === 0 ? (
                <p className="text-gray-500 text-sm text-center mt-8">
                  No messages yet. Start the chat to begin.
                </p>
              ) : (
                <div className="space-y-3">
                  {messages.map((msg, idx) => (
                    <div key={idx} className="space-y-1">
                      <div className="text-xs font-semibold text-gray-600">
                        {msg.role === 'user' ? '👤 You' : '🤖 Agent'}
                      </div>
                      <div
                        className={`text-sm p-2 rounded ${
                          msg.role === 'user'
                            ? 'bg-blue-100 text-blue-900'
                            : 'bg-gray-200 text-gray-900'
                        }`}
                      >
                        {msg.text}
                      </div>
                      <div className="text-xs text-gray-500">
                        {msg.timestamp.toLocaleTimeString()}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Input */}
            {isActive && (
              <div className="space-y-2">
                <Textarea
                  value={currentInput}
                  onChange={(e) => setCurrentInput(e.target.value)}
                  onKeyPress={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault()
                      sendMessage()
                    }
                  }}
                  placeholder="Type message or use voice..."
                  className="min-h-20 resize-none"
                />
                <Button
                  onClick={sendMessage}
                  variant="primary"
                  className="w-full"
                  disabled={!currentInput.trim()}
                >
                  Send
                </Button>
              </div>
            )}
          </div>
        </div>

        {error && (
          <div className="p-3 bg-red-50 border border-red-200 rounded text-sm text-red-900">
            {error}
          </div>
        )}

        {/* Info */}
        <div className="p-3 bg-blue-50 border border-blue-200 rounded text-sm text-blue-900">
          <p className="font-semibold mb-1">ℹ️ Tips:</p>
          <ul className="list-disc pl-5 space-y-1">
            <li>Use &quot;Listen&quot; button for voice input</li>
            <li>Type or speak to communicate with the AI</li>
            <li>Agent can see your video and respond naturally</li>
            <li>Works best with stable internet connection</li>
          </ul>
        </div>
      </Card>
    </div>
  )
}
