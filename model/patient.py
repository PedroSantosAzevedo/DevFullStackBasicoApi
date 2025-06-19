from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base

class Patient(Base):
    __tablename__ = 'patient'

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    cpf = Column(String(11),  primary_key=True, nullable=False)
    email = Column(String(100), unique=False, nullable=True)
    phone_number = Column(String(15), nullable=False)
    address = Column(String(255), nullable=True)

    def __init__(self, first_name: str, last_name: str, cpf: str, email: str, phone_number: str, address: str):
        self.first_name = first_name
        self.last_name = last_name
        self.cpf = cpf
        self.email = email
        self.phone_number = phone_number
        self.address = address
