from sqlalchemy import select, update
from datetime import datetime
# 👇 Biz engine va async_session ni models.py dan import qilyapmiz
from database.models import User, Transaction, Goal, Diary, Base, engine, async_session

# DIQQAT: Bu yerda engine = ... yaratish shart emas, chunki tepadagi importdan kelyapti.

async def init_db():
    # models.py dagi engine ishlatiladi
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def add_transaction(user_id, amount, category, trans_type, description):
    # models.py dagi session ishlatiladi
    async with async_session() as session:
        # Ensure user exists
        user = await session.get(User, user_id)
        if not user:
            user = User(id=user_id)
            session.add(user)
        
        new_trans = Transaction(
            user_id=user_id,
            amount=amount,
            category=category,
            type=trans_type,
            description=description
        )
        session.add(new_trans)
        
        # Update last activity
        await session.execute(
            update(User).where(User.id == user_id).values(last_activity=datetime.utcnow())
        )
        
        await session.commit()

async def add_diary_entry(user_id, content, sentiment, voice_file_id):
    async with async_session() as session:
        new_entry = Diary(
            user_id=user_id,
            content=content,
            sentiment=sentiment,
            voice_file_id=voice_file_id
        )
        session.add(new_entry)
        await session.commit()
