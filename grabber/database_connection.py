from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Returns what I understand to be a session maker object
def connect(url):
    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    return Session

