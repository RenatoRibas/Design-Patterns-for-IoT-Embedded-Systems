import pandas as pd

from src.services.io_validator import validate_columns


def test_valida_colunas_dispositivos():
    """
    Testa se o validador detecta corretamente um DataFrame com todas as colunas obrigatórias,
    tanto para dispositivos DO quanto AI (incluindo colunas específicas de AI).
    """
    df = pd.DataFrame(
        columns=[
            "Tag table",
            "TAG",
            "Area",
            "Descrição",
            "Range Min",
            "Range Max",
            "Unit",
        ]
    )

    valido, faltando = validate_columns(df)

    assert valido is True
    assert faltando == []
