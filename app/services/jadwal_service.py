from sqlalchemy.orm import Session
from app.models.jadwal import Jadwal, RiwayatGenerasi
from app.models.mata_kuliah import MataKuliah
from app.models.dosen import Dosen, PreferensiDosen
from app.models.ruangan import Ruangan
from app.genetic_algorithm.population import Population
from app.genetic_algorithm.chromosome import Chromosome, Gene
from app.genetic_algorithm.fitness import FitnessCalculator
import json

class JadwalService:
    
    @staticmethod
    def generate_jadwal(db: Session, population_size=50, max_generations=100, 
                       mutation_rate=0.1):
        """Generate jadwal menggunakan GA"""
        # Ambil data dari database
        mata_kuliah_list = db.query(MataKuliah).all()
        dosen_list = db.query(Dosen).all()
        ruangan_list = db.query(Ruangan).all()
        
        if not mata_kuliah_list or not dosen_list or not ruangan_list:
            raise ValueError("Data mata kuliah, dosen, atau ruangan kosong")
        
        # Ambil preferensi dosen
        preferensi_dict = {}
        for dosen in dosen_list:
            prefs = db.query(PreferensiDosen).filter(
                PreferensiDosen.dosen_id == dosen.id
            ).all()
            preferensi_dict[dosen.id] = prefs
        
        # Jalankan GA
        pop = Population(mata_kuliah_list, dosen_list, ruangan_list, 
                        preferensi_dict, population_size)
        best_chromosome, history = pop.run_genetic_algorithm(
            max_generations=max_generations, 
            mutation_rate=mutation_rate,
            verbose=True
        )
        
        # Simpan ke database
        JadwalService._save_jadwal(db, best_chromosome, pop)
        
        # Simpan riwayat
        jadwal_json = JadwalService._chromosome_to_json(best_chromosome, pop)
        riwayat = RiwayatGenerasi(
            generation_number=len(history),
            best_fitness=best_chromosome.fitness,
            json_jadwal=jadwal_json
        )
        db.add(riwayat)
        db.commit()
        
        return best_chromosome, history
    
    @staticmethod
    def _save_jadwal(db: Session, chromosome, population):
        """Simpan jadwal ke database"""
        # Hapus jadwal lama
        db.query(Jadwal).delete()
        db.commit()
        
        # Simpan jadwal baru
        for gene in chromosome.genes:
            jadwal = Jadwal(
                matkul_id=gene.matkul_id,
                dosen_id=gene.dosen_id,
                ruangan_id=gene.ruangan_id,
                hari=gene.hari,
                jam_mulai=gene.jam_mulai,
                jam_selesai=gene.jam_selesai
            )
            db.add(jadwal)
        
        db.commit()
    
    @staticmethod
    def _chromosome_to_json(chromosome, population):
        """Konversi kromosom ke JSON"""
        jadwal_list = []
        for gene in chromosome.genes:
            matkul = population.mata_kuliah_dict.get(gene.matkul_id)
            dosen = population.dosen_dict.get(gene.dosen_id)
            ruangan = population.ruangan_dict.get(gene.ruangan_id)
            
            jadwal_list.append({
                "matkul": matkul.nama if matkul else "",
                "kode": matkul.kode if matkul else "",
                "dosen": dosen.nama if dosen else "",
                "ruangan": ruangan.nama if ruangan else "",
                "hari": gene.hari,
                "jam_mulai": gene.jam_mulai,
                "jam_selesai": gene.jam_selesai
            })
        
        return {"jadwal": jadwal_list, "fitness": chromosome.fitness}
    
    @staticmethod
    def get_all_jadwal(db: Session):
        """Ambil semua jadwal"""
        jadwal_list = db.query(Jadwal).all()
        results = []
        
        for jadwal in jadwal_list:
            results.append({
                "id": jadwal.id,
                "matkul_nama": jadwal.mata_kuliah.nama,
                "matkul_kode": jadwal.mata_kuliah.kode,
                "dosen_nama": jadwal.dosen.nama,
                "ruangan_nama": jadwal.ruangan.nama,
                "hari": jadwal.hari,
                "jam_mulai": jadwal.jam_mulai,
                "jam_selesai": jadwal.jam_selesai
            })
        
        return results
    
    @staticmethod
    def edit_jadwal(db: Session, jadwal_id: int, hari=None, jam_mulai=None, 
                   jam_selesai=None, ruangan_id=None, dosen_id=None):
        """Edit jadwal secara manual"""
        jadwal = db.query(Jadwal).filter(Jadwal.id == jadwal_id).first()
        if not jadwal:
            raise ValueError("Jadwal tidak ditemukan")
        
        # Update fields
        if hari:
            jadwal.hari = hari
        if jam_mulai:
            jadwal.jam_mulai = jam_mulai
        if jam_selesai:
            jadwal.jam_selesai = jam_selesai
        if ruangan_id:
            jadwal.ruangan_id = ruangan_id
        if dosen_id:
            jadwal.dosen_id = dosen_id
        
        db.commit()
        
        # Cek konflik
        conflicts = JadwalService._check_conflicts(db, jadwal)
        
        return jadwal, conflicts
    
    @staticmethod
    def _check_conflicts(db: Session, jadwal):
        """Cek konflik jadwal"""
        conflicts = []
        
        # Cek konflik dosen
        dosen_conflicts = db.query(Jadwal).filter(
            Jadwal.id != jadwal.id,
            Jadwal.dosen_id == jadwal.dosen_id,
            Jadwal.hari == jadwal.hari
        ).all()
        
        for dc in dosen_conflicts:
            if JadwalService._time_overlap(jadwal.jam_mulai, jadwal.jam_selesai,
                                          dc.jam_mulai, dc.jam_selesai):
                conflicts.append({
                    "type": "dosen",
                    "jadwal_id": dc.id,
                    "message": f"Dosen {jadwal.dosen.nama} bentrok dengan {dc.mata_kuliah.nama}"
                })
        
        # Cek konflik ruangan
        ruangan_conflicts = db.query(Jadwal).filter(
            Jadwal.id != jadwal.id,
            Jadwal.ruangan_id == jadwal.ruangan_id,
            Jadwal.hari == jadwal.hari
        ).all()
        
        for rc in ruangan_conflicts:
            if JadwalService._time_overlap(jadwal.jam_mulai, jadwal.jam_selesai,
                                          rc.jam_mulai, rc.jam_selesai):
                conflicts.append({
                    "type": "ruangan",
                    "jadwal_id": rc.id,
                    "message": f"Ruangan {jadwal.ruangan.nama} bentrok dengan {rc.mata_kuliah.nama}"
                })
        
        return conflicts
    
    @staticmethod
    def auto_fix_conflicts(db: Session, jadwal_ids=None):
        """Auto fix konflik menggunakan GA fokus pada jadwal bermasalah"""
        # Ambil semua data
        mata_kuliah_list = db.query(MataKuliah).all()
        dosen_list = db.query(Dosen).all()
        ruangan_list = db.query(Ruangan).all()
        
        # Ambil preferensi dosen
        preferensi_dict = {}
        for dosen in dosen_list:
            prefs = db.query(PreferensiDosen).filter(
                PreferensiDosen.dosen_id == dosen.id
            ).all()
            preferensi_dict[dosen.id] = prefs
        
        # Setup dictionaries
        mata_kuliah_dict = {mk.id: mk for mk in mata_kuliah_list}
        dosen_dict = {d.id: d for d in dosen_list}
        ruangan_dict = {r.id: r for r in ruangan_list}
        
        # Buat chromosome dari jadwal saat ini
        current_jadwal = db.query(Jadwal).all()
        genes = []
        for j in current_jadwal:
            gene = Gene(j.matkul_id, j.dosen_id, j.ruangan_id, 
                       j.hari, j.jam_mulai, j.jam_selesai)
            genes.append(gene)
        
        current_chromosome = Chromosome(genes)
        
        # Jalankan GA dengan populasi kecil fokus pada perbaikan
        pop = Population(mata_kuliah_list, dosen_list, ruangan_list,
                        preferensi_dict, population_size=20)
        pop.chromosomes = [current_chromosome]
        
        # Tambah variasi
        for _ in range(19):
            variant = current_chromosome.copy()
            pop.mutation.smart_mutate(variant, 0.3, pop.fitness_calculator)
            pop.chromosomes.append(variant)
        
        # Evolusi fokus pada perbaikan konflik
        for _ in range(50):
            pop.evolve(mutation_rate=0.2, elitism_count=1)
        
        best = pop.get_best_chromosome()
        
        # Simpan hasil
        JadwalService._save_jadwal(db, best, pop)
        
        return best
    
    @staticmethod
    def get_fitness_explanation(db: Session):
        """Dapatkan penjelasan fitness jadwal saat ini"""
        jadwal_list = db.query(Jadwal).all()
        if not jadwal_list:
            return {"fitness_total": 0, "penjelasan": []}
        
        # Buat chromosome dari jadwal
        mata_kuliah_list = db.query(MataKuliah).all()
        dosen_list = db.query(Dosen).all()
        ruangan_list = db.query(Ruangan).all()
        
        preferensi_dict = {}
        for dosen in dosen_list:
            prefs = db.query(PreferensiDosen).filter(
                PreferensiDosen.dosen_id == dosen.id
            ).all()
            preferensi_dict[dosen.id] = prefs
        
        mata_kuliah_dict = {mk.id: mk for mk in mata_kuliah_list}
        dosen_dict = {d.id: d for d in dosen_list}
        ruangan_dict = {r.id: r for r in ruangan_list}
        
        genes = []
        for j in jadwal_list:
            gene = Gene(j.matkul_id, j.dosen_id, j.ruangan_id,
                       j.hari, j.jam_mulai, j.jam_selesai)
            genes.append(gene)
        
        chromosome = Chromosome(genes)
        
        # Hitung fitness
        fitness_calc = FitnessCalculator(mata_kuliah_dict, dosen_dict,
                                        ruangan_dict, preferensi_dict)
        fitness_calc.calculate(chromosome)
        
        return {
            "fitness_total": chromosome.fitness,
            "penjelasan": chromosome.fitness_details
        }
    
    @staticmethod
    def _time_overlap(start1, end1, start2, end2):
        """Cek overlap waktu"""
        def time_to_minutes(time_str):
            hour, minute = map(int, time_str.split(":"))
            return hour * 60 + minute
        
        start1_m = time_to_minutes(start1)
        end1_m = time_to_minutes(end1)
        start2_m = time_to_minutes(start2)
        end2_m = time_to_minutes(end2)
        
        return not (end1_m <= start2_m or end2_m <= start1_m)