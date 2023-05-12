from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import dp, bot, MESSAGES
from keyboards import cancel_kb
from states import UpdateLinkState

from handlers.logic import update_link_to_appoinment
from .filter import AdminFilter
from .admin import admin_callback


@dp.callback_query_handler(AdminFilter(), lambda cb: cb.data == "admin_update_link")
async def admin_update_link_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await UpdateLinkState.new_link.set()
    
    await callback_query.message.edit_text(MESSAGES["admin_update_link"], reply_markup=cancel_kb)
    

@dp.callback_query_handler(AdminFilter(), lambda cb: cb.data == "cancel", state=UpdateLinkState.new_link)
async def admin_cancel_update_link_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await admin_callback(callback_query)


@dp.message_handler(AdminFilter(), content_types=types.ContentTypes.TEXT, state=UpdateLinkState.new_link)
async def admin_new_link_handler(message: types.Message, state: FSMContext):
    await state.finish()
    
    update_link_to_appoinment(message.text)
    
    text_message = MESSAGES["admin_finish_update_link"].format(message.text)
    
    kb = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    kb.add(
        types.InlineKeyboardButton("◀️ Назад", callback_data="admin")
    )
    
    await bot.send_message(message.from_user.id, text_message, reply_markup=kb)
