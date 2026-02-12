from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:parth471001@localhost/gym_coach"


engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_session():
    return SessionLocal()
