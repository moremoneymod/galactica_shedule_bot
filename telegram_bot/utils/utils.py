from typing import Dict
from aiogram import types


def create_lessons_message(day: str, lessons: Dict) -> str:
    message = f"<b>{day.upper()}</b>\n\n"
    for lesson in lessons.items():
        message += f"<b>{lesson[0]}</b>  {lesson[1]}\n\n"
    print(message)
    return message
