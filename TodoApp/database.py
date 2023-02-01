from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# MYSQL Series
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:daovanson88@localhost/mrsondb"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:daovanson88@14.225.36.120/mrsondb"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL
# )
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:daovanson88@localhost/TodoApplicationDatabase"
# SQLALCHEMY_DATABASE_URL = "postgresql://ioipbvjh:gh55DaBH3Ikcl3nRdWfOK4ILYIlaHoHD@satao.db.elephantsql.com/ioipbvjh"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# MYSQL Series
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_size=40, max_overflow=0
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
