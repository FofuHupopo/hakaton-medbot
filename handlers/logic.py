import os
import re
import pymorphy2
from sqlalchemy.orm import Session

from bot import dp, bot, MESSAGES
from models import engine, UserModel


async def notify_administration(message: str):
    with Session(engine) as session:
        admins = session.query(UserModel).filter(
            UserModel.is_admin == True,
            UserModel.enable_notifications == True
        ).all()

        admins_telegram_id = list(map(lambda admin: admin.telegram_id, admins))

    for admin in admins_telegram_id:
        await bot.send_message(admin, message)


def get_link_to_appointment() -> str:
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    link_file = os.path.join(root_dir, "data/link_to_appointment.txt")
    
    if not os.path.exists(link_file):
        with open(link_file, "w", encoding="utf-8") as file:
            file.write(MESSAGES["no_link"])
    
    with open(link_file, "r", encoding="utf-8") as file:
        return file.read()


def update_link_to_appoinment(new_link: str):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    link_file = os.path.join(root_dir, "data/link_to_appointment.txt")
    
    with open(link_file, "w", encoding="utf-8") as file:
        file.write(new_link)


morph = pymorphy2.MorphAnalyzer()


def lemmatize(text: str) -> set:
    text_no_punct = re.sub(r'[^\w\s]', '', text)
    words = text_no_punct.split()
    return {morph.parse(word)[0].normal_form for word in words}

