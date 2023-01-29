from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Table, Column, Float, Integer, String, MetaData, ForeignKey, ARRAY


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    todos = relationship("Todos", back_populates="owner")
    xsmb = relationship("Xsmb", back_populates="owner")
    payment = relationship("Payment", back_populates="owner")
    payment_his = relationship("PaymentHistory", back_populates="owner")


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("Users", back_populates="todos")


class Xsmb(Base):
    __tablename__ = "xsmb"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    time = Column(String)
    data = Column(ARRAY(String))
    data_type = Column(String)
    data_cost = Column(String)
    active = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("Users", back_populates="xsmb")


class Payment(Base):
    __tablename__ = "payment"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    time = Column(String)
    data_money = Column(Float)
    active = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("Users", back_populates="payment")


class PaymentHistory(Base):
    __tablename__ = "payment_history"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    time = Column(String)
    data_money = Column(String)
    data_type = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("Users", back_populates="payment_his")


class ResultFiveMinute(Base):
    __tablename__ = "result_five_minute"
    id = Column(Integer, primary_key=True, index=True)
    day = Column(String)
    time = Column(String)
    result = Column(ARRAY(String))
    ischeck = Column(Boolean, default=True)


class ResultDaily(Base):
    __tablename__ = "result_daily"
    id = Column(Integer, primary_key=True, index=True)
    day = Column(String)
    result = Column(ARRAY(String))
