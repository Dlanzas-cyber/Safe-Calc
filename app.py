#!/usr/bin/env python3
import streamlit as st
import pandas as pd
from datetime import datetime
from database import inicializar_banco, carregar_medicamentos, carregar_registos, salvar_registos
from validacao import validar_dose, verificar_incompatibilidade

# Configurar a página da app com título, ícone e layout centralizado
st.set_page_config(
    page_title="SAFE-CALC Web App",
    page_icon=":rocket:",  # Se tiver um favicon personalizado, pode usar "favicon.ico"
    layout="centered"
)

st.title("SAFE-CALC - Validação de Prescrição IV")
st.write("Aplicação web para validar se uma prescrição intravenosa é segura com base em parâmetros clínicos.")

# Inicializar a base de dados (cria os ficheiros se não existirem)
inicializar_banco()

# Carregar os dados do ficheiro "medicamentos.xlsx"
df_medicamentos = carregar_medicamentos()
# Normalizar os nomes das colunas: converter para minúsculas e remover espaços
df_medicamentos.columns = df_medicamentos.columns.str.lower().str.strip()

# Entradas do utilizador na barra lateral
st.sidebar.header("Entradas do Utilizador")
peso = st.sidebar.number_input("Peso do paciente (kg):", min_value=0.1, step=0.1)
medicamento_selecionado = st.sidebar.selectbox("Selecione o fármaco", df_medicamentos["nome"].tolist())

# Entrada para a dose prescrita e a unidade
dose_prescrita = st.sidebar.number_input("Dose prescrita (valor numérico):", min_value=0.0, step=0.1)
unidade_dose_input = st.sidebar.selectbox("Unidade da dose", ("gr", "mg", "mcg", "UI"))

via = st.sidebar.text_input("Vía de administração (ex: IV):", "IV")

# Após os inputs de dose, mostrar um separador e o campo de conversão (não editável)
st.markdown("---")
if peso > 0 and dose_prescrita > 0:
    # Converter a dose para mg conforme a unidade
    if unidade_dose_input == "mg":
        dose_mg = dose_prescrita
    elif unidade_dose_input == "gr":
        dose_mg = dose_prescrita * 1000
    elif unidade_dose_input == "mcg":
        dose_mg = dose_prescrita / 1000
    elif unidade_dose_input == "UI":
        dose_mg = None  # Conversão não definida para UI
    else:
        dose_mg = None

    if dose_mg is not None:
        mg_per_kg_dose = dose_mg / peso
        # Supondo que, para esta conversão, o valor em mg/kg/h seja o mesmo da dose por dose
        mg_per_kg_h = mg_per_kg_dose
        mg_per_kg_min = mg_per_kg_h / 60
        mcg_per_kg_h = mg_per_kg_h * 1000
        mcg_per_kg_min = mg_per_kg_min * 1000
        conversion_str = (
            f"mg/kg/dose: {mg_per_kg_dose:.3f} | "
            f"mg/kg/h: {mg_per_kg_h:.3f} | "
            f"mg/kg/min: {mg_per_kg_min:.3f} | "
            f"mcg/kg/h: {mcg_per_kg_h:.3f} | "
            f"mcg/kg/min: {mcg_per_kg_min:.3f}"
        )
    else:
        conversion_str = "Conversão não disponível para a unidade UI"
else:
    conversion_str = "Insira valores válidos para peso e dose"

st.text_area("Conversão (não editável):", value=conversion_str, disabled=True)

# Cabeçalho para os resultados de validação
st.header("Resultados da Validação")

# Obter o registro completo do medicamento selecionado
medicamento = df_medicamentos[df_medicamentos["nome"] == medicamento_selecionado].iloc[0]

# Validar a dose prescrita (a conversão para mg é realizada internamente na função)
status, msg_dose = validar_dose(peso, dose_prescrita, unidade_dose_input, medicamento)
if status == "erro_unidade":
    st.error(msg_dose)
elif status == "dose_baixa":
    st.warning(msg_dose)
elif status == "dose_alta":
    st.error(msg_dose)
else:
    st.success("✔️ " + msg_dose)

# Exibir detalhes do medicamento com formatação – alguns campos em negrito e com acentos
st.subheader("Detalhes do Fármaco Selecionado")
st.write("**Nome:**", medicamento["nome"])
st.write("**Tipo terapêutico:**", medicamento["tipo"])
st.write("**Unidade de dose esperada:**", medicamento["unidade_dose"])
st.write("**Dose segura (por kg):** de", medicamento["dose_minima"], "a", medicamento["dose_maxima"])
st.write("**Concentração máxima:**", medicamento["concentracao_maxima"])
st.write("**Diluição sugerida:**", medicamento["diluicao_sugerida"])
st.write("**Forma de administração:**", medicamento["forma_de_administracao"])
st.markdown(f"<div style='font-size:20px; font-weight:bold;'>Compatíveis: {medicamento['compativeis']}</div>", unsafe_allow_html=True)
st.markdown(f"<div style='font-size:20px; font-weight:bold;'>Incompatíveis: {medicamento['incompativeis']}</div>", unsafe_allow_html=True)
st.markdown(f"<div style='font-size:20px; font-weight:bold;'>Observações: {medicamento['observacoes']}</div>", unsafe_allow_html=True)

# Botão para registrar a validação
if st.button("Registar Validação"):
    df_registos = carregar_registos()
    novo_registo = pd.DataFrame({
        "data_hora": [datetime.now().isoformat()],
        "peso": [peso],
        "medicamento": [medicamento_selecionado],
        "dosis":
