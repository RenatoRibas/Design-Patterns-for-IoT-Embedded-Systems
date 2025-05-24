from typing import List, Tuple
import pandas as pd


def validar_colunas_dispositivos(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Valida se o DataFrame do Excel contém todas as colunas obrigatórias para o sistema funcionar.

    Retorna:
        - True e lista vazia, se tudo estiver certo
        - False e lista com as colunas que faltam, caso contrário
    """
    colunas_obrigatorias = [
        "Tag table",
        "TAG",
        "Area",
        "Descrição",
        "Range Min",
        "Range Max",
        "Unit",
    ]

    colunas_faltando = [col for col in colunas_obrigatorias if col not in df.columns]

    if colunas_faltando:
        return False, colunas_faltando
    return True, []
