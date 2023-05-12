from aiogram import types
from sqlalchemy.orm import Session

from bot import dp, bot, MESSAGES
from models import UserModel, engine
from keyboards import go_admin_btn

from .filter import AdminFilter


@dp.callback_query_handler(AdminFilter(), lambda cb: cb.data == "admin_notifications")
async def admin_notifications_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    
    with Session(engine) as session:
        user = session.query(UserModel).filter(
            UserModel.telegram_id == callback_query.from_user.id
        ).first()

    kb = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    
    if user.enable_notifications:
        kb.add(
            types.InlineKeyboardButton("🔕 Отключить", callback_data="admin_change_notifications")
        )
    else:
        kb.add(
            types.InlineKeyboardButton("🔔 Включить", callback_data="admin_change_notifications")
        )
        
    kb.add(
        go_admin_btn
    )
    
    await callback_query.message.edit_text(MESSAGES["admin_notifications"], reply_markup=kb)


@dp.callback_query_handler(AdminFilter(), lambda cb: cb.data == "admin_change_notifications")
async def admin_change_notifications_callback(callback_query: types.CallbackQuery):
    with Session(engine) as session:
        notification_status = session.query(UserModel).filter(
            UserModel.telegram_id == callback_query.from_user.id
        ).first().enable_notifications

        session.query(UserModel).filter(
            UserModel.telegram_id == callback_query.from_user.id
        ).update({
            UserModel.enable_notifications: not notification_status
        })

        session.commit()
    
    await admin_notifications_callback(callback_query)
