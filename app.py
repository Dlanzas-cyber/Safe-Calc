#!/usr/bin/env python3
# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
from database import inicializar_banco, carregar_medicamentos, carregar_registos, salvar_registos
from validacao import validar_dose, verificar_incompatibilidade

# Configurar a página
st.set_page_config(page_title="SAFE-CALC Web App", layout="centered")

st.title("SAFE-CALC: Validação de Prescrição IV")
st.write("Aplicação web para validação de prescrições IV em UCI pediátrica/neonatal.")

# Inicializar a base de dados (cria ficheiros se não existirem)
inicializar_banco()

# Carregar os dados dos medicamentos
df_medicamentos = carregar_medicamentos()

# Seção de entradas do utilizador na barra lateral
st.sidebar.header("Entradas do Utilizador")
peso = st.sidebar.number_input("Peso do paciente (kg):", min_value=0.01, step=0.1)
medicamento_selecionado = st.sidebar.selectbox("Selecione o fármaco", df_medicamentos["nome"].tolist())
dose = st.sidebar.number_input("Dose prescrita (valor numérico):", min_value=0.0, step=0.1)
unidade_input = st.sidebar.selectbox("Unidade da dose", df_medicamentos["unidade_dose"].unique())
via = st.sidebar.text_input("Vía de administração (ex: IV):", "IV")
diluicao_final = st.sidebar.text_input("Diluição final (ex: 100 ml/5 mg/ml):", "")
compat_input = st.sidebar.text_input("Compatibilidades/incompatibilidades (separadas por vírgulas):", "")

# Exibir os resultados da validação
st.header("Resultados da Validação")

# Obter o registo do medicamento selecionado
medicamento = df_medicamentos[df_medicamentos["nome"] == medicamento_selecionado].iloc[0]

# Validar a dose
status, msg_dose = validar_dose(peso, dose, unidade_input, medicamento)

if status == "erro_unidade":
    st.error(msg_dose)
elif status == "dose_baixa":
    st.warning(msg_dose)
elif status == "dose_alta":
    st.error(msg_dose)
else:
    st.success("✔️ " + msg_dose)

# Verificar incompatibilidades
incompat_lab = verificar_incompatibilidade(compat_input, medicamento)
if incompat_lab:
    st.error("Incompatibilidades detectadas: " + ", ".join(incompat_lab))
else:
    st.info("Nenhuma incompatibilidade detetada.")

# Exibir detalhes do fármaco
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

# Registrar o registo (opção para modo investigação)
if st.button("Registar Validação"):
    df_registos = carregar_registos()
    novo_registro = pd.DataFrame({
        "data_hora": [datetime.now().isoformat()],
        "peso": [peso],
        "medicamento": [medicamento["nome"]],
        "dosis": [dose],
        "unidade": [unidade_input],
        "via": [via],
        "diluicao_final": [diluicao_final],
        "compatibilidades_input": [compat_input],
        "resultado": [msg_dose],
        "observacao_calculo": [f"Incompatibilidades: {', '.join(incompat_lab)}" if incompat_lab else "Nenhuma incompatibilidade"]
    })
    df_registos = pd.concat([df_registos, novo_registro], ignore_index=True)
    salvar_registos(df_registos)
    st.success("Registo guardado com sucesso!")

# Mostrar histórico de registos (opcional)
if st.checkbox("Mostrar Histórico de Registos"):
    df_registos = carregar_registos()
    st.dataframe(df_registos)
