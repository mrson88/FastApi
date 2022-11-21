from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# MYSQL Series
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:daovanson88@localhost/TodoApplicationDatabase"
SQLALCHEMY_DATABASE_URL = "postgresql://kahpmtuz:k9h91WHG02lgb06ug3v88wca8pg5udwG@satao.db.elephantsql.com/kahpmtuz"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# MYSQL Series
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL
# )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
