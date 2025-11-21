from sqlalchemy import Column, Integer, String
from app.database import Base

class MataKuliah(Base):
    __tablename__ = "mata_kuliah"
    
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(100), nullable=False)
    kode = Column(String(20), unique=True, nullable=False)
    sks = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)