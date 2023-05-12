from aiogram.dispatcher.filters.state import StatesGroup, State


class SupportQuestionState(StatesGroup):
    question = State()


class SupportAnswerState(StatesGroup):
    answer = State()
    

class ContextQuestionState(StatesGroup):
    question = State()


class SymptomsQuizState(StatesGroup):
    quiz = State()


class InstitutionState(StatesGroup):
    message_id = State()
