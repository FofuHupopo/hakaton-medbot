from aiogram import types
from aiogram.dispatcher import FSMContext, filters
from aiogram.types import ReplyKeyboardRemove

from bot import dp, bot, MESSAGES
from keyboards import admin_kb

from .filter import AdminFilter


@dp.message_handler(AdminFilter(), commands=['admin'])
async def admin_handler(message: types.Message):
    await message.reply(MESSAGES["admin"], reply_markup=admin_kb)


@dp.callback_query_handler(AdminFilter(), lambda cb: cb.data == "admin")
async def admin_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(MESSAGES["admin"], reply_markup=admin_kb)
