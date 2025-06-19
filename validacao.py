def validar_dose(peso, dose, unidade_input, medicamento):
    """
    Valida a dose prescrita:
        - Verifica se a unidade coincide com a esperada.
        - Compara a dose com os limites seguros (entre dose_minima e dose_maxima).
    """
    if unidade_input != medicamento["unidade_dose"]:
        return ("erro_unidade", f"Unidade incorreta. Deve ser {medicamento['unidade_dose']}")
    
    if dose < medicamento["dose_minima"]:
        return ("dose_baixa", f"{dose} é inferior à dose mínima de {medicamento['dose_minima']}")
    elif dose > medicamento["dose_maxima"]:
        return ("dose_alta", f"{dose} é superior à dose máxima de {medicamento['dose_maxima']}")
    else:
        return ("ok", "Dose dentro do intervalo seguro")

def verificar_incompatibilidade(compat_input, medicamento):
    """
    Verifica se os medicamentos informados (input) estão entre os incompatíveis do fármaco.
    Retorna uma lista das incompatibilidades encontradas.
    """
    lista_incomp = str(medicamento["incompativeis"]).split(",")
    lista_incomp = [item.strip().lower() for item in lista_incomp if item.strip()]
    
    lista_input = [item.strip().lower() for item in compat_input.split(",") if item.strip()]
    incompatibilidades = [item for item in lista_input if item in lista_incomp]
    return incompatibilidades
