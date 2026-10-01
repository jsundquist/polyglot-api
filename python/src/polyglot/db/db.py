from sqlmodel import create_engine, Session
from typing import Annotated
from fastapi import Depends

DATABASE_URL = "postgresql+psycopg://polyglot:polyglot@localhost:5432/polyglot_api"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]