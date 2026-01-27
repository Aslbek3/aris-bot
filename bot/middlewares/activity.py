from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message
from datetime import datetime
from database.requests import async_session
from database.models import User
from sqlalchemy import update

class ActivityMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        
        async with async_session() as session:
            # Update last activity on every message
            await session.execute(
                update(User).where(User.id == user_id).values(last_activity=datetime.utcnow())
            )
            await session.commit()
            
        return await handler(event, data)
