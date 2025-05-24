import pandas as pd
from src.services.io_validator import validar_colunas_dispositivos

def test_valida_colunas_dispositivos():
    df = pd.DataFrame(columns=[
        'Tag table', 'TAG', 'Area', 'Descrição', 'Range Min', 'Range Max', 'Unit'
    ])
    valido, faltando = validar_colunas_dispositivos(df)
    assert valido is True
    assert faltando == []
