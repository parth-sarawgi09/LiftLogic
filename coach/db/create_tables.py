from coach.db.database import engine
from coach.db.models import Base


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")


if __name__ == "__main__":
    create_tables()
