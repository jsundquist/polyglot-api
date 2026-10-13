import os
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

database = os.environ["SQLALCHEMY_DATABASE_URL"]
engine = create_engine(
    database, echo=os.environ.get("SQL_ECHO", "false").lower() == "true"
)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
