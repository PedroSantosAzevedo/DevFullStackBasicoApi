from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Patient
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
paciente_tag = Tag(name="Paciente", description="Adição, visualização e remoção de pacientes à base")



@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/paciente', tags=[paciente_tag],
          responses={"200": PatientSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_paciente(form: PatientSchema):
    """Adiciona um novo Paciente à base de dados

    Retorna uma representação dos pacientes associados.
    """

    paciente = Patient(
        first_name=form.first_name,
        last_name=form.last_name,
        cpf=form.cpf,
        email=form.email,
        phone_number=form.phone_number,
        address=form.address
    )
    print(paciente.first_name, paciente.last_name, paciente.cpf, paciente.email, paciente.phone_number, paciente.address)
    try:
        # criando conexão com a base
        session = Session()
        # adicionando paciente
        session.add(paciente)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        return apresenta_paciente(paciente), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Paciente de mesmo nome já salvo na base :/"
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        return {"mesage": error_msg}, 400


@app.get('/pacientes', tags=[paciente_tag],
         responses={"200": PatientListSchema, "404": ErrorSchema})
def get_allPatients():
    """Faz a busca por todos os Produto cadastrados

    Retorna uma representação da listagem de produtos.
    """
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pacientes = session.query(Patient).all()

    if not pacientes:
        # se não há produtos cadastrados
        return {"pacientes": []}, 200
    else:
        # retorna a representação de pacientes
        print(pacientes)
        return apresenta_pacientes(pacientes), 200
    
@app.get('/pacientes/<nome>', tags=[paciente_tag],
         responses={"200": PatientSchema, "404": ErrorSchema})
def get_Patients(path: PatientNameSearchSchema):
    """Faz a busca por todos os Produto cadastrados

    Retorna uma representação da listagem de produtos.
    """
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pacientes = session.query(Patient).filter(Patient.first_name == path.first_name)

    if not pacientes:
        # se não há produtos cadastrados
        return {"pacientes": []}, 200
    else:
        # retorna a representação de pacientes
        print(pacientes)
        return apresenta_pacientes(pacientes), 200

@app.post('/pacienteCompleto/', tags=[paciente_tag],
            responses={"200": PatientSchema, "404": ErrorSchema})
def get_Complete_Patient(form: PatientFetchSchema):
    """Faz a busca por todos os Pacientes cadastrados

    Retorna uma representação da listagem de pacientes.
    """
    session = Session()

    try:
        patient = session.query(Patient).filter(Patient.cpf == form.cpf).first()
    except Exception as e:
        error_msg = "Erro ao conectar com a base de dados :/"
        return {"mesage": error_msg}, 502   

    if not patient:
        # se não há produtos cadastrados
        error_msg = "Paciete não encontrado na base :/"
        return {"mesage": error_msg}, 404
    else:
        # retorna a representação de pacientes
        print(patient)
        return apresenta_paciente(patient), 200


@app.delete('/patient', tags=[paciente_tag],
            responses={"200": PatientDelSchema, "404": ErrorSchema})
def del_patient(query: PatientDelSchema):
    """Deleta um pactiente a partir do nome de propacienteduto informado

    Retorna uma mensagem de confirmação da remoção.
    """
    patientId = unquote(unquote(query.cpf))
    print(patientId)
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Patient).filter(Patient.cpf == patientId).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Produto removido", "id": patientId}
    else:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        return {"mesage": error_msg}, 404


