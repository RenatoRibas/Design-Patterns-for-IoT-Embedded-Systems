"""
Módulo responsável pela leitura da planilha Excel contendo a lista de dispositivos de I/O.
Retorna objetos do tipo DODevice ou AIDevice com base nas colunas do Excel.

Aplica validação de colunas obrigatórias e realiza parsing seguro dos campos.
"""

import logging
import os
from typing import List, NamedTuple, Union

import pandas as pd

from src.services.io_validator import validate_columns

logger = logging.getLogger(__name__)


class DODevice(NamedTuple):
    tipo: str
    tag: str
    area: str
    descricao: str


class AIDevice(NamedTuple):
    tipo: str
    tag: str
    area: str
    descricao: str
    range_min: float
    range_max: float
    unit: str


def read_lista_de_io(file_path: str) -> List[Union[DODevice, AIDevice]]:
    """
    Lê o arquivo Excel contendo a lista de dispositivos e retorna uma lista de objetos
    do tipo DODevice ou AIDevice, dependendo do tipo da linha.

    Args:
        file_path (str): Caminho absoluto do arquivo Excel.

    Returns:
        List[Union[DODevice, AIDevice]]: Lista de dispositivos criados com base nas colunas da lista de IO.

    Raises:
        FileNotFoundError: Caso o arquivo não seja encontrado.
        ValueError: Caso colunas obrigatórias estejam ausentes.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    df = pd.read_excel(file_path)

    valido, faltando = validate_columns(df)
    if not valido:
        raise ValueError(f"Colunas faltando no arquivo: {faltando}")

    df_filtered = df.loc[
        ((df["Tag table"] == "AI") & (df["TAG"].notnull())) | (df["Tag table"] == "DO")
    ]

    devices_data: List[Union[DODevice, AIDevice]] = []

    for _, row in df_filtered.iterrows():
        tipo = row["Tag table"]
        tag = row["TAG"]
        area = row["Area"]
        descricao = row["Descrição"]

        if tipo == "AI":
            range_min = float(row["Range Min"])
            range_max = float(row["Range Max"])
            unit = str(row["Unit"]) if pd.notna(row["Unit"]) else ""
            device = AIDevice(tipo, tag, area, descricao, range_min, range_max, unit)
        else:
            device = DODevice(tipo, tag, area, descricao)

        devices_data.append(device)

    return devices_data
