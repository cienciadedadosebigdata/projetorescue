import os
from openai import OpenAI

# Configurando a chave da API da OpenAI
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Substitua "your_prompt_here" pelo seu prompt específico para análise
your_prompt_here = "Por favor, analise os seguintes dados: ..."

# Criando uma conclusão de chat com GPT-4
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": your_prompt_here,
        }
    ],
    model="gpt-4",  # Substitua "gpt-4" pelo modelo exato se necessário
)

# Exibindo a resposta
print(chat_completion.choices[0].message.content)
