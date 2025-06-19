{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 #!/usr/bin/env python3\
import os\
import pandas as pd\
from datetime import datetime\
\
# ===================================================\
# CONFIGURA\'c7\'c3O DE ARQUIVOS DA BASE DE DADOS\
# ===================================================\
\
MEDICAMENTOS_FILE = "medicamentos.xlsx"  # Base de dados dos f\'e1rmacos (edit\'e1vel via Excel)\
REGISTROS_FILE = "registos.xlsx"         # Registos dos c\'e1lculos (modo investiga\'e7\'e3o)\
\
# ===================================================\
# 1. INIT E CARREGAMENTO DA BASE DE DADOS\
# ===================================================\
\
def inicializar_banco():\
    # Se o ficheiro de medicamentos n\'e3o existir, criar uma base de dados de exemplo\
    if not os.path.exists(MEDICAMENTOS_FILE):\
        df_med = pd.DataFrame(\{\
            "nome": [\
                "Morfina", "Fentanil", "Fenobarbital", "Levetiracetam",\
                "Vancomicina", "Gentamicina", "Ampicilina", "Citrato de cafe\'edna"\
            ],\
            "tipo": [\
                "Opioide", "Opioide", "Antiepil\'e9ptico", "Antiepil\'e9ptico",\
                "Antibi\'f3tico", "Antibi\'f3tico", "Antibi\'f3tico", "Estimulante respirat\'f3rio"\
            ],\
            "unidade_dose": [\
                "mcg/kg/h", "mcg/kg/h", "mg/kg/dose", "mg/kg/dose",\
                "mg/kg/dose", "mg/kg/dose", "mg/kg/dose", "mg/kg/dose"\
            ],\
            "dose_minima": [10, 0.5, 15, 10, 10, 4, 25, 10],\
            "dose_maxima": [100, 5, 20, 60, 15, 7.5, 100, 20],\
            "dose_terapeutica": ["--"] * 8,  # Campo opcional para uso futuro\
            "concentracao_maxima": [\
                "1 mg/ml", "50 mcg/ml", "20 mg/ml", "100 mg/ml",\
                "5 mg/ml", "1.5 mg/ml", "100 mg/ml", "20 mg/ml"\
            ],\
            "diluicao_recomendada": [\
                "10 mg em 50 ml SG5%", "500 mcg em 50 ml SG5%", "50\'96100 mg em 10\'9620 ml", "500 mg em 50 ml SF ou SG5%",\
                "500 mg em 100 ml SG5%", "10 mg/kg em 25\'9650 ml SG5%", "1 g em 10 ml SF", "10\'9620 mg em 10 ml SG5%"\
            ],\
            "forma_de_administracao": [\
                "Perfus\'e3o cont\'ednua", "Perfus\'e3o ou b\'f3lus lento", "B\'f3lus IV lento", "Infus\'e3o IV em 15 min",\
                "Infus\'e3o IV prolongada (>60 min)", "B\'f3lus ou infus\'e3o lenta", "B\'f3lus ou perfus\'e3o curta", "B\'f3lus IV lento"\
            ],\
            "compativeis": [\
                "Midazolam", "Midazolam", "", "", "", "", "Gentamicina", ""\
            ],\
            "incompativeis": [\
                "Furosemida", "Aminofilina", "Glicose 10%", "", "", "Vancomicina", "", "Midazolam"\
            ],\
            "observacoes": [\
                "Ajustar dose em RN prematuros. Risco de apneia. (GFN)",\
                "Vigiar rigidez tor\'e1cica em bolos r\'e1pidos. (MI)",\
                "Usar filtro em perfus\'e3o. Risco de hipotens\'e3o. (GFN)",\
                "Evitar mistura com sais de c\'e1lcio. (Pediamecum)",\
                "Evitar associa\'e7\'e3o com aminoglicos\'eddeos (nefrotoxicidade). (GFN)",\
                "Monitorizar fun\'e7\'e3o renal. (MI)",\
                "Solu\'e7\'e3o inst\'e1vel ap\'f3s reconstitui\'e7\'e3o (usar em <1 hora). (GFN)",\
                "Monitorizar FC. Metabolismo lento em RN. (GFN)"\
            ]\
        \})\
        with pd.ExcelWriter(MEDICAMENTOS_FILE, engine="openpyxl") as writer:\
            df_med.to_excel(writer, index=False)\
    \
    # Se o ficheiro de registos n\'e3o existir, criar uma estrutura vazia\
    if not os.path.exists(REGISTROS_FILE):\
        df_reg = pd.DataFrame(columns=[\
            "data_hora", "peso", "medicamento", "dosis", "unidade", "via",\
            "diluicao_final", "compatibilidades_input", "resultado", "observacao_calculo"\
        ])\
        with pd.ExcelWriter(REGISTROS_FILE, engine="openpyxl") as writer:\
            df_reg.to_excel(writer, index=False)\
\
def carregar_medicamentos():\
    return pd.read_excel(MEDICAMENTOS_FILE, engine="openpyxl")\
\
def carregar_registos():\
    return pd.read_excel(REGISTROS_FILE, engine="openpyxl")\
\
def salvar_registos(df):\
    with pd.ExcelWriter(REGISTROS_FILE, engine="openpyxl") as writer:\
        df.to_excel(writer, index=False)\
\
# ===================================================\
# 2. FUN\'c7\'d5ES DE C\'c1LCULO E VALIDA\'c7\'c3O\
# ===================================================\
\
def validar_dose(peso, dose, unidade_input, medicamento):\
    """\
    Valida a dose prescrita comparando com os limites seguros do f\'e1rmaco.\
    Se a unidade fornecida n\'e3o coincidir com a esperada, retorna um erro.\
    """\
    unidade_esperada = medicamento["unidade_dose"]\
    if unidade_input != unidade_esperada:\
        return ("erro_unidade", f"Unidade incorreta. Deve ser \{unidade_esperada\}")\
    # Supondo que a dose j\'e1 est\'e1 normalizada (em mg/kg ou mcg/kg) \'96 caso seja necess\'e1rio, pode-se usar 'peso'\
    if dose < medicamento["dose_minima"]:\
        return ("dose_baixa", f"\{dose\} \'e9 inferior \'e0 dose m\'ednima de \{medicamento['dose_minima']\}")\
    elif dose > medicamento["dose_maxima"]:\
        return ("dose_alta", f"\{dose\} \'e9 superior \'e0 dose m\'e1xima de \{medicamento['dose_maxima']\}")\
    else:\
        return ("ok", "Dose dentro do intervalo seguro")\
\
def verificar_incompatibilidade(compat_input, medicamento):\
    """\
    Verifica se os medicamentos indicados no input aparecem na lista de incompat\'edveis para o f\'e1rmaco.\
    """\
    lista_incomp = str(medicamento["incompativeis"]).split(",")\
    lista_incomp = [x.strip().lower() for x in lista_incomp if x.strip()]\
    \
    # O input do utilizador deve ser uma lista separada por v\'edrgulas\
    lista_input = [x.strip().lower() for x in compat_input.split(",") if x.strip()]\
    incompatibilidades = [x for x in lista_input if x in lista_incomp]\
    return incompatibilidades\
\
# ===================================================\
# 3. INTERFACE DE LINHA DE COMANDO (CLI)\
# ===================================================\
\
def main():\
    print("=== SAFE-CALC: Valida\'e7\'e3o de Prescri\'e7\'e3o IV em UCI Pedi\'e1trica/Neonatal ===\\n")\
    \
    # Inicializa\'e7\'e3o e carregamento\
    inicializar_banco()\
    df_medicamentos = carregar_medicamentos()\
    df_registos = carregar_registos()\
    \
    # Listar medicamentos dispon\'edveis\
    print("Medicamentos dispon\'edveis:")\
    for idx, row in df_medicamentos.iterrows():\
        print(f"\{idx\} - \{row['nome']\} (\{row['tipo']\})")\
    \
    try:\
        med_index = int(input("\\nSelecione o n\'famero do f\'e1rmaco: "))\
    except ValueError:\
        print("Entrada inv\'e1lida. Saindo...")\
        return\
    if med_index < 0 or med_index >= len(df_medicamentos):\
        print("N\'famero fora do intervalo. Saindo...")\
        return\
        \
    medicamento = df_medicamentos.iloc[med_index]\
    \
    try:\
        peso = float(input("Peso do paciente (kg): "))\
        dose = float(input("Dose prescrita (valor num\'e9rico): "))\
    except ValueError:\
        print("Erro na convers\'e3o dos valores num\'e9ricos. Saindo...")\
        return\
    \
    print(f"A unidade esperada \'e9: \{medicamento['unidade_dose']\}")\
    unidade_input = input("Digite a unidade da dose: ").strip()\
    via = input("V\'eda de administra\'e7\'e3o (ex: IV): ").strip() or "IV"\
    diluicao_final = input("Dilui\'e7\'e3o final (ex: 100 ml/5 mg/ml): ").strip()\
    compat_input = input("Compatibilidades/incompatibilidades (separadas por v\'edrgulas): ").strip()\
    \
    # Valida\'e7\'e3o da dose\
    status, msg = validar_dose(peso, dose, unidade_input, medicamento)\
    print("\\nResultado da valida\'e7\'e3o da dose:")\
    if status == "erro_unidade":\
        print("ERRO:", msg)\
    elif status == "dose_baixa":\
        print("ATEN\'c7\'c3O:", msg)\
    elif status == "dose_alta":\
        print("ERRO:", msg)\
    else:\
        print("\uc0\u10004 \u65039  Dose dentro do intervalo seguro.")\
    \
    incompat = verificar_incompatibilidade(compat_input, medicamento)\
    if incompat:\
        print("Incompatibilidades detectadas:", ", ".join(incompat))\
    else:\
        print("Nenhuma incompatibilidade detetada.")\
    \
    # Mostrar detalhes do f\'e1rmaco\
    print("\\n=== Detalhes do F\'e1rmaco Selecionado ===")\
    print(f"Tipo terap\'eautico: \{medicamento['tipo']\}")\
    print(f"Unidade esperada: \{medicamento['unidade_dose']\}")\
    print(f"Dose segura: de \{medicamento['dose_minima']\} a \{medicamento['dose_maxima']\}")\
    print(f"Concentra\'e7\'e3o m\'e1xima: \{medicamento['concentracao_maxima']\}")\
    print(f"Dilui\'e7\'e3o recomendada: \{medicamento['diluicao_recomendada']\}")\
    print(f"Forma de administra\'e7\'e3o: \{medicamento['forma_de_administracao']\}")\
    print(f"Compat\'edveis: \{medicamento['compativeis']\}")\
    print(f"Incompat\'edveis: \{medicamento['incompativeis']\}")\
    print(f"Observa\'e7\'f5es: \{medicamento['observacoes']\}")\
    \
    # Registrar registo de c\'e1lculo (modo investiga\'e7\'e3o)\
    registar = input("\\nDeseja registar este c\'e1lculo? (s/n): ").strip().lower()\
    if registar == "s":\
        novo_registo = pd.DataFrame(\{\
            "data_hora": [datetime.now().isoformat()],\
            "peso": [peso],\
            "medicamento": [medicamento["nome"]],\
            "dosis": [dose],\
            "unidade": [unidade_input],\
            "via": [via],\
            "diluicao_final": [diluicao_final],\
            "compatibilidades_input": [compat_input],\
            "resultado": [msg],\
            "observacao_calculo": [f"Incompatibilidades: \{', '.join(incompat)\}"]\
        \})\
        df_registos = pd.concat([df_registos, novo_registo], ignore_index=True)\
        salvar_registos(df_registos)\
        print("Registo guardado com sucesso!")\
    else:\
        print("Registo n\'e3o efetuado.")\
    \
    # Mostrar hist\'f3rico de registos\
    ver_hist = input("\\nDeseja ver o hist\'f3rico de registos? (s/n): ").strip().lower()\
    if ver_hist == "s":\
        print("\\n=== Hist\'f3rico de Registos ===")\
        print(df_registos.to_string(index=False))\
\
if __name__ == "__main__":\
    main()\
}