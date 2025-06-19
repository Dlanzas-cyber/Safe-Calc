#!/usr/bin/env python3
import streamlit as st
import pandas as pd
from datetime import datetime
from database import inicializar_banco, carregar_medicamentos, carregar_registos, salvar_registos
from validacao import validar_dose, verificar_incompatibilidade

# Configurar a página da app
st.set_page_config(page_title="SAFE-CALC Web App", page_icon=":safe-calc.ico:", layout="centered")

st.title("SAFE-CALC - Validacao de Prescricao IV")
st.write("Aplicacao web para validar se uma prescricao intravenosa e segura com base em parametros clinicos.")

# Inicializar a base de dados (cria ficheiros se nao existirem)
inicializar_banco()

# Carrega os dados do ficheiro "medicamentos.xlsx"
df_medicamentos = carregar_medicamentos()
# Normalizar nomes das colunas: converter para minúsculas e remover espacos
df_medicamentos.columns = df_medicamentos.columns.str.lower().str.strip()

# Entradas do utilizador na barra lateral
st.sidebar.header("Entradas do Utilizador")
peso = st.sidebar.number_input("Peso do paciente (kg):", min_value=0.1, step=0.1)

# Selecionar o medicamento (campo 'nome' no Excel)
medicamento_selecionado = st.sidebar.selectbox("Selecione o farmaco", df_medicamentos["nome"].tolist())

# Entrada para a dose prescrita:
dose_prescrita = st.sidebar.number_input("Dose prescrita (valor numerico):", min_value=0.0, step=0.1)
unidade_dose_input = st.sidebar.selectbox("Unidade da dose", ("gr", "mg", "mcg", "UI"))

via = st.sidebar.text_input("Via de administracao (ex: IV):", "IV")
diluicao_final = st.sidebar.text_input("Diluição final (ex: 100 ml/5 mg/ml):", "")
compat_input = st.sidebar.text_input("Compatibilidades/incompativeis (separadas por virgulas):", "")

st.header("Resultados da Validacao")
# Obter o registro do medicamento escolhido
medicamento = df_medicamentos[df_medicamentos["nome"] == medicamento_selecionado].iloc[0]

# Validar a dose prescrita considerando o peso
status, msg_dose = validar_dose(peso, dose_prescrita, unidade_dose_input, medicamento)
if status == "erro_unidade":
    st.error(msg_dose)
elif status == "dose_baixa":
    st.warning(msg_dose)
elif status == "dose_alta":
    st.error(msg_dose)
else:
    st.success("✔️ " + msg_dose)

# Verificar incompatibilidades (usando a função do validacao.py)
incompat_lab = verificar_incompatibilidade(compat_input, medicamento)
if incompat_lab:
    st.error("Incompatibilidades detectadas: " + ", ".join(incompat_lab))
else:
    st.info("Nenhuma incompatibilidade detetada.")

# Exibir detalhes do medicamento com formatação em negrito e fonte maior para alguns campos
st.subheader("Detalhes do Farmaco Selecionado")
st.write("**Nome:**", medicamento["nome"])
st.write("**Tipo terapeutico:**", medicamento["tipo"])
st.write("**Unidade de dose esperada:**", medicamento["unidade_dose"])
st.write("**Dose segura (por kg):** de", medicamento["dose_minima"], "a", medicamento["dose_maxima"])
st.write("**Concentracao maxima:**", medicamento["concentracao_maxima"])
st.write("**Diluição sugerida:**", medicamento["diluicao_sugerida"])
st.write("**Forma de administracao:**", medicamento["forma_de_administracao"])

st.markdown(
    f"<div style='font-size:20px; font-weight:bold;'>Compativeis: {medicamento['compativeis']}</div>",
    unsafe_allow_html=True)
st.markdown(
    f"<div style='font-size:20px; font-weight:bold;'>Incompativeis: {medicamento['incompativeis']}</div>",
    unsafe_allow_html=True)
st.markdown(
    f"<div style='font-size:20px; font-weight:bold;'>Observacoes: {medicamento['observacoes']}</div>",
    unsafe_allow_html=True)

if st.button("Registar Validacao"):
    df_registos = carregar_registos()
    novo_registo = pd.DataFrame({
        "data_hora": [datetime.now().isoformat()],
        "peso": [peso],
        "medicamento": [medicamento_selecionado],
        "dosis": [dose_prescrita],
        "unidade": [unidade_dose_input],
        "via": [via],
        "diluicao_final": [diluicao_final],
        "compatibilidades_input": [compat_input],
        "resultado": [msg_dose],
        "observacao_calculo": [f"Incompatibilidades: {', '.join(incompat_lab)}" if incompat_lab else "Nenhuma incompatibilidade"]
    })
    df_registos = pd.concat([df_registos, novo_registo], ignore_index=True)
    salvar_registos(df_registos)
    st.success("Registo guardado com sucesso!")

if st.checkbox("Mostrar Historico de Registos"):
    df_registos = carregar_registos()
    st.dataframe(df_registos)
