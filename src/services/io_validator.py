"""
Módulo de validação de colunas para a planilha de dispositivos.

Verifica se o DataFrame contém as colunas obrigatórias para DO e AI.
Dispositivos do tipo AI exigem colunas adicionais: Range Min, Range Max e Unit.
"""

from typing import List, Tuple

import pandas as pd


def validate_columns(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Valida se o DataFrame contém todas as colunas necessárias.

    Colunas obrigatórias:
    - Sempre: 'Tag table', 'TAG', 'Area', 'Descrição'
    - Se houver AI: 'Range Min', 'Range Max', 'Unit'

    Args:
        df (pd.DataFrame): DataFrame lido da planilha Excel.

    Returns:
            - True e lista vazia, se todas as colunas estiverem presentes.
            - False e lista com os nomes das colunas faltantes.
    """
    colunas_comuns = ["Tag table", "TAG", "Area", "Descrição"]
    colunas_ai = ["Range Min", "Range Max", "Unit"]

    colunas_requeridas = colunas_comuns.copy()

    if "AI" in df.get("Tag table", pd.Series()).unique():
        colunas_requeridas += colunas_ai

    colunas_faltando = [col for col in colunas_requeridas if col not in df.columns]

    return (False, colunas_faltando) if colunas_faltando else (True, [])
