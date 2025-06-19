def validar_dose(peso, dose, unidade_input, medicamento):
    """
    Valida a dose prescrita considerando o peso do paciente.
    Verifica se a unidade coincide com a esperada (armazenada em 'unidade_dose')
    e se a dose, multiplicada por peso, se encontra dentro do intervalo seguro.
    
    Os campos 'dose_minima' e 'dose_maxima' no Excel devem conter a dose recomendada por kg.
    """
    # Verificar se a unidade de entrada é igual à esperada
    if unidade_input != medicamento["unidade_dose"]:
        return ("erro_unidade", f"Unidade incorreta. Deve ser {medicamento['unidade_dose']}.")
    
    # Cálculo das doses seguras com base no peso do paciente
    dose_minima_total = medicamento["dose_minima"] * peso
    dose_maxima_total = medicamento["dose_maxima"] * peso

    if dose < dose_minima_total:
        return ("dose_baixa", f"Dose prescrita {dose} é inferior à dose mínima de {dose_minima_total}.")
    elif dose > dose_maxima_total:
        return ("dose_alta", f"Dose prescrita {dose} é superior à dose máxima de {dose_maxima_total}.")
    else:
        return ("ok", f"Dose prescrita {dose} está dentro do intervalo seguro ({dose_minima_total} - {dose_maxima_total}).")

def verificar_incompatibilidade(compat_input, medicamento):
    """
    Verifica se os medicamentos informados (como uma string, separados por vírgula)
    estão listados como incompatíveis no registro do medicamento.
    
    Retorna uma lista com as incompatibilidades encontradas.
    """
    lista_incomp = str(medicamento["incompativeis"]).split(",")
    lista_incomp = [item.strip().lower() for item in lista_incomp if item.strip()]
    
    lista_input = [item.strip().lower() for item in compat_input.split(",") if item.strip()]
    incompatibilidades = [item for item in lista_input if item in lista_incomp]
    return incompatibilidades
