"""
Langgraph workflow for intent → initial steps and first prompt (T025).
No adaptation yet (US2 extends this).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ai.prompts.inspection_prompts import first_prompt_for_intent


@dataclass
class GraphState:
    """State for the inspection graph."""

    intent_goal: str
    intent_constraints: dict[str, Any] | None
    steps: list[dict[str, Any]]
    current_prompt: str | None
    done: bool


def run_initial_graph(goal: str, constraints: dict | None = None) -> tuple[list[dict[str, Any]], str]:
    """
    From intent, produce initial steps (one for MVP) and first prompt.
    Returns (steps, prompt_text).
    """
    prompt_text = first_prompt_for_intent(goal, constraints)
    # Single initial step for MVP
    steps = [
        {
            "id": "step-1",
            "order": 0,
            "type": "check",
            "prompt": prompt_text,
            "status": "pending",
        }
    ]
    return steps, prompt_text


def run_next_prompt(
    current_step_id: str,
    answer: str,
    steps: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, str, bool]:
    """
    Given answer for current step, return (completed_step, next_prompt_text, has_next).
    MVP: one step then done.
    """
    if not steps:
        return None, "No more steps.", False
    # Mark first step completed; no more steps in MVP
    completed = {**steps[0], "status": "completed"} if steps else None
    return completed, "", False
