from sqlalchemy import Column, Integer, String
from db.session import Base

class Proceso(Base):
    __tablename__ = "procesos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  
    value = Column(Integer, nullable=False)
    category = Column(String(10), nullable=False)