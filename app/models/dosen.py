from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Dosen(Base):
    __tablename__ = "dosen"
    
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(100), nullable=False)
    preferensi_waktu = Column(String(255), nullable=True)
    
    preferensi = relationship("PreferensiDosen", back_populates="dosen", cascade="all, delete-orphan")
    jadwal = relationship("Jadwal", back_populates="dosen")

class PreferensiDosen(Base):
    __tablename__ = "preferensi_dosen"
    
    id = Column(Integer, primary_key=True, index=True)
    dosen_id = Column(Integer, ForeignKey("dosen.id", ondelete="CASCADE"))
    hari = Column(String(20), nullable=False)
    jam_mulai = Column(String(10), nullable=False)
    jam_selesai = Column(String(10), nullable=False)
    
    dosen = relationship("Dosen", back_populates="preferensi")