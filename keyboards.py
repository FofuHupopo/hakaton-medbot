from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton
)


go_menu_btn = InlineKeyboardButton("◀️ Назад", callback_data="menu")
go_admin_btn = InlineKeyboardButton("◀️ Назад", callback_data="admin")
cancel_btn = InlineKeyboardButton("❌ Отмена", callback_data="cancel")
go_information_btn = InlineKeyboardButton("◀️ Назад", callback_data="information")


menu_kb = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
menu_kb.add(
    InlineKeyboardButton("📋 Записаться к врачу", callback_data="make_appointment"),
    InlineKeyboardButton("❤ Симптомы", callback_data="symptoms"),
    InlineKeyboardButton("❔ Задать вопрос", callback_data="context_question"),
    InlineKeyboardButton("ℹ Информация", callback_data="information"),
    InlineKeyboardButton("☎ Обратиться в поддержку", callback_data="contact_support"),
    InlineKeyboardButton("📍 Помощь", callback_data="help")
)


go_menu_kb = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
go_menu_kb.add(
    go_menu_btn
)


cancel_kb = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
cancel_kb.add(
    cancel_btn
)


support_kb = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
support_kb.add(
    InlineKeyboardButton("❔ Мои вопросы", callback_data="my_questions"),
    InlineKeyboardButton("📋 Ответы", callback_data="my_answers"),
    InlineKeyboardButton("✏️ Задать вопрос", callback_data="ask_question"),
    go_menu_btn
)


context_kb = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
context_kb.add(
    InlineKeyboardButton("❔ Спросить еще", callback_data="context_question"),
    go_menu_btn
)


quiz_kb = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
quiz_kb.add(
    InlineKeyboardButton("🎌 Начать", callback_data="start_quiz"),
    go_menu_btn
)


information_kb = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
information_kb.add(
    InlineKeyboardButton("🏣 Об учреждениях", callback_data="institutions_information"),
    InlineKeyboardButton("👨 О сотрудниках", callback_data="employees_information"),
    InlineKeyboardButton("📞 Контактная информация", callback_data="contact_information"),
    go_menu_btn
)


admin_kb = InlineKeyboardMarkup(row_width=1, resize_keyboards=True)
admin_kb.add(
    InlineKeyboardButton("❔ Вопросы пользователей", callback_data="admin_questions"),
    InlineKeyboardButton("🔗 Обновить ссылку", callback_data="admin_update_link"),
    InlineKeyboardButton("🔔 Уведомления", callback_data="admin_notifications")
)


admin_question_kb = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
admin_question_kb.add(
    InlineKeyboardButton("💌 Новые вопросы", callback_data="admin_view_questions"),
    InlineKeyboardButton("📝 История вопросов", callback_data="admin_answered_questions"),
    go_admin_btn
)
