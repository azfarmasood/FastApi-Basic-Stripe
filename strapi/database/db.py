from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import SQLModel, Session, create_engine
from starlette.config import Config


try:
    config = Config(".env")
except FileNotFoundError as error:
    print(str(error))
    
db = config("DB")
strip_secret_key = config("STRIPE_SECRET_KEY")
# strip_publisher_key = config("STRIPE_PUBLISHABLE_KEY")
base_url = config("BASE_URL")

connection_string = db.replace("postgresql", "postgresql+psycopg")

engine = create_engine(connection_string, echo = True, max_overflow = 0, pool_recycle = 300, pool_pre_ping = True)

async def get_tables(app: FastAPI):
    print(f"creating tables... {app}")
    SQLModel.metadata.create_all(bind = engine)
    yield
    
def get_session():
    with Session(engine) as session:
        yield session
        
        
DB_SESSION = Annotated[Session, Depends(get_session)]