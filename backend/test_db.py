from sqlalchemy import text

from app.db.session import engine


with engine.connect() as connection:
    version = connection.execute(text("SELECT version();"))
    print(version.scalar())
