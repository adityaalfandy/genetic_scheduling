from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.data_service import DataService
from app.schemas.schemas import MataKuliahCreate, DosenCreate, RuanganCreate, PreferensiDosenCreate

router = APIRouter(prefix="/api/data", tags=["data"])

@router.post("/import-dummy")
def import_dummy_data(db: Session = Depends(get_db)):
    """Import data dummy untuk testing"""
    try:
        result = DataService.import_dummy_data(db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mata-kuliah")
def add_mata_kuliah(data: MataKuliahCreate, db: Session = Depends(get_db)):
    """Tambah mata kuliah"""
    try:
        matkul = DataService.add_mata_kuliah(db, data)
        return {"message": "Mata kuliah berhasil ditambahkan", "id": matkul.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/dosen")
def add_dosen(data: DosenCreate, db: Session = Depends(get_db)):
    """Tambah dosen"""
    try:
        dosen = DataService.add_dosen(db, data)
        return {"message": "Dosen berhasil ditambahkan", "id": dosen.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ruangan")
def add_ruangan(data: RuanganCreate, db: Session = Depends(get_db)):
    """Tambah ruangan"""
    try:
        ruangan = DataService.add_ruangan(db, data)
        return {"message": "Ruangan berhasil ditambahkan", "id": ruangan.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/preferensi-dosen")
def add_preferensi(data: PreferensiDosenCreate, db: Session = Depends(get_db)):
    """Tambah preferensi dosen"""
    try:
        pref = DataService.add_preferensi_dosen(db, data)
        return {"message": "Preferensi berhasil ditambahkan", "id": pref.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))