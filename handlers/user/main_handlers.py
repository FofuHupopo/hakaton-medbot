from aiogram import types

from bot import dp, bot, MESSAGES
from keyboards import menu_kb, go_menu_kb

from handlers.filter import NewUserFilter


@dp.message_handler(NewUserFilter(), commands=['start'])
async def start_handler(message: types.Message):
    await message.reply(MESSAGES["start"], reply_markup=menu_kb)


@dp.message_handler(NewUserFilter(), commands=["menu"])
async def menu_handler(message: types.Message):
    await message.reply(MESSAGES["menu"], reply_markup=menu_kb)


@dp.message_handler(NewUserFilter(), commands=["help"])
async def help_handler(message: types.Message):
    await message.reply(MESSAGES["help"], reply_markup=go_menu_kb)


@dp.callback_query_handler(lambda cb: cb.data == "menu")
async def menu_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(MESSAGES["menu"], reply_markup=menu_kb)


@dp.callback_query_handler(lambda cb: cb.data == "help")
async def help_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(MESSAGES["help"], reply_markup=go_menu_kb)


@dp.callback_query_handler(lambda cb: cb.data == "empty")
async def empty_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
