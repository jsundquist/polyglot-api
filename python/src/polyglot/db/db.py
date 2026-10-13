from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

from os import environ

engine = create_engine(environ.get("DATABASE_URL", ""), echo=True)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]