#!/usr/bin/env python3
import streamlit as st
import pandas as pd
from datetime import datetime
from database import inicializar_banco, carregar_medicamentos, carregar_registos, salvar_registos
from validacao import validar_dose, verificar_incompatibilidade

# Configura a página da App
st.set_page_config(page_title="SAFE-CALC Web App", page_icon="favicon.ico", layout="centered")

st.title("SAFE-CALC – Validação de Prescrição IV")
st.write("Aplicação web para validar se uma prescrição intravenosa é segura com base em parâmetros clínicos.")

# Inicializa a base de dados (cria ficheiros se não existirem)
inicializar_banco()

# Carrega os dados dos medicamentos (ficheiro "medicamentos.xlsx")
df_medicamentos = carregar_medicamentos()

# Entradas do utilizador na barra lateral
st.sidebar.header("Entradas do Utilizador")
peso = st.sidebar.number_input("Peso do paciente (kg):", min_value=0.1, step=0.1)
medicamento_selecionado = st.sidebar.selectbox("Selecione o fármaco", df_medicamentos["nome"].tolist())
dose = st.sidebar.number_input("Dose prescrita (valor numérico):", min_value=0.0, step=0.1)
unidade_input = st.sidebar.selectbox("Unidade da dose", df_medicamentos["unidade_dose"].unique().tolist())
via = st.sidebar.text_input("Vía de administração (ex: IV):", "IV")
diluicao_final = st.sidebar.text_input("Diluição final (ex: 100 ml/5 mg/ml):", "")
compat_input = st.sidebar.text_input("Compatibilidades/incompatibilidades (separadas por vírgulas):", "")

# Seção de resultados
st.header("Resultados da Validação")
# Seleciona o registo do medicamento escolhido
medicamento = df_medicamentos[df_medicamentos["nome"] == medicamento_selecionado].iloc[0]

# Validação da dose
status, msg_dose = validar_dose(peso, dose, unidade_input, medicamento)
if status == "erro_unidade":
    st.error(msg_dose)
elif status == "dose_baixa":
    st.warning(msg_dose)
elif status == "dose_alta":
    st.error(msg_dose)
else:
    st.success("✔️ " + msg_dose)

# Verificação de incompatibilidades
incompat_lab = verificar_incompatibilidade(compat_input, medicamento)
if incompat_lab:
    st.error("Incompatibilidades detectadas: " + ", ".join(incompat_lab))
else:
    st.info("Nenhuma incompatibilidade detetada.")

# Exibição dos detalhes do medicamento
st.subheader("Detalhes do Fármaco Selecionado")
st.write("**Nome:**", medicamento["nome"])
st.write("**Tipo terapêutico:**", medicamento["tipo"])
st.write("**Unidade de dose esperada:**", medicamento["unidade_dose"])
st.write("**Dose segura:** de", medicamento["dose_minima"], "a", medicamento["dose_maxima"])
st.write("**Concentração máxima:**", medicamento["concentracao_maxima"])
st.write("**Diluição recomendada:**", medicamento["diluicao_recomendada"])
st.write("**Forma de administração:**", medicamento["forma_de_administracao"])
st.write("**Compatíveis:**", medicamento["compativeis"])
st.write("**Incompatíveis:**", medicamento["incompativeis"])
st.write("**Observações:**", medicamento["observacoes"])

# Registar o cálculo (modo investigação)
if st.button("Registar Validação"):
    df_registos = carregar_registos()
    novo_registo = pd.DataFrame({
        "data_hora": [datetime.now().isoformat()],
        "peso": [peso],
        "medicamento": [medicamento_selecionado],
        "dosis": [dose],
        "unidade": [unidade_input],
        "via": [via],
        "diluicao_final": [diluicao_final],
        "compatibilidades_input": [compat_input],
        "resultado": [msg_dose],
        "observacao_calculo": [f"Incompatibilidades: {', '.join(incompat_lab)}" if incompat_lab else "Nenhuma incompatibilidade"]
    })
    df_registos = pd.concat([df_registos, novo_registo], ignore_index=True)
    salvar_registos(df_registos)
    st.success("Registo guardado com sucesso!")

if st.checkbox("Mostrar Histórico de Registos"):
    df_registos = carregar_registos()
    st.dataframe(df_registos)
