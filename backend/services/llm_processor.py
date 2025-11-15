"""
LLM Processor - Generate summaries and extract action items
Uses OpenAI GPT-4, Anthropic Claude, or OpenRouter
"""

import os
import logging
from typing import Dict, Any, List
import json

logger = logging.getLogger(__name__)


class LLMProcessor:
    """
    Process transcriptions using LLM for:
    - Meeting summaries
    - Action item extraction
    - Key points identification
    - Speaker identification (future)
    """

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai")  # openai, anthropic, or openrouter
        self.client = None
        self._init_client()

    def _init_client(self):
        """Initialize LLM client"""
        try:
            if self.provider == "openai":
                from openai import AsyncOpenAI
                api_key = os.getenv("OPENAI_API_KEY")
                if api_key:
                    self.client = AsyncOpenAI(api_key=api_key)
                    logger.info("OpenAI client initialized")
                else:
                    logger.warning("OPENAI_API_KEY not set")

            elif self.provider == "anthropic":
                from anthropic import AsyncAnthropic
                api_key = os.getenv("ANTHROPIC_API_KEY")
                if api_key:
                    self.client = AsyncAnthropic(api_key=api_key)
                    logger.info("Anthropic client initialized")
                else:
                    logger.warning("ANTHROPIC_API_KEY not set")

            elif self.provider == "openrouter":
                from openai import AsyncOpenAI
                api_key = os.getenv("OPENROUTER_API_KEY")
                if api_key:
                    self.client = AsyncOpenAI(
                        api_key=api_key,
                        base_url="https://openrouter.ai/api/v1"
                    )
                    logger.info("OpenRouter client initialized")
                else:
                    logger.warning("OPENROUTER_API_KEY not set")

        except Exception as e:
            logger.error(f"Failed to initialize LLM client: {e}")
            self.client = None

    def is_available(self) -> bool:
        """Check if LLM service is available"""
        return self.client is not None

    async def generate_summary(
        self,
        transcription: str,
        language: str = "id"
    ) -> Dict[str, Any]:
        """
        Generate meeting summary and extract insights

        Args:
            transcription: Full meeting transcription
            language: Language of the meeting (id, en, etc.)

        Returns:
            Dictionary with summary, action_items, key_points
        """
        if not self.is_available():
            # Return basic summary if LLM not available
            return self._generate_basic_summary(transcription)

        try:
            if self.provider == "openai":
                return await self._summarize_openai(transcription, language)
            elif self.provider == "anthropic":
                return await self._summarize_anthropic(transcription, language)
            elif self.provider == "openrouter":
                return await self._summarize_openrouter(transcription, language)
        except Exception as e:
            logger.error(f"LLM summarization failed: {e}")
            return self._generate_basic_summary(transcription)

    async def _summarize_openai(self, transcription: str, language: str) -> Dict[str, Any]:
        """Generate summary using OpenAI GPT-4"""

        system_prompt = self._get_system_prompt(language)

        response = await self.client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Meeting Transcription:\n\n{transcription}"}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)

        return {
            "summary": result.get("summary", ""),
            "action_items": result.get("action_items", []),
            "key_points": result.get("key_points", []),
            "participants": result.get("participants")
        }

    async def _summarize_anthropic(self, transcription: str, language: str) -> Dict[str, Any]:
        """Generate summary using Anthropic Claude"""

        system_prompt = self._get_system_prompt(language)

        response = await self.client.messages.create(
            model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
            max_tokens=2000,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Meeting Transcription:\n\n{transcription}\n\nPlease provide a JSON response."
                }
            ]
        )

        # Parse JSON from response
        content = response.content[0].text

        # Extract JSON if it's wrapped in markdown code blocks
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        result = json.loads(content)

        return {
            "summary": result.get("summary", ""),
            "action_items": result.get("action_items", []),
            "key_points": result.get("key_points", []),
            "participants": result.get("participants")
        }

    async def _summarize_openrouter(self, transcription: str, language: str) -> Dict[str, Any]:
        """Generate summary using OpenRouter (supports 100+ models)"""

        system_prompt = self._get_system_prompt(language)

        # Get model from env, default to DeepSeek V3 (free/cheap, great for Indonesian)
        model = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-r1-0528-qwen3-8b:free")

        response = await self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Meeting Transcription:\n\n{transcription}"}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)

        return {
            "summary": result.get("summary", ""),
            "action_items": result.get("action_items", []),
            "key_points": result.get("key_points", []),
            "participants": result.get("participants")
        }

    def _get_system_prompt(self, language: str) -> str:
        """Get system prompt based on language"""

        if language == "id":
            return """Anda adalah asisten AI yang membantu merangkum meeting notes dalam bahasa Indonesia.

Tugas Anda:
1. Buat ringkasan meeting yang komprehensif dan terstruktur
2. Identifikasi dan ekstrak semua action items (tugas yang harus dilakukan)
3. Ekstrak poin-poin penting dari diskusi
4. Identifikasi peserta meeting jika memungkinkan

Format output dalam JSON:
{
  "summary": "Ringkasan meeting dalam 2-3 paragraf",
  "action_items": ["Action item 1", "Action item 2", ...],
  "key_points": ["Poin penting 1", "Poin penting 2", ...],
  "participants": ["Nama 1", "Nama 2", ...] atau null jika tidak teridentifikasi
}

Pastikan ringkasan mencakup:
- Topik utama yang dibahas
- Keputusan yang diambil
- Isu atau masalah yang diangkat
- Next steps atau rencana tindak lanjut"""

        else:  # English
            return """You are an AI assistant that helps summarize meeting notes.

Your tasks:
1. Create a comprehensive and structured meeting summary
2. Identify and extract all action items (tasks to be done)
3. Extract key points from the discussion
4. Identify meeting participants if possible

Output format in JSON:
{
  "summary": "Meeting summary in 2-3 paragraphs",
  "action_items": ["Action item 1", "Action item 2", ...],
  "key_points": ["Key point 1", "Key point 2", ...],
  "participants": ["Name 1", "Name 2", ...] or null if not identified
}

Ensure the summary covers:
- Main topics discussed
- Decisions made
- Issues or problems raised
- Next steps or follow-up plans"""

    def _generate_basic_summary(self, transcription: str) -> Dict[str, Any]:
        """Generate basic summary when LLM is not available"""

        # Simple extraction of sentences that might be action items
        sentences = transcription.split('.')
        action_words = ['akan', 'harus', 'perlu', 'tolong', 'should', 'will', 'need', 'must', 'please']

        action_items = []
        for sentence in sentences:
            sentence = sentence.strip()
            if any(word in sentence.lower() for word in action_words):
                if len(sentence) > 10:
                    action_items.append(sentence)

        # Limit to first 5 potential action items
        action_items = action_items[:5]

        # Create basic summary (first 500 characters)
        summary = transcription[:500] + "..." if len(transcription) > 500 else transcription

        return {
            "summary": summary,
            "action_items": action_items,
            "key_points": [],
            "participants": None
        }
