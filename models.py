import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float, func
)

import json


Base = declarative_base()


class UnregisteredMessageModel(Base):
    __tablename__ = "unregistered_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer)
    message = Column(Text)
    date = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer)
    is_admin = Column(Boolean, default=False)
    enable_notifications = Column(Boolean, default=True)
    join_date = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


class QuestionModel(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)

    questioner_name = Column(String(255), nullable=False)
    questioner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    question = Column(Text, nullable=False)

    defendant_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    answer = Column(Text, nullable=True)
    is_answered = Column(Boolean, default=False)

    date = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    
    
class ContextAnswerModel(Base):
    __tablename__ =  "context_answers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    keywords_set = Column(Text)
    answer = Column(Text)

    def set_keywords(self, keywords_set: set):
        self.keywords_set = json.dumps(list(keywords_set), ensure_ascii=False).encode("utf-8")

    def get_keywords(self) -> frozenset:
        return frozenset(json.loads(self.keywords_set)) if self.keywords_set else {}
    

class QuizQuestionModel(Base):
    __tablename__ = "quiz_questions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(Text)
    symptom = Column(String(127))


class DiseaseBySymptomsModel(Base):
    __tablename__ = "disease_by_symptoms"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    disease = Column(String(127))
    symptoms_set = Column(Text)
    
    def set_symptoms(self, symptoms_set: set):
        self.symptoms_set = json.dumps(list(symptoms_set), ensure_ascii=False).encode("utf-8")

    def get_symptoms(self) -> frozenset:
        return frozenset(json.loads(self.symptoms_set)) if self.symptoms_set else {}
    

class EmployeeModel(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    fullname = Column(String(63))
    position = Column(String(63))
    phone = Column(String(20))
    email = Column(String(63))

    city = Column(String(63))
    branch = Column(String(63))
    address = Column(String(215))

    additional_info = Column(Text)
    

class InstitutionModel(Base):
    __tablename__ = "institutions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    name = Column(String(127))
    schedule = Column(String(127))
    
    city = Column(String(63))
    address = Column(String(215))

    lat = Column(Float)
    lon = Column(Float)


DEFAULT_DB_PATH = "sqlite:///data/temp.db"
DB_PATH = os.environ.get("DB_PATH", DEFAULT_DB_PATH)

if DB_PATH == DEFAULT_DB_PATH:
    print(
        "WARNING! Вы используете базу данных по умолчанию. "
        "Для подключения другой используйте команду 'export DB_PATH=\"...\"' или 'SET DB_PATH=\"...\"'"
    )

engine = create_engine(DB_PATH)

Base.metadata.create_all(engine)
