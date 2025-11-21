from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class MataKuliahCreate(BaseModel):
    nama: str
    kode: str
    sks: int
    semester: int

class DosenCreate(BaseModel):
    nama: str
    preferensi_waktu: Optional[str] = None

class RuanganCreate(BaseModel):
    nama: str
    kapasitas: int
    fasilitas: Optional[str] = None

class PreferensiDosenCreate(BaseModel):
    dosen_id: int
    hari: str
    jam_mulai: str
    jam_selesai: str

class JadwalResponse(BaseModel):
    id: int
    matkul_nama: str
    matkul_kode: str
    dosen_nama: str
    ruangan_nama: str
    hari: str
    jam_mulai: str
    jam_selesai: str
    
    class Config:
        from_attributes = True

class JadwalEdit(BaseModel):
    jadwal_id: int
    hari: Optional[str] = None
    jam_mulai: Optional[str] = None
    jam_selesai: Optional[str] = None
    ruangan_id: Optional[int] = None
    dosen_id: Optional[int] = None

class FitnessExplanation(BaseModel):
    fitness_total: int
    penjelasan: List[Dict[str, Any]]

class GenerateRequest(BaseModel):
    population_size: int = 50
    max_generations: int = 100
    mutation_rate: float = 0.1