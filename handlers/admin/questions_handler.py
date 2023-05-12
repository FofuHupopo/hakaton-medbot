from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy.orm import Session

from bot import dp, bot, MESSAGES
from keyboards import admin_question_kb, cancel_btn
from models import UserModel, QuestionModel, engine
from states import AnswerState

from handlers.logic import update_link_to_appoinment
from .filter import AdminFilter


async def view_question(callback_query: types.CallbackQuery, question_id: int):
    with Session(engine) as session:
        is_answered = session.query(QuestionModel).filter(
            QuestionModel.id == question_id
        ).first().is_answered

        questions = session.query(QuestionModel).filter(
            QuestionModel.is_answered == is_answered
        ).all()

        count = len(questions)
        
        index = list(map(lambda x: x.id, questions)).index(question_id)

        text = MESSAGES["admin_question_detail"].format(questions[index].questioner_name, questions[index].question, questions[index].date)

        if questions[index].is_answered:
            text += MESSAGES["admin_question_answer"].format(questions[index].answer)
        
        kb = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=True)

        btns = []

        if index > 0:
            another_question_id = questions[index - 1].id
    
            btns.append(
                types.InlineKeyboardButton("<<<", callback_data=f"admin_view_question_{another_question_id}")
            )
            
        btns.append(
            types.InlineKeyboardButton(f"{index + 1}/{count}", callback_data=f"empty")
        )

        if index < count - 1:
            another_question_id = questions[index + 1].id

            btns.append(
                types.InlineKeyboardButton(">>>", callback_data=f"admin_view_question_{another_question_id}")
            )

        if not questions[index].is_answered:
            kb.add(
                types.InlineKeyboardButton("🗣 Ответить", callback_data=f"admin_answer_question_{question_id}")
            )

        kb.add(*btns)
        kb.add(
            types.InlineKeyboardButton("◀️ Назад", callback_data=f"admin_questions")
        )
        
        await callback_query.message.edit_text(text, reply_markup=kb)


@dp.callback_query_handler(AdminFilter(), lambda cb: cb.data == "admin_questions")
async def view_questions_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await callback_query.message.edit_text(MESSAGES["admin_questions"], reply_markup=admin_question_kb)


@dp.callback_query_handler(AdminFilter(), lambda cb: cb.data == "admin_view_questions")
async def view_questions_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    
    with Session(engine) as session:
        question = session.query(QuestionModel).filter(
            QuestionModel.is_answered == False
        ).first()

    if question:
        await view_question(callback_query, question.id)
        return

    kb = types.InlineKeyboardMarkup(resize_keyboard=True)
    kb.add(
        types.InlineKeyboardButton("◀️ Назад", callback_data="admin_questions")
    )

    await callback_query.message.edit_text(MESSAGES["admin_no_new_questions"], reply_markup=kb)


@dp.callback_query_handler(AdminFilter(), lambda cb: "admin_view_question_" in cb.data)
async def view_question_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    
    question_id = int(callback_query.data.replace("admin_view_question_", ""))
    
    await view_question(callback_query, question_id)


@dp.callback_query_handler(AdminFilter(), lambda cb: "admin_answer_question_" in cb.data)
async def start_answer_question_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    
    question_id = int(callback_query.data.replace("admin_answer_question_", ""))
    
    async with state.proxy() as data:
        data["question_id"] = question_id

    await AnswerState.answer.set()
    await bot.send_message(callback_query.from_user.id, "Введите текст ответа:")
    

@dp.message_handler(AdminFilter(), state=AnswerState.answer)
async def end_answer_question_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        answer = message.text
        question_id = data["question_id"]
    
    await state.finish()
    
    with Session(engine) as session:
        admin_id = session.query(UserModel).filter(
            UserModel.telegram_id == message.from_user.id
        ).first().id

        session.query(QuestionModel).filter(
            QuestionModel.id == question_id
        ).update({
            QuestionModel.defendant_id: admin_id,
            QuestionModel.answer: answer,
            QuestionModel.is_answered: True,
        })
        
        user_telegram_id = session.query(UserModel).join(
            QuestionModel, UserModel.id == QuestionModel.questioner_id
        ).filter(
            QuestionModel.id == question_id
        ).first().telegram_id
        
        session.commit()

    await bot.send_message(user_telegram_id, MESSAGES["you_have_answer"])

    kb = types.InlineKeyboardMarkup(resize_keyboard=True)
    kb.add(
       types. InlineKeyboardButton("◀️ Назад", callback_data="admin_questions")
    )
    
    await bot.send_message(message.from_user.id, MESSAGES["admin_answer_sended"], reply_markup=kb)


@dp.callback_query_handler(AdminFilter(), lambda cb: cb.data == "admin_answered_questions")
async def view_questions_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    
    with Session(engine) as session:
        question = session.query(QuestionModel).filter(
            QuestionModel.is_answered == True
        ).order_by(
            ~QuestionModel.id    
        ).first()

    if question:
        await view_question(callback_query, question.id)
    else:
        kb = types.InlineKeyboardMarkup(resize_keyboard=True)
        kb.add(
            types.InlineKeyboardButton("◀️ Назад", callback_data="admin_questions")
        )

        await callback_query.message.edit_text(MESSAGES["admin_no_question_history"], reply_markup=kb)
    