from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# MYSQL Series
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:daovanson88@127.0.0.1:3306/todoapp"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:daovanson88@localhost/TodoApplicationDatabase"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL
# )

SQLALCHEMY_DATABASE_URL = "postgresql://kahpmtuz:k9h91WHG02lgb06ug3v88wca8pg5udwG@satao.db.elephantsql.com/kahpmtuz"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# MYSQL Series
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL
# )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
