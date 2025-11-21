from sqlalchemy.orm import Session
from app.models.mata_kuliah import MataKuliah
from app.models.dosen import Dosen, PreferensiDosen
from app.models.ruangan import Ruangan
from app.schemas.schemas import MataKuliahCreate, DosenCreate, RuanganCreate, PreferensiDosenCreate

class DataService:
    
    @staticmethod
    def add_mata_kuliah(db: Session, data: MataKuliahCreate):
        """Tambah mata kuliah"""
        matkul = MataKuliah(**data.dict())
        db.add(matkul)
        db.commit()
        db.refresh(matkul)
        return matkul
    
    @staticmethod
    def add_dosen(db: Session, data: DosenCreate):
        """Tambah dosen"""
        dosen = Dosen(**data.dict())
        db.add(dosen)
        db.commit()
        db.refresh(dosen)
        return dosen
    
    @staticmethod
    def add_ruangan(db: Session, data: RuanganCreate):
        """Tambah ruangan"""
        ruangan = Ruangan(**data.dict())
        db.add(ruangan)
        db.commit()
        db.refresh(ruangan)
        return ruangan
    
    @staticmethod
    def add_preferensi_dosen(db: Session, data: PreferensiDosenCreate):
        """Tambah preferensi dosen"""
        preferensi = PreferensiDosen(**data.dict())
        db.add(preferensi)
        db.commit()
        db.refresh(preferensi)
        return preferensi
    
    @staticmethod
    def import_dummy_data(db: Session):
        """Import data dummy untuk testing"""
        # Clear existing data
        db.query(PreferensiDosen).delete()
        db.query(Dosen).delete()
        db.query(MataKuliah).delete()
        db.query(Ruangan).delete()
        db.commit()
        
        # Mata Kuliah
        mata_kuliah_data = [
            {"nama": "Struktur Data dan Algoritma", "kode": "CS101", "sks": 3, "semester": 3},
            {"nama": "Basis Data", "kode": "CS102", "sks": 3, "semester": 3},
            {"nama": "Pemrograman Web", "kode": "CS103", "sks": 3, "semester": 4},
            {"nama": "Kalkulus I", "kode": "MTK101", "sks": 3, "semester": 1},
            {"nama": "Fisika Dasar", "kode": "FIS101", "sks": 3, "semester": 1},
            {"nama": "Praktikum Basis Data", "kode": "CS102P", "sks": 1, "semester": 3},
            {"nama": "Jaringan Komputer", "kode": "CS104", "sks": 3, "semester": 4},
            {"nama": "Sistem Operasi", "kode": "CS105", "sks": 3, "semester": 4},
        ]
        
        for mk_data in mata_kuliah_data:
            matkul = MataKuliah(**mk_data)
            db.add(matkul)
        
        db.commit()
        
        # Dosen
        dosen_data = [
            {"nama": "Dr. Ahmad Fauzi", "preferensi_waktu": "Senin-Rabu pagi"},
            {"nama": "Dr. Siti Nurhaliza", "preferensi_waktu": "Selasa-Kamis"},
            {"nama": "Prof. Budi Santoso", "preferensi_waktu": "Senin-Jumat"},
            {"nama": "Dr. Rina Wijaya", "preferensi_waktu": "Rabu-Jumat"},
            {"nama": "Dr. Eko Prasetyo", "preferensi_waktu": "Senin-Kamis"},
        ]
        
        for d_data in dosen_data:
            dosen = Dosen(**d_data)
            db.add(dosen)
        
        db.commit()
        
        # Preferensi Dosen
        dosen_list = db.query(Dosen).all()
        preferensi_data = [
            {"dosen_id": dosen_list[0].id, "hari": "Senin", "jam_mulai": "07:00", "jam_selesai": "12:00"},
            {"dosen_id": dosen_list[0].id, "hari": "Rabu", "jam_mulai": "07:00", "jam_selesai": "12:00"},
            {"dosen_id": dosen_list[1].id, "hari": "Selasa", "jam_mulai": "09:00", "jam_selesai": "17:00"},
            {"dosen_id": dosen_list[1].id, "hari": "Kamis", "jam_mulai": "09:00", "jam_selesai": "17:00"},
            {"dosen_id": dosen_list[2].id, "hari": "Senin", "jam_mulai": "07:00", "jam_selesai": "17:00"},
            {"dosen_id": dosen_list[3].id, "hari": "Rabu", "jam_mulai": "13:00", "jam_selesai": "17:00"},
            {"dosen_id": dosen_list[3].id, "hari": "Jumat", "jam_mulai": "09:00", "jam_selesai": "15:00"},
        ]
        
        for pref_data in preferensi_data:
            pref = PreferensiDosen(**pref_data)
            db.add(pref)
        
        db.commit()
        
        # Ruangan
        ruangan_data = [
            {"nama": "A101", "kapasitas": 40, "fasilitas": "Proyektor, AC"},
            {"nama": "A102", "kapasitas": 35, "fasilitas": "Proyektor, AC, Whiteboard"},
            {"nama": "Lab Komputer 1", "kapasitas": 30, "fasilitas": "Komputer, Proyektor, AC"},
            {"nama": "Lab Komputer 2", "kapasitas": 30, "fasilitas": "Komputer, Proyektor, AC"},
            {"nama": "B201", "kapasitas": 50, "fasilitas": "Proyektor, AC, Sound System"},
            {"nama": "B202", "kapasitas": 45, "fasilitas": "Proyektor, AC"},
            {"nama": "C301", "kapasitas": 30, "fasilitas": "Whiteboard, AC"},
        ]
        
        for r_data in ruangan_data:
            ruangan = Ruangan(**r_data)
            db.add(ruangan)
        
        db.commit()
        
        return {"message": "Data dummy berhasil diimport"}