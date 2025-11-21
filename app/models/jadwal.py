from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class Jadwal(Base):
    __tablename__ = "jadwal"
    
    id = Column(Integer, primary_key=True, index=True)
    matkul_id = Column(Integer, ForeignKey("mata_kuliah.id"))
    dosen_id = Column(Integer, ForeignKey("dosen.id"))
    ruangan_id = Column(Integer, ForeignKey("ruangan.id"))
    hari = Column(String(20), nullable=False)
    jam_mulai = Column(String(10), nullable=False)
    jam_selesai = Column(String(10), nullable=False)
    
    mata_kuliah = relationship("MataKuliah")
    dosen = relationship("Dosen", back_populates="jadwal")
    ruangan = relationship("Ruangan", back_populates="jadwal")

class RiwayatGenerasi(Base):
    __tablename__ = "riwayat_generasi"
    
    id = Column(Integer, primary_key=True, index=True)
    generation_number = Column(Integer, nullable=False)
    best_fitness = Column(Integer, nullable=False)
    json_jadwal = Column(JSON, nullable=False)