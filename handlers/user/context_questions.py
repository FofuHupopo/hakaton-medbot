from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy.orm import Session

from bot import dp, bot, MESSAGES
from keyboards import cancel_kb, context_kb
from models import ContextAnswerModel, engine
from states import ContextQuestionState

from .main_handlers import menu_callback
from handlers.logic import lemmatize


@dp.callback_query_handler(lambda cb: cb.data == "context_question")
async def context_question_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    
    await ContextQuestionState.question.set()
    
    await callback_query.message.edit_text(MESSAGES["enter_context_question"], reply_markup=cancel_kb)
    

@dp.callback_query_handler(lambda cb: cb.data == "cancel", state=ContextQuestionState.question)
async def cancel_context_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await menu_callback(callback_query)
    

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=ContextQuestionState.question)
async def context_question_handler(message: types.Message, state: FSMContext):
    await state.finish()
    
    lemmas = lemmatize(message.text)

    with Session(engine) as session:
        context_answers = session.query(ContextAnswerModel).all()

    text_message = MESSAGES["sorry_we_cant_answer"]
    
    answers = []

    for answer in context_answers:
        for lemma in lemmas:
            if lemma in answer.get_keywords():
                answers.append(answer.answer)
                break
    
    if answers:
        if len(answers) == 1:
            text_message = MESSAGES["context_answer_one"].format(answers[0])
        else:
            text_message = MESSAGES["context_answer_many"].format(
                "\n".join(answers)
            )
        
    await bot.send_message(message.from_user.id, text_message, reply_markup=context_kb)
