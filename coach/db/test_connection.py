from sqlalchemy import text
from coach.db.database import engine

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 'MySQL connected!'"))
        for row in result:
            print(row[0])
except Exception as e:
    print("Connection failed:", e)
