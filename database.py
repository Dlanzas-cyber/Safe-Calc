import os
import pandas as pd

# Definir os nomes dos ficheiros de dados
MEDICAMENTOS_FILE = "medicamentos.xlsx"
REGISTROS_FILE = "registos.xlsx"

def inicializar_banco():
    """
    Inicializa a base de dados.
    Se os ficheiros 'medicamentos.xlsx' ou 'registos.xlsx' nao existirem,
    eles sao criados com dados de exemplo (para medicamentos) ou com a estrutura vazia (para registos).
    """
    if not os.path.exists(MEDICAMENTOS_FILE):
        df_med = pd.DataFrame({
            "nome": [
                "Morfina", "Fentanil", "Fenobarbital", "Levetiracetam",
                "Vancomicina", "Gentamicina", "Ampicilina", "Citrato de cafeina"
            ],
            "tipo": [
                "Opioide", "Opioide", "Antiepileptico", "Antiepileptico",
                "Antibiotico", "Antibiotico", "Antibiotico", "Estimulante respiratorio"
            ],
            "unidade_dose": [
                "mg", "mg", "mg", "mg",
                "mg", "mg", "mg", "mg"
            ],
            # Os valores de dose_minima e dose_maxima sao considerados por kg
            "dose_minima": [0.1, 0.05, 0.15, 0.1, 0.1, 0.04, 0.25, 0.1],
            "dose_maxima": [1.0, 0.5, 0.2, 0.6, 0.15, 0.075, 1.0, 0.2],
            "concentracao_maxima": [
                "1 mg/ml", "50 mcg/ml", "20 mg/ml", "100 mg/ml",
                "5 mg/ml", "1.5 mg/ml", "100 mg/ml", "20 mg/ml"
            ],
            # Usamos 'diluicao_sugerida' para que fique alinhado com o app.py
            "diluicao_sugerida": [
                "10 mg em 50 ml SG5%", "500 mcg em 50 ml SG5%",
                "50–100 mg em 10–20 ml", "500 mg em 50 ml SF ou SG5%",
                "500 mg em 100 ml SG5%", "10 mg/kg em 25–50 ml SG5%",
                "1 g em 10 ml SF", "10–20 mg em 10 ml SG5%"
            ],
            "forma_de_administracao": [
                "Perfusao continua", "Perfusao ou bolus lento",
                "Bolus IV lento", "Infusao IV em 15 min",
                "Infusao IV prolongada (>60 min)", "Bolus ou infusao lenta",
                "Bolus ou perfusao curta", "Bolus IV lento"
            ],
            "compativeis": [
                "Midazolam", "Midazolam", "", "", "", "", "Gentamicina", ""
            ],
            "incompativeis": [
                "Furosemida", "Aminofilina", "Glicose 10%", "", "", "Vancomicina", "", "Midazolam"
            ],
            "observacoes": [
                "Ajustar dose em RN prematuros. Risco de apneia. (GFN)",
                "Vigiar rigidez toracica em bolus rapidos. (MI)",
                "Usar filtro em perfusao. Risco de hipotensao. (GFN)",
                "Evitar mistura com sais de calcio. (Pediamecum)",
                "Evitar associacao com aminoglicosideos (nefrotoxicidade). (GFN)",
                "Monitorizar funcao renal. (MI)",
                "Solucao instavel apos reconstituicao (usar em <1 hora). (GFN)",
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
    """Carrega e retorna um DataFrame a partir do ficheiro 'medicamentos.xlsx'."""
    return pd.read_excel(MEDICAMENTOS_FILE, engine="openpyxl")

def carregar_registos():
    """Carrega e retorna um DataFrame a partir do ficheiro 'registos.xlsx'."""
    return pd.read_excel(REGISTROS_FILE, engine="openpyxl")

def salvar_registos(df):
    """Salva o DataFrame fornecido no ficheiro 'registos.xlsx'."""
    with pd.ExcelWriter(REGISTROS_FILE, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
