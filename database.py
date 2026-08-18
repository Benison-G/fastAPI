from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#TODO: change the password while working on local and do not password to github ${pwd}

db_url = "postgresql://postgres:{pwd}@localhost:5432/fastapi-demo"
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)