from sqlalchemy import text

from src.database.session import get_session


with get_session() as session:

    result = session.execute(text("SELECT version();"))

    print(result.scalar())