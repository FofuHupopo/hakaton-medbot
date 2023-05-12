from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy.orm import Session

from bot import dp, bot, MESSAGES
from keyboards import cancel_btn, quiz_kb, cancel_kb
from models import QuizQuestionModel, DiseaseBySymptomsModel, engine
from states import SymptomsQuizState

from handlers.logic import get_link_to_appointment


@dp.callback_query_handler(lambda cb: cb.data == "symptoms")
async def symptoms_quiz_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(MESSAGES["lets_start_quiz"], reply_markup=quiz_kb)
    
    
async def get_quiz_question(callback_query: types.CallbackQuery, question_id: int):
    with Session(engine) as session:
        questions = session.query(QuizQuestionModel).all()
    
    questions_count = len(questions)
    question_index = list(map(lambda q: q.id, questions)).index(question_id)
    
    question = questions[question_index]
    
    text_message = MESSAGES["quiz_question"].format(question_index + 1, questions_count, question.question.strip())
    
    kb = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    kb.add(
        types.InlineKeyboardButton("Да", callback_data=f"yes_symptom_{question_id}"),
        types.InlineKeyboardButton("Нет", callback_data=f"no_symptom_{question_id}"),
        cancel_btn
    )
    
    await callback_query.message.edit_text(text_message, reply_markup=kb)
    

@dp.callback_query_handler(lambda cb: cb.data == "start_quiz")
async def start_symptoms_quiz_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await SymptomsQuizState.quiz.set()

    with Session(engine) as session:
        question = session.query(QuizQuestionModel).first()

    if question:
        await get_quiz_question(callback_query, question.id)
        return
    
    text_message = MESSAGES["no_quiz"].format(get_link_to_appointment())

    await callback_query.message.edit_text(text_message, reply_markup=cancel_kb)


@dp.callback_query_handler(lambda cb: cb.data == "cancel", state=SymptomsQuizState.quiz)
async def start_symptoms_quiz_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await symptoms_quiz_callback(callback_query)


@dp.callback_query_handler(lambda cb: "_symptom_" in cb.data, state=SymptomsQuizState.quiz)
async def start_symptoms_quiz_callback(callback_query: types.CallbackQuery, state: FSMContext):
    quiz_question_id = int(callback_query.data.split("_")[-1])
    availability = "yes" in callback_query.data
    
    with Session(engine) as session:
        questions = session.query(QuizQuestionModel).all()
    
    questions_count = len(questions)
    question_index = list(map(lambda q: q.id, questions)).index(quiz_question_id)

    async with state.proxy() as data:
        if "symptoms" not in data:
            data["symptoms"] = set()


        if "symptoms" in data and availability:
            data["symptoms"].add(questions[question_index].symptom)
            
    if question_index + 1 < questions_count:
        await get_quiz_question(callback_query, questions[question_index + 1].id)
        return

    kb = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    kb.add(
        types.InlineKeyboardButton("🏁 Перейти к результату", callback_data="quiz_result"),
        cancel_btn
    )
    
    await callback_query.message.edit_text(MESSAGES["end_quiz"], reply_markup=kb)
    
    
@dp.callback_query_handler(lambda cb: cb.data == "quiz_result", state=SymptomsQuizState.quiz)
async def quiz_result_callback(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        symptoms = set(data["symptoms"])
    
    await state.finish()
    
    with Session(engine) as session:
        diseases = session.query(DiseaseBySymptomsModel).all()
    
    user_diseases_list = list()
    
    for disease in diseases:
        if symptoms.issubset(disease.get_symptoms()):
            user_diseases_list.append(disease.disease)
            
    link = get_link_to_appointment()
    text_message = MESSAGES["quiz_result_no_disease"].format(link)

    if user_diseases_list:
        if len(user_diseases_list) == 1:
            text_message = MESSAGES["quiz_result_one_disease"].format(user_diseases_list[0], link)
        else:
            text_message = MESSAGES["quiz_result_many_dieseases"].format("\n".join(user_diseases_list), link)
        
    kb = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    kb.add(
        types.InlineKeyboardButton("◀️ Назад", callback_data="symptoms")
    )

    await callback_query.message.edit_text(text_message, reply_markup=kb)
