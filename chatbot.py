import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.memory import ConversationBufferMemory

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
database_url = os.getenv("DATABASE_URL")
if not os.getenv("OPENAI_API_KEY") and os.getenv("DATABASE_URL"):
    raise ValueError("OPENAI_API_KEY ou DATABASE_URL não encontrado no .env")


database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url)
db = SQLDatabase(engine)

llm = ChatOpenAI(model="gpt-4o-mini",temperature=0,api_key=api_key)
conversatio_memory = ConversationBufferMemory(
    memory_key='chat_history',
    return_messages=True
)
print("LLM e db configurados")

toolkit = SQLDatabaseToolkit(db=db,llm=llm)

agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type="openai-tools",
    prefix="Você é um assientente AI para o banco de dados SistemaPontos que contem dados sobre clientes,produtos e transaçoes desses clientes. Tente sempre ver somente o necessário",
    memory=conversatio_memory

)

print("Agente SQL criado")

def ask_bot(question):

    try:
        response = agent_executor.invoke({"input":question})
        return response['output']
    except Exception as e:
        return f"Ocorreu um erro: {e}"
    
if __name__ == "__main__":
    print("\nChatbot SQL pronto! Faça suas perguntas (digite 'sair' para terminar).")
    while True:
        user_query = input("Você: ")

        if user_query.lower() == 'sair':
            break
        bot_response = ask_bot(user_query)
        print(f"Bot: {bot_response}")