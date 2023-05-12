from aiogram import types

from bot import dp, bot, MESSAGES

from keyboards import go_menu_kb
from handlers.logic import get_link_to_appointment, notify_administration


@dp.callback_query_handler(lambda cb: cb.data == "make_appointment")
async def make_appointment_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    
    link = get_link_to_appointment()
    message = MESSAGES["make_appointment"] + "\n" + link
    
    kb = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    kb.add(
        types.InlineKeyboardButton(
            "🤚 Попросить обновить ссылку",
            callback_data="please_update_appointment_link"
        ),
        types.InlineKeyboardButton("◀️ Назад", callback_data="menu"),
    )
    
    await callback_query.message.edit_text(message, reply_markup=kb)



@dp.callback_query_handler(lambda cb: cb.data == "please_update_appointment_link")
async def please_update_appointment_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    
    await notify_administration(MESSAGES["please_update_link"])
    
    await callback_query.message.edit_text(MESSAGES["request_sended"], reply_markup=go_menu_kb)
