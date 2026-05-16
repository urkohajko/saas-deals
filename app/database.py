from sqlmodel import SQLModel, create_engine

engine = create_engine("sqlite:///deals.db")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
