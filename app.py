from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Patient
from logger import logger
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
        date_of_birth=form.date_of_birth,
        email=form.email,
        phone_number=form.phone_number,
        address=form.address)
    logger.debug(f"Adicionando paciente de nome: '{paciente.first_name} {paciente.last_name}    '")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando paciente
        session.add(paciente)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado paciente de nome: '{paciente.first_name} {paciente.last_name}'")
        return apresenta_paciente(paciente), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Paciente de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar paciente '{paciente.first_name} {paciente.last_name}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar paciente '{paciente.first_name} {paciente.last_name}', {error_msg}")
        return {"mesage": error_msg}, 400


# @app.get('/pacientes', tags=[produto_tag],
#          responses={"200": ListagemProdutosSchema, "404": ErrorSchema})
# def get_produtos():
#     """Faz a busca por todos os Produto cadastrados

#     Retorna uma representação da listagem de produtos.
#     """
#     logger.debug(f"Coletando produtos ")
#     # criando conexão com a base
#     session = Session()
#     # fazendo a busca
#     produtos = session.query(Produto).all()

#     if not produtos:
#         # se não há produtos cadastrados
#         return {"produtos": []}, 200
#     else:
#         logger.debug(f"%d rodutos econtrados" % len(produtos))
#         # retorna a representação de produto
#         print(produtos)
#         return apresenta_produtos(produtos), 200


# @app.get('/produto', tags=[produto_tag],
#          responses={"200": ProdutoViewSchema, "404": ErrorSchema})
# def get_produto(query: ProdutoBuscaSchema):
#     """Faz a busca por um Produto a partir do id do produto

#     Retorna uma representação dos produtos e comentários associados.
#     """
#     produto_nome = query.nome
#     logger.debug(f"Coletando dados sobre produto #{produto_nome}")
#     # criando conexão com a base
#     session = Session()
#     # fazendo a busca
#     produto = session.query(Produto).filter(Produto.nome == produto_nome).first()

#     if not produto:
#         # se o produto não foi encontrado
#         error_msg = "Produto não encontrado na base :/"
#         logger.warning(f"Erro ao buscar produto '{produto_nome}', {error_msg}")
#         return {"mesage": error_msg}, 404
#     else:
#         logger.debug(f"Produto econtrado: '{produto.nome}'")
#         # retorna a representação de produto
#         return apresenta_produto(produto), 200


# @app.delete('/produto', tags=[produto_tag],
#             responses={"200": ProdutoDelSchema, "404": ErrorSchema})
# def del_produto(query: ProdutoBuscaSchema):
#     """Deleta um Produto a partir do nome de produto informado

#     Retorna uma mensagem de confirmação da remoção.
#     """
#     produto_nome = unquote(unquote(query.nome))
#     print(produto_nome)
#     logger.debug(f"Deletando dados sobre produto #{produto_nome}")
#     # criando conexão com a base
#     session = Session()
#     # fazendo a remoção
#     count = session.query(Produto).filter(Produto.nome == produto_nome).delete()
#     session.commit()

#     if count:
#         # retorna a representação da mensagem de confirmação
#         logger.debug(f"Deletado produto #{produto_nome}")
#         return {"mesage": "Produto removido", "id": produto_nome}
#     else:
#         # se o produto não foi encontrado
#         error_msg = "Produto não encontrado na base :/"
#         logger.warning(f"Erro ao deletar produto #'{produto_nome}', {error_msg}")
#         return {"mesage": error_msg}, 404


# @app.post('/cometario', tags=[comentario_tag],
#           responses={"200": ProdutoViewSchema, "404": ErrorSchema})
# def add_comentario(form: ComentarioSchema):
#     """Adiciona de um novo comentário à um produtos cadastrado na base identificado pelo id

#     Retorna uma representação dos produtos e comentários associados.
#     """
#     produto_id  = form.produto_id
#     logger.debug(f"Adicionando comentários ao produto #{produto_id}")
#     # criando conexão com a base
#     session = Session()
#     # fazendo a busca pelo produto
#     produto = session.query(Produto).filter(Produto.id == produto_id).first()

#     if not produto:
#         # se produto não encontrado
#         error_msg = "Produto não encontrado na base :/"
#         logger.warning(f"Erro ao adicionar comentário ao produto '{produto_id}', {error_msg}")
#         return {"mesage": error_msg}, 404

#     # criando o comentário
#     texto = form.texto
#     comentario = Comentario(texto)

#     # adicionando o comentário ao produto
#     produto.adiciona_comentario(comentario)
#     session.commit()

#     logger.debug(f"Adicionado comentário ao produto #{produto_id}")

#     # retorna a representação de produto
#     return apresenta_produto(produto), 200
