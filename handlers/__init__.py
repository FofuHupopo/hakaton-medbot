from sqlalchemy.orm import Session

from .user import *
from .admin import *

from models import engine, UnregisteredMessageModel


@dp.message_handler()
async def unregistered_message(message: types.Message):
    if not message.text:
        return

    with Session(engine) as session:
        message = UnregisteredMessageModel(
            telegram_id=message.chat.id,
            message=message.text
        )
        
        session.add(message)
        session.commit()
