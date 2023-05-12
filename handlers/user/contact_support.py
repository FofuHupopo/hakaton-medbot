from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy.orm import Session

from bot import dp, bot, MESSAGES
from keyboards import cancel_kb, support_kb
from models import QuestionModel, UserModel, engine
from states import SupportQuestionState

from handlers.logic import notify_administration


@dp.callback_query_handler(lambda cb: cb.data == "contact_support")
async def contact_support_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(MESSAGES["contact_support"], reply_markup=support_kb)


# View questions and answers

async def view_my_question(callback_query: types.CallbackQuery, question_id):
    with Session(engine) as session:
        is_answered = session.query(QuestionModel).filter(
            QuestionModel.id == question_id
        ).first().is_answered

        questions = session.query(QuestionModel).join(
            UserModel, UserModel.id == QuestionModel.questioner_id    
        ).filter(
            QuestionModel.is_answered == is_answered,
            UserModel.telegram_id == callback_query.from_user.id
        ).all()

        questions_count = len(questions)
        
        question_index = list(map(lambda x: x.id, questions)).index(question_id)
        question = questions[question_index]

        text = "Вопрос:\n" + question.question
        
        if question.is_answered:
            text += "\n\nОтвет поддержки:\n" + question.answer
        
        keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=True)
        btns = []

        if question_index > 0:
            another_question_id = questions[question_index - 1].id
    
            btns.append(
                types.InlineKeyboardButton("<<<", callback_data=f"view_my_question_{another_question_id}")
            )
        
        btns.append(
            types.InlineKeyboardButton(f"{question_index + 1}/{questions_count}", callback_data="empty")
        )

        if question_index + 1 < questions_count:
            another_question_id = questions[question_index + 1].id

            btns.append(
                types.InlineKeyboardButton(">>>", callback_data=f"view_my_question_{another_question_id}")
            )

        keyboard.add(*btns)
        keyboard.add(
            types.InlineKeyboardButton("◀️ Назад", callback_data=f"contact_support")
        )
        
        await callback_query.message.edit_text(text, reply_markup=keyboard)


async def get_first_question_id(callback_query: types.CallbackQuery, is_answered: bool):
    with Session(engine) as session:
        question = session.query(QuestionModel).join(
            UserModel, UserModel.id == QuestionModel.questioner_id    
        ).filter(
            QuestionModel.is_answered == is_answered,
            UserModel.telegram_id == callback_query.from_user.id
        ).order_by(
            not QuestionModel.id
        ).first()

    if question:
        await view_my_question(callback_query, question.id)
        return
    
    go_back_kb = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    go_back_kb.add(
        types.InlineKeyboardButton("◀️ Назад", callback_data="contact_support")
    )

    if is_answered:
        await callback_query.message.edit_text(MESSAGES["no_answers"], reply_markup=go_back_kb)
    else:
        await callback_query.message.edit_text(MESSAGES["no_questions"], reply_markup=go_back_kb)


@dp.callback_query_handler(lambda cb: cb.data == "my_questions")
async def my_questions_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    
    await get_first_question_id(callback_query, False)


@dp.callback_query_handler(lambda cb: cb.data == "my_answers")
async def my_answers_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    
    await get_first_question_id(callback_query, True)


@dp.callback_query_handler(lambda cb: "view_my_question_" in cb.data)
async def view_my_question_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    
    question_id = int(callback_query.data.replace("view_my_question_", ""))
    
    await view_my_question(callback_query, question_id)



@dp.callback_query_handler(lambda cb: cb.data == "ask_question")
async def ask_question_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    
    await callback_query.message.edit_text(MESSAGES["ask_question"], reply_markup=cancel_kb)
    await SupportQuestionState.question.set()
    

@dp.callback_query_handler(lambda cb: cb.data == "cancel", state=SupportQuestionState.question)
async def cancel_ask_question_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await contact_support_callback(callback_query)


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=SupportQuestionState.question)
async def send_question_handler(message: types.Message, state: FSMContext):
    await state.finish()
    
    with Session(engine) as session:
        user_id = session.query(UserModel).filter(
            UserModel.telegram_id == message.from_user.id
        ).first().id
        
        question = QuestionModel(
            questioner_name=message.from_user.full_name,
            questioner_id=user_id,
            question=message.text
        )
        
        session.add(question)
        session.commit()

    await notify_administration(MESSAGES["new_question"])

    kb = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    kb.add(
        types.InlineKeyboardButton("◀️ Назад", callback_data="contact_support")
    )

    await bot.send_message(message.from_user.id, MESSAGES["question_sended"], reply_markup=kb)
