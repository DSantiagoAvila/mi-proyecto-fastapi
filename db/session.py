from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


USERNAME = "root"         
PASSWORD = ""              
HOST = "localhost"
PORT = "3306"
DATABASE = "resultados"  

# URL de conexión SQLAlchemy
DATABASE_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

# Crear el motor y la sesión
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependencia para inyectar la sesión en FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
