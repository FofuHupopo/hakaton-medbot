from aiogram.dispatcher import FSMContext, filters
from aiogram.types import ReplyKeyboardRemove

from .filter import AdminFilter
from bot import dp, bot, MESSAGES
from aiogram import types


@dp.message_handler(AdminFilter(), commands=['admin'])
async def admin_handler(message: types.Message):
    await message.reply(MESSAGES["admin"])


@dp.callback_query_handler(lambda cb: cb.data == "admin")
async def admin_callback(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(MESSAGES["admin"])
