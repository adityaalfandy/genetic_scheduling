from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Ruangan(Base):
    __tablename__ = "ruangan"
    
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(50), nullable=False)
    kapasitas = Column(Integer, nullable=False)
    fasilitas = Column(String(255), nullable=True)
    
    jadwal = relationship("Jadwal", back_populates="ruangan")