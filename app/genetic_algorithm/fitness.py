from typing import List, Dict
from datetime import datetime, timedelta

class FitnessCalculator:
    def __init__(self, mata_kuliah_dict, dosen_dict, ruangan_dict, preferensi_dict):
        self.mata_kuliah_dict = mata_kuliah_dict
        self.dosen_dict = dosen_dict
        self.ruangan_dict = ruangan_dict
        self.preferensi_dict = preferensi_dict
    
    def calculate(self, chromosome):
        """Hitung fitness dengan detail scoring"""
        total_fitness = 0
        details = []
        
        for i, gene in enumerate(chromosome.genes):
            score = 0
            reasons = []
            
            # Cek tabrakan waktu dosen
            no_dosen_conflict = self._check_no_dosen_conflict(gene, chromosome.genes, i)
            if no_dosen_conflict:
                score += 20
                reasons.append("Tidak ada tabrakan waktu dosen")
            else:
                score -= 50
                reasons.append("KONFLIK: Tabrakan waktu dosen")
            
            # Cek tabrakan ruangan
            no_ruangan_conflict = self._check_no_ruangan_conflict(gene, chromosome.genes, i)
            if no_ruangan_conflict:
                score += 20
                reasons.append("Tidak ada tabrakan ruangan")
            else:
                score -= 50
                reasons.append("KONFLIK: Tabrakan ruangan")
            
            # Cek kelas paralel tidak tumpang tindih
            no_parallel_conflict = self._check_no_parallel_conflict(gene, chromosome.genes, i)
            if no_parallel_conflict:
                score += 15
                reasons.append("Tidak ada kelas paralel bertumpuk")
            
            # Cek preferensi dosen
            if self._match_dosen_preference(gene):
                score += 5
                reasons.append("Sesuai preferensi dosen")
            
            # Cek kesesuaian ruangan
            if self._check_ruangan_facility(gene):
                score += 10
                reasons.append("Fasilitas ruangan sesuai")
            
            # Cek jadwal efisien (tidak terlalu pagi/malam)
            if self._is_efficient_time(gene):
                score += 5
                reasons.append("Waktu efisien")
            
            # Cek kapasitas ruangan
            if self._check_kapasitas(gene):
                score += 5
                reasons.append("Kapasitas ruangan mencukupi")
            else:
                score -= 15
                reasons.append("Kapasitas ruangan kurang")
            
            # Cek dosen tidak mengajar >3 jam berturut
            if not self._check_dosen_marathon(gene, chromosome.genes):
                score -= 10
                reasons.append("Dosen mengajar terlalu lama berturut-turut")
            
            matkul = self.mata_kuliah_dict.get(gene.matkul_id)
            detail = {
                "matkul": matkul.nama if matkul else f"ID-{gene.matkul_id}",
                "kode": matkul.kode if matkul else "",
                "penyebab": ", ".join(reasons),
                "skor": score
            }
            details.append(detail)
            total_fitness += score
        
        chromosome.fitness = total_fitness
        chromosome.fitness_details = details
        return total_fitness
    
    def _check_no_dosen_conflict(self, gene, all_genes, current_idx):
        """Cek tidak ada dosen yang mengajar di waktu bersamaan"""
        for i, other_gene in enumerate(all_genes):
            if i != current_idx and gene.dosen_id == other_gene.dosen_id:
                if gene.hari == other_gene.hari:
                    if self._time_overlap(gene.jam_mulai, gene.jam_selesai, 
                                        other_gene.jam_mulai, other_gene.jam_selesai):
                        return False
        return True
    
    def _check_no_ruangan_conflict(self, gene, all_genes, current_idx):
        """Cek tidak ada ruangan yang dipakai bersamaan"""
        for i, other_gene in enumerate(all_genes):
            if i != current_idx and gene.ruangan_id == other_gene.ruangan_id:
                if gene.hari == other_gene.hari:
                    if self._time_overlap(gene.jam_mulai, gene.jam_selesai,
                                        other_gene.jam_mulai, other_gene.jam_selesai):
                        return False
        return True
    
    def _check_no_parallel_conflict(self, gene, all_genes, current_idx):
        """Cek tidak ada mata kuliah semester sama bertumpuk"""
        matkul = self.mata_kuliah_dict.get(gene.matkul_id)
        if not matkul:
            return True
        
        for i, other_gene in enumerate(all_genes):
            if i != current_idx:
                other_matkul = self.mata_kuliah_dict.get(other_gene.matkul_id)
                if other_matkul and matkul.semester == other_matkul.semester:
                    if gene.hari == other_gene.hari:
                        if self._time_overlap(gene.jam_mulai, gene.jam_selesai,
                                            other_gene.jam_mulai, other_gene.jam_selesai):
                            return False
        return True
    
    def _match_dosen_preference(self, gene):
        """Cek apakah sesuai preferensi dosen"""
        preferensi_list = self.preferensi_dict.get(gene.dosen_id, [])
        for pref in preferensi_list:
            if pref.hari == gene.hari:
                if self._time_within(gene.jam_mulai, gene.jam_selesai,
                                   pref.jam_mulai, pref.jam_selesai):
                    return True
        return False
    
    def _check_ruangan_facility(self, gene):
        """Cek kesesuaian fasilitas ruangan"""
        ruangan = self.ruangan_dict.get(gene.ruangan_id)
        if not ruangan or not ruangan.fasilitas:
            return True
        
        # Cek apakah mata kuliah praktek butuh lab
        matkul = self.mata_kuliah_dict.get(gene.matkul_id)
        if matkul and "Praktikum" in matkul.nama:
            return "Lab" in ruangan.fasilitas or "Komputer" in ruangan.fasilitas
        return True
    
    def _is_efficient_time(self, gene):
        """Cek jadwal tidak terlalu pagi (<07:00) atau terlalu malam (>18:00)"""
        jam_mulai_int = int(gene.jam_mulai.split(":")[0])
        jam_selesai_int = int(gene.jam_selesai.split(":")[0])
        return 7 <= jam_mulai_int <= 17 and jam_selesai_int <= 19
    
    def _check_kapasitas(self, gene):
        """Cek kapasitas ruangan mencukupi (asumsi 30 mahasiswa per kelas)"""
        ruangan = self.ruangan_dict.get(gene.ruangan_id)
        if ruangan:
            return ruangan.kapasitas >= 30
        return True
    
    def _check_dosen_marathon(self, gene, all_genes):
        """Cek dosen tidak mengajar lebih dari 3 jam berturut-turut"""
        teaching_hours = []
        for other_gene in all_genes:
            if other_gene.dosen_id == gene.dosen_id and other_gene.hari == gene.hari:
                teaching_hours.append((other_gene.jam_mulai, other_gene.jam_selesai))
        
        # Sort by start time
        teaching_hours.sort()
        
        # Cek consecutive hours
        if len(teaching_hours) > 1:
            for i in range(len(teaching_hours) - 1):
                if teaching_hours[i][1] == teaching_hours[i+1][0]:
                    # Consecutive, hitung total
                    total_hours = self._calculate_duration(teaching_hours[i][0], teaching_hours[i+1][1])
                    if total_hours > 3:
                        return False
        return True
    
    def _time_overlap(self, start1, end1, start2, end2):
        """Cek apakah dua rentang waktu tumpang tindih"""
        start1_minutes = self._time_to_minutes(start1)
        end1_minutes = self._time_to_minutes(end1)
        start2_minutes = self._time_to_minutes(start2)
        end2_minutes = self._time_to_minutes(end2)
        
        return not (end1_minutes <= start2_minutes or end2_minutes <= start1_minutes)
    
    def _time_within(self, start, end, pref_start, pref_end):
        """Cek apakah waktu berada dalam preferensi"""
        start_minutes = self._time_to_minutes(start)
        end_minutes = self._time_to_minutes(end)
        pref_start_minutes = self._time_to_minutes(pref_start)
        pref_end_minutes = self._time_to_minutes(pref_end)
        
        return start_minutes >= pref_start_minutes and end_minutes <= pref_end_minutes
    
    def _calculate_duration(self, start, end):
        """Hitung durasi dalam jam"""
        start_minutes = self._time_to_minutes(start)
        end_minutes = self._time_to_minutes(end)
        return (end_minutes - start_minutes) / 60
    
    def _time_to_minutes(self, time_str):
        """Konversi string waktu ke menit"""
        hour, minute = map(int, time_str.split(":"))
        return hour * 60 + minute