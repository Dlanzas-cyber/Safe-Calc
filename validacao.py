def validar_dose(peso, dose, unidade_input, medicamento):
    """
    Valida a dose prescrita considerando o peso do paciente.
    Converte a dose para mg e a compara com o intervalo seguro,
    usando os valores 'dose_minima' e 'dose_maxima' (por kg) do medicamento.
    """
    # Converter a dose para mg conforme a unidade
    if unidade_input == "mg":
        dose_mg = dose
    elif unidade_input == "gr":
        dose_mg = dose * 1000
    elif unidade_input == "mcg":
        dose_mg = dose / 1000
    elif unidade_input == "UI":
        return ("erro_unidade", "Conversão não disponível para a unidade UI.")
    else:
        return ("erro_unidade", f"Unidade {unidade_input} desconhecida.")

    # Calcular o total seguro com base no peso (dose por kg)
    dose_minima_total = medicamento["dose_minima"] * peso
    dose_maxima_total = medicamento["dose_maxima"] * peso

    if dose_mg < dose_minima_total:
        return ("dose_baixa", f"Dose prescrita ({dose_mg:.3f} mg) é inferior à dose mínima ({dose_minima_total:.3f} mg).")
    elif dose_mg > dose_maxima_total:
        return ("dose_alta", f"Dose prescrita ({dose_mg:.3f} mg) é superior à dose máxima ({dose_maxima_total:.3f} mg).")
    else:
        return ("ok", f"Dose prescrita ({dose_mg:.3f} mg) está dentro do intervalo seguro ({dose_minima_total:.3f} - {dose_maxima_total:.3f} mg).")

def verificar_incompatibilidade(compat_input, medicamento):
    """
    Verifica se os medicamentos informados (em uma string, separados por vírgula)
    estão listados como incompatíveis no registro do medicamento.
    Retorna uma lista com as incompatibilidades encontradas.
    """
    lista_incomp = str(medicamento["incompativeis"]).split(",")
    lista_incomp = [item.strip().lower() for item in lista_incomp if item.strip()]
    
    lista_input = [item.strip().lower() for item in compat_input.split(",") if item.strip()]
    incompatibilidades = [item for item in lista_input if item in lista_incomp]
    return incompatibilidades
