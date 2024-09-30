from fastapi import APIRouter, HTTPException, status
from models.vendas import Venda, ProductItem
from typing import List
import os
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

# Conexão com o MongoDB
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client.VentusSystemDB
vendas_collection = db["vendas"]
counters_collection = db["counters"]

router = APIRouter()

# Função para obter o próximo ID sequencial de vendas
def get_next_id():
    # Encontra o contador "venda_id" e incrementa o valor em 1
    counter = counters_collection.find_one_and_update(
        {"_id": "venda_id"},
        {"$inc": {"seq_value": 1}},
        return_document=True,
        upsert=True  # Se não existir o contador, ele será criado
    )
    return counter["seq_value"]

# Rota para buscar uma venda por ID
@router.get("/vendas/{venda_id}", response_model=Venda)
async def get_venda_by_id(venda_id: str):
    try:
        # Verifica se o venda_id é um ObjectId válido
        if ObjectId.is_valid(venda_id):
            venda = vendas_collection.find_one({"_id": ObjectId(venda_id)})
        else:
            # Se não for um ObjectId, trata como um ID string normal
            venda = vendas_collection.find_one({"_id": venda_id})

        if not venda:
            raise HTTPException(status_code=404, detail="Venda não encontrada")

        # Retorna a venda encontrada
        return Venda(**venda)

    except Exception as e:
        # Loga o erro para depuração e retorna um erro de servidor
        print(f"Erro ao buscar a venda: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao buscar a venda")

@router.get("/vendas", response_model=List[Venda])
async def get_all_vendas():
    vendas = list(vendas_collection.find())
    return [Venda(**venda) for venda in vendas]

@router.post("/vendas", response_model=Venda, status_code=status.HTTP_201_CREATED)
async def create_venda(venda: Venda):
    # Gera o ID sequencial para a venda
    venda.id = str(get_next_id())  # Gera um ID sequencial com no mínimo 5 dígitos
    venda.calculate_total()  # Calcula o total da venda
    venda_dict = venda.dict()
    venda_dict["_id"] = venda.id  # Usa o ID gerado como o _id do MongoDB
    vendas_collection.insert_one(venda_dict)
    return venda

@router.put("/vendas/{venda_id}", response_model=Venda)
async def update_venda(venda_id: str, venda_atualizada: Venda):
    try:
        # Busca a venda existente no banco de dados
        venda_existente = vendas_collection.find_one({"_id": venda_id})
        if not venda_existente:
            raise HTTPException(status_code=404, detail="Venda não encontrada")

        # Atualiza os itens da venda com os novos produtos e recalcula o valor total
        venda_obj = Venda(**venda_existente)

        # Verifica se o nome do cliente (client_id) foi passado e atualiza
        if venda_atualizada.client_id:
            venda_obj.client_id = venda_atualizada.client_id  # Atualiza o nome do cliente

        venda_obj.products = venda_atualizada.products  # Atualiza a lista de produtos
        venda_obj.calculate_total()  # Recalcula o total da venda com os novos produtos

        # Converte os objetos Pydantic para dicionários antes de salvar no MongoDB
        produtos_dict = [produto.dict() for produto in venda_obj.products]  # Converte a lista de produtos para dicionário
        venda_dict = venda_obj.dict()  # Converte a venda completa para dicionário

        # Atualiza a venda no banco de dados, incluindo o nome do cliente se alterado
        vendas_collection.update_one(
            {"_id": venda_id},
            {"$set": {
                "client_id": venda_obj.client_id,  # Atualiza o nome do cliente no banco de dados
                "products": produtos_dict,
                "total_value": venda_dict["total_value"]
            }}
        )

        return venda_obj
    except Exception as e:
        # Logando o erro para ajudar na depuração
        print(f"Erro ao atualizar a venda: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao atualizar a venda")


@router.put("/vendas/{venda_id}/finalizar", response_model=Venda)
async def finalizar_venda(venda_id: str):
    venda = vendas_collection.find_one({"_id": venda_id})
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    
    # Atualiza o status para 'completed' e define a data de finalização no formato brasileiro
    venda_obj = Venda(**venda)
    venda_obj.status = "completed"
    venda_obj.set_data_finalizacao()  # Define a data no formato brasileiro

    # Atualiza no banco de dados
    vendas_collection.update_one(
        {"_id": venda_id},
        {"$set": {
            "status": "completed",
            "data_finalizacao": venda_obj.data_finalizacao
        }}
    )
    
    return venda_obj

@router.delete("/vendas/{venda_id}")
async def delete_venda(venda_id: str):
    result = vendas_collection.delete_one({"_id": venda_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return {"msg": "Venda deletada com sucesso"}