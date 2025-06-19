# SAFE-CALC CLI Web App

Aplicação web para validação de prescrições IV em UCI pediátrica/neonatal.

## Como Utilizar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt


---

## Sobre os Ficheiros Excel

- **medicamentos.xlsx:**  
  - Será utilizado para armazenar os dados dos fármacos.  
  - Pode ser editado diretamente no Excel e deve incluir os campos apresentados no código (nome, tipo, unidade_dose, dose_minima, dose_maxima, etc.).
  
- **registos.xlsx:**  
  - Será usado para guardar os registos dos cálculos realizados (data_hora, peso, medicamento, dosis, etc.).  
  - Este ficheiro é gerido automaticamente pelo código e pode ser consultado ou editado se necessário.

---

## Conclusão

Coloca todos os ficheiros na pasta **Safe-CALC** conforme descrito. Se seguires estes passos e carregares o projeto no GitHub (ou executares localmente com o comando `streamlit run app.py`), a tua aplicação deverá iniciar e apresentar a interface web de forma interativa.

Se encontrares algum erro ou tiveres dúvidas em algum passo, avisa que vou-te ajudar a identificar o que está a faltar ou a corrigir. Estou aqui para apoiar-te em cada passo!
