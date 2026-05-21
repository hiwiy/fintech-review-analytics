import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")

engine = create_engine(DATABASE_URL)

with open("schema.sql", "r", encoding="utf-8") as file:
    schema_sql = file.read()

with engine.begin() as conn:
    conn.execute(text(schema_sql))

print("Tables created successfully in Neon PostgreSQL.")