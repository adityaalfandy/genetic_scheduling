from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.jadwal_service import JadwalService
from app.schemas.schemas import GenerateRequest, JadwalEdit
from app.models.jadwal import RiwayatGenerasi

router = APIRouter(prefix="/api/jadwal", tags=["jadwal"])

@router.post("/generate")
def generate_jadwal(request: GenerateRequest, db: Session = Depends(get_db)):
    """Generate jadwal menggunakan algoritma genetika"""
    try:
        best_chromosome, history = JadwalService.generate_jadwal(
            db,
            population_size=request.population_size,
            max_generations=request.max_generations,
            mutation_rate=request.mutation_rate
        )
        
        return {
            "message": "Jadwal berhasil digenerate",
            "fitness": best_chromosome.fitness,
            "generations": len(history),
            "fitness_history": history[-10:]  # Last 10 generations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
def get_jadwal(db: Session = Depends(get_db)):
    """Dapatkan semua jadwal"""
    try:
        jadwal_list = JadwalService.get_all_jadwal(db)
        return {"jadwal": jadwal_list, "total": len(jadwal_list)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/edit")
def edit_jadwal(data: JadwalEdit, db: Session = Depends(get_db)):
    """Edit jadwal manual"""
    try:
        jadwal, conflicts = JadwalService.edit_jadwal(
            db,
            jadwal_id=data.jadwal_id,
            hari=data.hari,
            jam_mulai=data.jam_mulai,
            jam_selesai=data.jam_selesai,
            ruangan_id=data.ruangan_id,
            dosen_id=data.dosen_id
        )
        
        return {
            "message": "Jadwal berhasil diupdate",
            "jadwal_id": jadwal.id,
            "conflicts": conflicts,
            "has_conflicts": len(conflicts) > 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/auto-fix")
def auto_fix(db: Session = Depends(get_db)):
    """Auto fix konflik jadwal menggunakan GA"""
    try:
        best_chromosome = JadwalService.auto_fix_conflicts(db)
        
        return {
            "message": "Konflik berhasil diperbaiki",
            "fitness": best_chromosome.fitness
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/fitness-explanation")
def get_fitness_explanation(db: Session = Depends(get_db)):
    """Dapatkan penjelasan fitness jadwal saat ini"""
    try:
        explanation = JadwalService.get_fitness_explanation(db)
        return explanation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    """Dapatkan riwayat generasi"""
    try:
        riwayat = db.query(RiwayatGenerasi).order_by(
            RiwayatGenerasi.id.desc()
        ).limit(10).all()
        
        results = []
        for r in riwayat:
            results.append({
                "id": r.id,
                "generation_number": r.generation_number,
                "best_fitness": r.best_fitness,
                "jadwal": r.json_jadwal
            })
        
        return {"riwayat": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))