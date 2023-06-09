from sqlalchemy.orm import sessionmaker
from faker import Faker

from models import (
    QuizQuestionModel, EmployeeModel, DiseaseBySymptomsModel,
    ContextAnswerModel, InstitutionModel, engine
)


Session = sessionmaker(bind=engine)
session = Session()


def diseases_generator():
    diseases = {
        "Грипп": ["головная боль", "насморк/заложенность носа", "боль в горле", "мышечная боль", "повышенная температура тела", "усталость/слабость", "кашель"],
        "ОРВИ":  ["головная боль", "насморк/заложенность носа", "боль в горле", "кашель", "повышенная температура тела", "усталость/слабость"],
        "Ангина": ["головная боль", "боль в горле", "повышенная температура тела", "усталость/слабость"],
        "Стрептодерма": ["головная боль", "кашель", "боль в горле", "повышенная температура тела", "усталость/слабость"],
        "Синусит": ["головная боль", "насморк/заложенность носа", "мышечная боль", "повышенная температура тела"],
        "Бронхит": ["кашель", "проблемы с дыханием", "повышенная температура тела", "усталость/слабость"],
        "Пневмония": ["кашель", "проблемы с дыханием", "повышенная температура тела", "усталость/слабость"],
        "Астма": ["кашель", "проблемы с дыханием", "усталость/слабость"],
        "Бронхиальная астма": ["кашель", "проблемы с дыханием", "усталость/слабость"],
        "Эмфизема легких": ["проблемы с дыханием", "усталость/слабость"],
        "Гепатит А": ["проблемы со ЖКТ", "повышенная температура тела", "усталость/слабость"],
        "Гепатит В": ["проблемы со ЖКТ", "повышенная температура тела", "усталость/слабость"],
        "Гепатит С": ["проблемы со ЖКТ", "повышенная температура тела", "усталость/слабость"],
        "Язва желудка": ["проблемы со ЖКТ", "боль в животе", "тошнота"],
        "Язва двенадцатиперстной кишки": ["проблемы со ЖКТ", "боль в животе", "тошнота"],
        "Нарушение моторики желудка": ["проблемы со ЖКТ", "боль в животе", "тошнота"],
        "Гастрит": ["проблемы со ЖКТ", "боль в животе", "тошнота"],
        "Панкреатит": ["проблемы со ЖКТ", "боль в животе", "тошнота"],
        "Колит": ["проблемы со ЖКТ", "боль в животе", "диарея"],
        "Дизентерия": ["проблемы со ЖКТ", "боль в животе", "диарея"],
        "Холера": ["проблемы со ЖКТ", "боль в животе", "диарея"],
        "Сепсис": ["головокружения", "насморк/заложенность носа", "боль в горле", "мышечная боль", "повышенная температура тела", "усталость/слабость", "проблемы с дыханием"],
        "Лимфома": ["головная боль", "усталость/слабость", "боль в шее"],
        "Анемия": ["усталость/слабость", "головокружения", "боли в мышцах"]
    }
    
    for disease, symptoms in diseases.items():
        d = DiseaseBySymptomsModel(disease=disease)
        d.set_symptoms(symptoms)
        
        session.add(d)


def employees_generator():
    fake = Faker()

    for _ in range(40):
        employee = EmployeeModel(
            fullname=fake.name(),
            position=fake.job(),
            phone=fake.phone_number(),
            email=fake.email(),
            city=fake.city(),
            branch=fake.company(),
            address=fake.address(),
            additional_info=fake.text()
        )
        session.add(employee)


def question_symptoms_generator():
    questions_symptoms = [
        ("Вы испытываете головную боль?", "головная боль"),
        ("У вас есть насморк или заложенность носа?", "насморк/заложенность носа"),
        ("Ваше горло болит?", "боль в горле"),
        ("У вас болят или ноют мышцы?", "мышечная боль"),
        ("Вы испытываете боли в животе?", "боль в животе"),
        ("Есть у вас повышенная температура тела?", "повышенная температура тела"),
        ("У вас есть кашель?", "кашель"),
        ("Бывают ли у вас проблемы с дыханием?", "проблемы с дыханием"),
        ("Вы чувствуете усталость или слабость?", "усталость/слабость"),
        ("Вы испытываете тошноту?", "тошнота"),
        ("У вас есть тошнота, рвота или другие проблемы со стулом?", "проблемы со ЖКТ"),
        ("У вас бывают головокружения?", "головокружения"),
    ]

    for question, symptom in questions_symptoms:
        session.add(
            QuizQuestionModel(
                question=question,
                symptom=symptom
            )
        )
        
        
def context_questions_generator():
    context_questions = [
        ('Запись на прием к нужному врачу осуществляется через регистратуру или сайт госуслуг.', ["записаться", "прием", "врач", "время"]),
        ('Результаты анализов следует принести на прием к врачу.', ["результаты", "исследования"]),
        ('Медицинские процедуры и анализы могут быть проведены в один день.', ["анализы", "медицинские процедуры", "день"]),
        ('Для записи на консультацию и ожидания операции необходимо обратиться в регистратуру.', ["операция", "консультация", "время ожидания"]),
        ('При наличии страховки ОМС, все услуги будут покрыты.', ["страховка", "услуги", "покрытие"]),
        ('Программы реабилитации и список доступных услуг можно узнать в регистратуре.', ["реабилитация", "программа", "услуги", "расположение"]),
        ('Рентгеновские исследования абсолютно безопасны для здоровья.', ["рентген", "безопасность"]),
    ]
    
    for answer, keywords in context_questions:
        ca = ContextAnswerModel(
            answer=answer
        )
        ca.set_keywords(keywords)
        
        session.add(ca)
        

def institutions_generator():
    institutions = [
        {"name": "Клиника «Медикана плюс»", "city": "Орск", "address": "пр-кт Мира, д. 6а", "schedule": "с 8:00 до 20:00", "lat": "51.230947", "lon": "58.504858"},
        {"name": "Медицинский центр «ЦМД»", "city": "Орск", "address": "пр-кт Ленина, д. 36", "schedule": "с 7:30 до 20:00", "lat": "51.232802", "lon": "58.474136"},
        {"name": "МДЦ имени Войно-Ясенецкого", "city": "Орск", "address": "ул. Суворова, д. 25", "schedule": "с 8:00 до 21:00", "lat": "51.235267", "lon": "58.469725"},
        {"name": "Стоматология «Дента-Люкс»", "city": "Новотроицк", "address": "ул. Уметбаева, д. 3а", "schedule": "с 8:00 до 20:00", "lat": "51.210204", "lon": "58.301911"},
        {"name": "Медицинский центр «Ваш доктор»", "city": "Новотроицк", "address": "ул. Советская, д. 10", "schedule": "с 9:00 до 18:00", "lat": "51.200492", "lon": "58.337178"},
    ]
    
    for institution in institutions:
        session.add(InstitutionModel(
            name=institution["name"],
            city=institution["city"],
            address=institution["address"],
            schedule=institution["schedule"],
            lat=institution["lat"],
            lon=institution["lon"],
        ))
    

def main():
    diseases_generator()
    employees_generator()
    question_symptoms_generator()
    context_questions_generator()
    institutions_generator()

    session.commit()


if __name__ == "__main__":
    main()
