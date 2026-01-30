from database_data_connection.data_connection import user, password, server, port, database
from sqlalchemy import create_engine, pool
from sqlalchemy.orm import sessionmaker, declarative_base
import os


#DATABASE_URL = f"postgresql://{user}:{password}@{server}:{port}/{database}"
#DATABASE_URL = "postgresql://myuser:superpass@dpg-abcd1234-a.oregon-postgres.render.com:5432/mydb"
#DATABASE_URL = "postgresql://myuser:superpass@dpg-abcd1234-a.oregon-postgres.render.com:5432/mydb?sslmode=require"
DATABASE_URL = os.getenv("DATABASE_URL")



engine = create_engine(DATABASE_URL)

sessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
#sesion = sessionLocal()