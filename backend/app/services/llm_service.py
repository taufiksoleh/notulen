import logging
from typing import Dict, List, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """
    Service for LLM-based post-processing (summaries, action items, key points)
    Supports both OpenAI and Anthropic
    """

    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self._initialize_clients()

    def _initialize_clients(self):
        """Initialize LLM clients based on available API keys"""
        try:
            if settings.OPENAI_API_KEY:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
                logger.info("OpenAI client initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize OpenAI client: {e}")

        try:
            if settings.ANTHROPIC_API_KEY:
                from anthropic import Anthropic
                self.anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
                logger.info("Anthropic client initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Anthropic client: {e}")

    def generate_summary_with_openai(self, transcription: str, language: str = "id") -> Dict:
        """Generate summary using OpenAI GPT-4"""
        if not self.openai_client:
            raise Exception("OpenAI client not initialized. Please set OPENAI_API_KEY.")

        prompt = self._create_summary_prompt(transcription, language)

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that summarizes meeting transcriptions and extracts action items."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1000
            )

            result_text = response.choices[0].message.content
            return self._parse_llm_response(result_text)

        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise

    def generate_summary_with_anthropic(self, transcription: str, language: str = "id") -> Dict:
        """Generate summary using Anthropic Claude"""
        if not self.anthropic_client:
            raise Exception("Anthropic client not initialized. Please set ANTHROPIC_API_KEY.")

        prompt = self._create_summary_prompt(transcription, language)

        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            result_text = response.content[0].text
            return self._parse_llm_response(result_text)

        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise

    def _create_summary_prompt(self, transcription: str, language: str) -> str:
        """Create prompt for summary generation"""
        lang_instruction = "in Indonesian" if language == "id" else "in English"

        return f"""Please analyze the following meeting transcription and provide:

1. A concise summary of the meeting (2-3 paragraphs) {lang_instruction}
2. A list of action items (tasks that need to be done)
3. Key discussion points

Transcription:
{transcription}

Please format your response as follows:

SUMMARY:
[Your summary here]

ACTION ITEMS:
- [Action item 1]
- [Action item 2]
- [etc...]

KEY POINTS:
- [Key point 1]
- [Key point 2]
- [etc...]
"""

    def _parse_llm_response(self, response_text: str) -> Dict:
        """Parse the LLM response into structured format"""
        try:
            summary = ""
            action_items = []
            key_points = []

            lines = response_text.strip().split('\n')
            current_section = None

            for line in lines:
                line = line.strip()

                if line.startswith("SUMMARY:"):
                    current_section = "summary"
                    continue
                elif line.startswith("ACTION ITEMS:"):
                    current_section = "action_items"
                    continue
                elif line.startswith("KEY POINTS:"):
                    current_section = "key_points"
                    continue

                if current_section == "summary" and line:
                    summary += line + " "
                elif current_section == "action_items" and line.startswith("-"):
                    action_items.append(line[1:].strip())
                elif current_section == "key_points" and line.startswith("-"):
                    key_points.append(line[1:].strip())

            return {
                "summary": summary.strip(),
                "action_items": action_items,
                "key_points": key_points
            }

        except Exception as e:
            logger.error(f"Failed to parse LLM response: {e}")
            return {
                "summary": response_text,
                "action_items": [],
                "key_points": []
            }

    def generate_summary(self, transcription: str, language: str = "id") -> Dict:
        """
        Generate summary using available LLM provider

        Returns dict with summary, action_items, and key_points
        """
        try:
            # Try OpenAI first, then Anthropic
            if self.openai_client:
                logger.info("Generating summary with OpenAI")
                return self.generate_summary_with_openai(transcription, language)
            elif self.anthropic_client:
                logger.info("Generating summary with Anthropic")
                return self.generate_summary_with_anthropic(transcription, language)
            else:
                # Fallback: simple summary without LLM
                logger.warning("No LLM client available, using simple summary")
                return self._generate_simple_summary(transcription)

        except Exception as e:
            logger.error(f"Summary generation failed: {e}")
            # Return simple fallback
            return self._generate_simple_summary(transcription)

    def _generate_simple_summary(self, transcription: str) -> Dict:
        """Simple summary when no LLM is available"""
        # Basic summary: first 500 characters
        summary = transcription[:500] + "..." if len(transcription) > 500 else transcription

        return {
            "summary": summary,
            "action_items": [],
            "key_points": []
        }

    def is_available(self) -> bool:
        """Check if any LLM client is available"""
        return self.openai_client is not None or self.anthropic_client is not None


# Global instance
llm_service = LLMService()
