"""
Prompt generation: one question at a time (T026). Wired to graph.
"""
from __future__ import annotations


def first_prompt_for_intent(goal: str, constraints: dict | None = None) -> str:
    """Generate first prompt from intent goal."""
    if not goal or not goal.strip():
        return "What would you like to inspect? Please describe your goal."
    return f"Your goal is: {goal}. What is the first thing you want to check?"


def next_prompt_from_answer(step_prompt: str, answer: str) -> str:
    """Generate next prompt (simplified: can be replaced by LLM)."""
    return "What would you like to check next?"
