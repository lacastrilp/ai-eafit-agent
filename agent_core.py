import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Cargar variables de entorno
load_dotenv()

# 2. Inicializar el modelo Groq Llama 3
llm = ChatGroq(
    model="llama-3.1-8b-instant",  # ✅ modelo actualizado
    temperature=0.3
)

# 3. Crear el prompt moderno
prompt = ChatPromptTemplate.from_template(
    """Eres un asistente útil y amigable.
Historial:
{history}

Usuario: {question}

Responde de manera natural y útil, en español."""
)

# 4. Crear el parser de salida
parser = StrOutputParser()

# 5. Combinar en una cadena (pipe operator)
chain = prompt | llm | parser

# 6. Función para invocar la IA
def invoke_agent(user_input, chat_history_messages):
    """
    Invoca al modelo con historial de chat.
    Compatible con LangChain 1.0.x y ChatGroq.
    """
    # Convertir historial a texto
    history_text = "\n".join(
        f"{m.type.upper()}: {m.content}" for m in chat_history_messages
    )

    try:
        response = chain.invoke({
            "history": history_text,
            "question": user_input
        })
        return response.strip()
    except Exception as e:
        import traceback
        print("[Error invoke_agent]:", e)
        traceback.print_exc()  # 🔥 esto imprime el stack completo
        return "⚠️ Ocurrió un error al procesar tu solicitud."
