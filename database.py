import os
import pandas as pd

# Definição dos nomes dos ficheiros de dados
MEDICAMENTOS_FILE = "medicamentos.xlsx"
REGISTROS_FILE = "registos.xlsx"

def inicializar_banco():
    """
    Verifica se os ficheiros de dados existem.
    Se não existirem, cria:
       - "medicamentos.xlsx" com dados de exemplo.
       - "registos.xlsx" com estrutura vazia.
    """
    if not os.path.exists(MEDICAMENTOS_FILE):
        df_med = pd.DataFrame({
            "nome": [
                "Morfina", "Fentanil", "Fenobarbital", "Levetiracetam",
                "Vancomicina", "Gentamicina", "Ampicilina", "Citrato de cafeína"
            ],
            "tipo": [
                "Opioide", "Opioide", "Antiepiléptico", "Antiepiléptico",
                "Antibiótico", "Antibiótico", "Antibiótico", "Estimulante respiratório"
            ],
            "unidade_dose": [
                "mcg/kg/h", "mcg/kg/h", "mg/kg/dose", "mg/kg/dose",
                "mg/kg/dose", "mg/kg/dose", "mg/kg/dose", "mg/kg/dose"
            ],
            "dose_minima": [10, 0.5, 15, 10, 10, 4, 25, 10],
            "dose_maxima": [100, 5, 20, 60, 15, 7.5, 100, 20],
            "dose_terapeutica": ["--"] * 8,
            "concentracao_maxima": [
                "1 mg/ml", "50 mcg/ml", "20 mg/ml", "100 mg/ml",
                "5 mg/ml", "1.5 mg/ml", "100 mg/ml", "20 mg/ml"
            ],
            "diluicao_recomendada": [
                "10 mg em 50 ml SG5%", "500 mcg em 50 ml SG5%",
                "50–100 mg em 10–20 ml", "500 mg em 50 ml SF ou SG5%",
                "500 mg em 100 ml SG5%", "10 mg/kg em 25–50 ml SG5%",
                "1 g em 10 ml SF", "10–20 mg em 10 ml SG5%"
            ],
            "forma_de_administracao": [
                "Perfusão contínua", "Perfusão ou bólus lento",
                "Bólus IV lento", "Infusão IV em 15 min",
                "Infusão IV prolongada (>60 min)", "Bólus ou infusão lenta",
                "Bólus ou perfusão curta", "Bólus IV lento"
            ],
            "compativeis": [
                "Midazolam", "Midazolam", "", "", "", "", "Gentamicina", ""
            ],
            "incompativeis": [
                "Furosemida", "Aminofilina", "Glicose 10%", "", "", "Vancomicina", "", "Midazolam"
            ],
            "observacoes": [
                "Ajustar dose em RN prematuros. Risco de apneia. (GFN)",
                "Vigiar rigidez torácica em bolos rápidos. (MI)",
                "Usar filtro em perfusão. Risco de hipotensão. (GFN)",
                "Evitar mistura com sais de cálcio. (Pediamecum)",
                "Evitar associação com aminoglicosídeos (nefrotoxicidade). (GFN)",
                "Monitorizar função renal. (MI)",
                "Solução instável após reconstituição (usar em <1 hora). (GFN)",
                "Monitorizar FC. Metabolismo lento em RN. (GFN)"
            ]
        })
        with pd.ExcelWriter(MEDICAMENTOS_FILE, engine="openpyxl") as writer:
            df_med.to_excel(writer, index=False)
    
    if not os.path.exists(REGISTROS_FILE):
        df_reg = pd.DataFrame(columns=[
            "data_hora", "peso", "medicamento", "dosis", "unidade", "via",
            "diluicao_final", "compatibilidades_input", "resultado", "observacao_calculo"
        ])
        with pd.ExcelWriter(REGISTROS_FILE, engine="openpyxl") as writer:
            df_reg.to_excel(writer, index=False)

def carregar_medicamentos():
    """Carrega e retorna o DataFrame com os medicamentos."""
    return pd.read_excel(MEDICAMENTOS_FILE, engine="openpyxl")

def carregar_registos():
    """Carrega e retorna o DataFrame com os registos."""
    return pd.read_excel(REGISTROS_FILE, engine="openpyxl")

def salvar_registos(df):
    """Guarda o DataFrame fornecido no ficheiro 'registos.xlsx'."""
    with pd.ExcelWriter(REGISTROS_FILE, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
