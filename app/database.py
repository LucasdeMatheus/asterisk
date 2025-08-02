from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from urllib.parse import quote_plus

# Codifica a senha corretamente
password = quote_plus("sua senha") 

DATABASE_URL = f"mysql+mysqlconnector://root:{password}@localhost:3306/asterisk_log"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
