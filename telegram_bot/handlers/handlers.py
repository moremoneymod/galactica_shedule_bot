from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.message(Command('start'))
async def command_start_handler(message: Message) -> None:
    await message.answer("Данный бот предназначен для просмотра расписания в колледже 'Галактика' "
                         "Чтобы воспользоваться ботом, нужно отправить команду !!! /schedule !!! "
                         "или выбрать ее в меню в левом нижнем углу")


@router.message(Command('help'))
async def command_help(message: Message) -> None:
    await message.answer("Чтобы воспользоваться ботом, нужно отправить боту команду '/schedule' или "
                         "выбрать соответствующую команду в меню бота в левом нижнем углу")


@router.message(Command('schedule'))
async def command_articles(message: Message) -> None:
    builder = InlineKeyboardBuilder()
    builder.button(text="Выбрать группу", callback_data="select_group")
    await message.answer("~~~ Просмотр расписания ~~~", reply_markup=builder.as_markup())
