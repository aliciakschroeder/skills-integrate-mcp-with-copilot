from sqlmodel import create_engine, SQLModel, Session, select
from pathlib import Path
from .models import Activity

DB_URL = "sqlite:///./data.db"
engine = create_engine(DB_URL, echo=False)


def init_db():
    Path("./").mkdir(parents=True, exist_ok=True)
    SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)


def get_all_activities():
    with get_session() as session:
        statement = select(Activity)
        results = session.exec(statement).all()
        return results


def get_activity_by_name(name: str):
    with get_session() as session:
        return session.get(Activity, name)
