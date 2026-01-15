"""
Voice API endpoints for audio transcription and voice-based task creation.
Uses OpenAI's Whisper API for speech-to-text conversion.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Form
import httpx
import os
import logging

router = APIRouter(prefix='/api/voice', tags=['voice'])
logger = logging.getLogger(__name__)

# OpenAI Whisper API configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
WHISPER_API_URL = 'https://api.openai.com/v1/audio/transcriptions'


@router.post('/transcribe')
async def transcribe_audio(
    audio: UploadFile = File(...),
    language: str = Form(default='en'),
) -> dict:
    """
    Transcribe audio file to text using OpenAI Whisper API.
    
    Args:
        audio: Audio file (webm, mp3, wav, m4a, etc.)
        language: Language code (e.g., 'en', 'es', 'fr')
    
    Returns:
        {
            'text': 'Transcribed text from audio',
            'language': 'en',
            'duration': 15.5
        }
    """
    try:
        if not OPENAI_API_KEY:
            raise HTTPException(
                status_code=500,
                detail='OpenAI API key not configured'
            )

        # Validate file type
        if audio.content_type not in [
            'audio/webm',
            'audio/mpeg',
            'audio/wav',
            'audio/m4a',
            'audio/ogg',
            'audio/flac',
        ]:
            raise HTTPException(
                status_code=400,
                detail=f'Unsupported audio format: {audio.content_type}'
            )

        # Read audio content
        audio_content = await audio.read()

        if len(audio_content) == 0:
            raise HTTPException(status_code=400, detail='Audio file is empty')

        if len(audio_content) > 25 * 1024 * 1024:  # 25MB limit
            raise HTTPException(status_code=413, detail='Audio file too large')

        # Prepare request to Whisper API
        files = {
            'file': (audio.filename, audio_content, audio.content_type),
        }
        data = {
            'model': 'whisper-1',
            'language': language,
            'temperature': '0.0',  # For consistency
        }
        headers = {
            'Authorization': f'Bearer {OPENAI_API_KEY}',
        }

        # Call Whisper API
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                WHISPER_API_URL,
                files=files,
                data=data,
                headers=headers,
            )

        if response.status_code != 200:
            logger.error(f'Whisper API error: {response.text}')
            raise HTTPException(
                status_code=response.status_code,
                detail='Failed to transcribe audio'
            )

        result = response.json()

        # Extract text
        transcribed_text = result.get('text', '').strip()

        if not transcribed_text:
            return {
                'text': '',
                'language': language,
                'duration': 0,
                'warning': 'No speech detected in audio',
            }

        return {
            'text': transcribed_text,
            'language': language,
            'duration': result.get('duration', None),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Voice transcription error: {str(e)}')
        raise HTTPException(
            status_code=500,
            detail=f'Transcription error: {str(e)}'
        )


@router.post('/check-permission')
async def check_microphone_permission() -> dict:
    """
    Check if microphone access is available (client-side validation endpoint).
    This is mainly for future compatibility - real check happens in browser.
    
    Returns:
        {
            'available': true,
            'message': 'Microphone access available'
        }
    """
    return {
        'available': True,
        'message': 'Microphone API available in modern browsers',
    }


@router.get('/supported-formats')
async def get_supported_formats() -> dict:
    """Get list of supported audio formats for transcription."""
    return {
        'formats': [
            'audio/webm',
            'audio/mpeg',
            'audio/wav',
            'audio/m4a',
            'audio/ogg',
            'audio/flac',
        ],
        'max_duration_seconds': 3600,
        'max_file_size_mb': 25,
    }
