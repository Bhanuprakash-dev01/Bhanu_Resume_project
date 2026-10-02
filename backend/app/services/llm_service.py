from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


class LLMService:
    def __init__(self, model: Optional[str] = None, api_key: Optional[str] = None) -> None:
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def generate(self, prompt: str, system_prompt: str = "You are a helpful AI assistant.") -> str:
        if not self.client:
            return self._fallback_response(prompt)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
            )
            return response.choices[0].message.content or "No response returned."
        except Exception:
            return self._fallback_response(prompt)

    def _fallback_response(self, prompt: str) -> str:
        lower = prompt.lower()
        if "refund" in lower:
            return "A refund request is supported only after policy review and human approval."
        if "delay" in lower or "late" in lower:
            return "The delivery delay should be investigated using carrier status, order details, and company policy."
        if "tracking" in lower:
            return "Tracking details need to be checked before confirming any delivery issue."
        return "This request has been routed through the agent workflow for policy-grounded review."


llm_service = LLMService()
