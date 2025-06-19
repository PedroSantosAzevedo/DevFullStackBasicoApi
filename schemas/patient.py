from pydantic import BaseModel
from typing import Optional, List
from model.patient import Patient

class PatientSchema(BaseModel):
    """ Define como um novo paciente a ser inserido deve ser representado
    """
    first_name: str = "John"
    last_name: str = "Doe"
    date_of_birth: str = "2000-01-01"
    email: Optional[str] = "john.doe@example.com"
    phone_number: str = "123456789"
    address: Optional[str] = "123 Main St"


def apresenta_pacientes(pacientes: List[Patient]):
    """ Retorna uma representação de uma lista de pacientes em json
    """
    result = []
    for paciente in pacientes:
        result.append({
            "first_name": paciente.first_name,
            "last_name": paciente.last_name,
            "date_of_birth": paciente.date_of_birth,
            "email": paciente.email,
            "phone_number": paciente.phone_number,
            "address": paciente.address,
        })

    return {"pacientes": result}

def apresenta_paciente(paciente: Patient):
    """ Retorna uma representação do paciente em json
    """
    return {
        "first_name": paciente.first_name,
        "last_name": paciente.last_name,
        "date_of_birth": paciente.date_of_birth,
        "email": paciente.email,
        "phone_number": paciente.phone_number,
        "address": paciente.address,
    }