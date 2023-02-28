from db.engine import SessionAsync


async def get_db():
    async with SessionAsync() as session:
        yield session
