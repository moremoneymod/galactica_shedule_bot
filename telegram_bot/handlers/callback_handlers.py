import os
import aiogram.types
from aiogram import Router
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
import asyncio
import json
from utils import utils
from pathlib import Path

router = Router()


@router.callback_query(F.data == "select_group")
async def callback_query_handler(callback_query: aiogram.types.CallbackQuery) -> None:
    file = open(os.path.split(os.path.dirname(__file__))[0] + '/../groups.json', encoding='cp1251')
    study_groups = json.load(file)
    file.close()
    builder = InlineKeyboardBuilder()
    for group in study_groups:
        builder.button(text=group, callback_data=f"group_{group}")
    builder.button(text="Назад", callback_data='back_to_menu')
    builder.adjust(1, 1)
    await callback_query.message.edit_text("~~~ Выберите группу ~~~", reply_markup=builder.as_markup())


@router.callback_query(F.data == "back_to_menu")
async def callback_query_handler(callback_query: aiogram.types.CallbackQuery) -> None:
    builder = InlineKeyboardBuilder()
    builder.button(text="~~~ Выберите группу ~~~", callback_data="select_group")
    await callback_query.message.edit_text("~~~ Просмотр расписания ~~~", reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith('group_'))
async def callback_query_handler(callback_query: aiogram.types.CallbackQuery) -> None:
    await callback_query.message.delete()
    group = callback_query.data.replace('group_', '')
    builder = InlineKeyboardBuilder()
    for day in ["понедельник", "вторник", "среда", "четверг", "пятница"]:
        builder.button(text=day, callback_data=f"gr_{group}!d_{day}")
    builder.button(text="Назад", callback_data="back_to_menu")
    builder.adjust(1, 1)
    await callback_query.message.answer("~~~ Выберите день недели ~~~", reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("gr_"))
async def callback_query_handler(callback_query: aiogram.types.CallbackQuery) -> None:
    data = callback_query.data.split("!")
    group = data[0].replace("gr_", '')
    day = data[1].replace("d_", '')
    course = group.split('-')[1][0]

    f = open(os.path.split(os.path.dirname(__file__))[0] + '/../schedule.json', 'r', encoding='cp1251')
    json_data = json.load(f)
    f.close()

    builder = InlineKeyboardBuilder()
    lessons = json_data[group][day]

    f = open(os.path.split(os.path.dirname(__file__))[0] + '/../time.json', 'r', encoding='UTF-8')
    json_data1 = json.load(f)
    f.close()
    print(json_data1)
    time = json_data1[course]

    message = utils.create_lessons_message(day, lessons, time)

    print(json_data[group][day])
    builder.button(text="Назад", callback_data=f"group_{group}")
    builder.adjust(1, 1)
    await callback_query.message.edit_text(message, reply_markup=builder.as_markup())
