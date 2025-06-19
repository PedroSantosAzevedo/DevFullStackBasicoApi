from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from model.patient import Patient

class PatientSchema(BaseModel):
    """ Define como um novo paciente a ser inserido deve ser representado
    """
    first_name: str = "John"
    last_name: str = "Doe"
    cpf:str = "11111111111"
    email: str = "john.doe@example.com"
    phone_number: str = "123456789"
    address: str = "123 Main St"

class PatientListSchema(BaseModel):
    """ Define como uma lista de pacientes deve ser representada
    """
    pacientes: List[PatientSchema]


def apresenta_pacientes(pacientes: List[Patient]):
    """ Retorna uma representação de uma lista de pacientes em json
    """
    result = []
    for paciente in pacientes:
        result.append({
            "first_name": paciente.first_name,
            "last_name": paciente.last_name,
            "email": paciente.email,
            "phone_number": paciente.phone_number,
            "address": paciente.address,
            "cpf": paciente.cpf
        })

    return {"pacientes": result}

def apresenta_paciente(paciente: Patient):
    """ Retorna uma representação do paciente em json
    """
    return {
        "first_name": paciente.first_name,
        "last_name": paciente.last_name,
        "email": paciente.email,
        "phone_number": paciente.phone_number,
        "address": paciente.address,
        "cpf": paciente.cpf
    }