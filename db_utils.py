import os
from sqlalchemy import inspect
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

database_url = os.getenv("DATABASE_URL")

def get_engine():
    return create_engine()

def print_schema(engine):

    inspector = inspect(engine)
    schemas = inspector.get_schema_names()
    print(f"Schemas: {schemas}")

    for table_name in inspector.get_table_names(schema='main'):
        print(f"\nTable: {table_name}")
        columns = inspector.get_columns(table_name,schema='main')

        for column in columns:
            print(f"  Colum: {column['name']} ({column['type']})")


if __name__ == "__main__":
    engine = get_engine()
    try:
        conn = engine.connect()
        print("Conexão com banco de dados bem sucedida")
        print_schema(engine)
        conn.close()

    except Exception as e:
        print(f"Erro ao conectar ou inspecionar o banco de dados: {e}")