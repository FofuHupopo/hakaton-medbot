from aiogram import types
from aiogram.dispatcher import FSMContext
from itertools import chain
from sqlalchemy.orm import Session

from bot import dp, bot, MESSAGES
from keyboards import information_kb, go_information_btn
from states import InstitutionState
from models import EmployeeModel, InstitutionModel, engine


@dp.callback_query_handler(lambda cb: cb.data == "information")
async def information_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(MESSAGES["information"], reply_markup=information_kb)
    

# Contact information

@dp.callback_query_handler(lambda cb: cb.data == "contact_information")
async def contact_information_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    
    kb = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    kb.add(
        go_information_btn
    )
    
    await callback_query.message.edit_text(MESSAGES["contact_information"], reply_markup=kb)


# Employess information

async def view_employees_list(callback_query: types.CallbackQuery, page=0, count=10):
    with Session(engine) as session:
        all_employees = session.query(EmployeeModel).all()
    
    employees_count = len(all_employees)
    employees = all_employees[page * count:(page + 1) * count]
    
    max_page = (employees_count + count - 1) // count
    
    kb = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    kb.add(*[
        types.InlineKeyboardButton(
            employee.fullname,
            callback_data=f"employee_detail_{employee.id}"
        )
        for employee in employees  
    ])
    
    move_btns = []
    if page > 0:
        move_btns.append(
            types.InlineKeyboardButton("<<<", callback_data=f"employees_information{page - 1}")
        )
    
    move_btns.append(
        types.InlineKeyboardButton(f"{page + 1}/{max_page}", callback_data="empty")
    )

    if page + 1 < max_page:
        move_btns.append(
            types.InlineKeyboardButton(">>>", callback_data=f"employees_information{page + 1}")
        )

    kb.row(*move_btns)
    kb.row(
        types.InlineKeyboardButton("◀️ Назад", callback_data=f"information")
    )
    
    await callback_query.message.edit_text(MESSAGES["employees_list"], reply_markup=kb)


async def view_employee_detail(callback_query: types.CallbackQuery, employee_id: int):
    with Session(engine) as session:
        all_employees = session.query(EmployeeModel).all()
        employee: EmployeeModel = session.query(EmployeeModel).get({"id": employee_id})
    
    text = MESSAGES["employee_detail"].format(
        f"👨‍🦱 ФИО: {employee.fullname}\n"
        f"🦺 Должность: {employee.position}\n"
        f"☎️ Телефон: {employee.phone}\n"
        f"📧 E-mail: {employee.email}\n"
        f"🌆 Город: {employee.city}\n"
        f"🏢 Филиал: {employee.branch}\n"
        f"🏘 Адрес: {employee.address}\n"
        f"ℹ️ Доп. информация:\n{employee.additional_info}\n"
    )
    
    page = (all_employees.index(employee) + 9) // 10 - 1
    
    kb = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    kb.add(
        types.InlineKeyboardButton("◀️ Назад", callback_data=f"employees_information{page}")
    )
    
    await callback_query.message.edit_text(text, reply_markup=kb)


@dp.callback_query_handler(lambda cb: "employees_information" in cb.data)
async def employees_information_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    
    page = callback_query.data.replace("employees_information", "")

    if not page:
        page = 0
    
    await view_employees_list(callback_query, int(page))


@dp.callback_query_handler(lambda cb: "employee_detail_" in cb.data)
async def employee_detail_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    employee_id = int(callback_query.data.replace("employee_detail_", ""))
    
    await view_employee_detail(callback_query, employee_id)


# Institutions information

@dp.callback_query_handler(lambda cb: cb.data == "institutions_information")
async def institutions_information_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    
    with Session(engine) as session:
        cities = list(chain(*session.query(InstitutionModel.city).distinct().all()))
    
    kb = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    kb.add(*[
        types.InlineKeyboardButton(city, callback_data=f"institution_city_{city}")
        for city in cities
    ])
    kb.add(
        types.InlineKeyboardButton("◀️ Назад", callback_data="information")
    )
    
    await callback_query.message.edit_text(MESSAGES["institutions_information_city"], reply_markup=kb)


@dp.callback_query_handler(lambda cb: "institution_city_" in cb.data)
async def institutions_city_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    city = callback_query.data.replace("institution_city_", "")
    
    with Session(engine) as session:
        institutions = session.query(InstitutionModel).filter(InstitutionModel.city == city)
    
    kb = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    kb.add(*[
        types.InlineKeyboardButton(institution.name, callback_data=f"view_institution_{institution.id}")
        for institution in institutions
    ])
    kb.add(
        types.InlineKeyboardButton("◀️ Назад", callback_data="institutions_information")
    )
    
    await callback_query.message.edit_text(MESSAGES["institutions_information_institution"], reply_markup=kb)


@dp.callback_query_handler(lambda cb: "institution_city_" in cb.data, state=InstitutionState)
async def institutions_city_go_back_callback(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        message_id = data["message_id"]
    
    await state.finish()
    await bot.delete_message(callback_query.from_user.id, message_id)
    
    await institutions_city_callback(callback_query)


@dp.callback_query_handler(lambda cb: "view_institution_" in cb.data)
async def view_institution_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    
    institution_id = callback_query.data.replace("view_institution_", "")
    
    with Session(engine) as session:
        institution = session.query(InstitutionModel).filter(
            InstitutionModel.id == institution_id
        ).first()

    text = MESSAGES["institution_information"].format(
        f"Наименование учреждения:\n{institution.name}\n"
        f"Город:\n{institution.city}\n"
        f"Адрес:\n{institution.address}\n"
        f"График работы:\n{institution.schedule}\n"
    )

    kb = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    kb.add(
        types.InlineKeyboardButton("◀️ Назад", callback_data=f"institution_city_{institution.city}")
    )

    await callback_query.message.edit_text(text, reply_markup=kb)
    message = (await bot.send_location(callback_query.from_user.id, institution.lat, institution.lon))

    await InstitutionState.message_id.set()
    async with state.proxy() as data:
        data["message_id"] = message["message_id"]
