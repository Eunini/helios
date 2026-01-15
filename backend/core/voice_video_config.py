"""
Configuration settings for voice and video services.
"""

import os
from typing import List

# Voice Transcription Settings
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
WHISPER_MODEL = 'whisper-1'
SUPPORTED_AUDIO_FORMATS = [
    'audio/webm',
    'audio/mpeg',
    'audio/wav',
    'audio/m4a',
    'audio/ogg',
    'audio/flac',
]
MAX_AUDIO_DURATION_SECONDS = 3600  # 1 hour
MAX_AUDIO_FILE_SIZE_MB = 25
DEFAULT_AUDIO_LANGUAGE = 'en'

# Video Chat Settings
VIDEO_CHAT_ENABLED = os.getenv('VIDEO_CHAT_ENABLED', 'true').lower() == 'true'
VIDEO_FRAME_RATE = 1  # Frames per second
MAX_VIDEO_RESOLUTION = (1280, 720)
VIDEO_QUALITY = 'high'  # high, medium, low

# WebSocket Settings
WEBSOCKET_TIMEOUT_SECONDS = 3600  # 1 hour
WEBSOCKET_HEARTBEAT_INTERVAL = 30  # seconds
MAX_CONCURRENT_WEBSOCKET_CONNECTIONS = 1000

# Real-time Communication
ENABLE_REAL_TIME_TRANSCRIPTION = os.getenv(
    'ENABLE_REAL_TIME_TRANSCRIPTION', 'false'
).lower() == 'true'
ENABLE_VIDEO_ANALYSIS = os.getenv(
    'ENABLE_VIDEO_ANALYSIS', 'false'
).lower() == 'true'

# Security
VOICE_ENABLE_RATE_LIMITING = True
VOICE_RATE_LIMIT_PER_MINUTE = 60
VOICE_RATE_LIMIT_PER_HOUR = 1000

# Logging
VOICE_VIDEO_LOG_LEVEL = os.getenv('VOICE_VIDEO_LOG_LEVEL', 'INFO')
ENABLE_VOICE_VIDEO_DEBUG = os.getenv(
    'ENABLE_VOICE_VIDEO_DEBUG', 'false'
).lower() == 'true'


class VoiceConfig:
    """Configuration for voice features."""

    api_key = OPENAI_API_KEY
    model = WHISPER_MODEL
    supported_formats = SUPPORTED_AUDIO_FORMATS
    max_duration = MAX_AUDIO_DURATION_SECONDS
    max_file_size = MAX_AUDIO_FILE_SIZE_MB
    default_language = DEFAULT_AUDIO_LANGUAGE

    @classmethod
    def validate(cls) -> bool:
        """Validate voice configuration."""
        if not cls.api_key:
            raise ValueError('OPENAI_API_KEY not set')
        return True


class VideoConfig:
    """Configuration for video chat features."""

    enabled = VIDEO_CHAT_ENABLED
    frame_rate = VIDEO_FRAME_RATE
    max_resolution = MAX_VIDEO_RESOLUTION
    quality = VIDEO_QUALITY
    enable_analysis = ENABLE_VIDEO_ANALYSIS

    @classmethod
    def validate(cls) -> bool:
        """Validate video configuration."""
        if not cls.enabled:
            return True
        return True


class WebSocketConfig:
    """Configuration for WebSocket connections."""

    timeout = WEBSOCKET_TIMEOUT_SECONDS
    heartbeat_interval = WEBSOCKET_HEARTBEAT_INTERVAL
    max_connections = MAX_CONCURRENT_WEBSOCKET_CONNECTIONS


def validate_voice_config():
    """Validate voice feature configuration."""
    try:
        VoiceConfig.validate()
        return True
    except ValueError as e:
        print(f'Voice config error: {e}')
        return False


def validate_video_config():
    """Validate video feature configuration."""
    try:
        VideoConfig.validate()
        return True
    except ValueError as e:
        print(f'Video config error: {e}')
        return False
