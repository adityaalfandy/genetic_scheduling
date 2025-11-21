import random
from typing import List, Dict

class Gene:
    """Representasi satu jadwal mata kuliah"""
    def __init__(self, matkul_id: int, dosen_id: int, ruangan_id: int, 
                 hari: str, jam_mulai: str, jam_selesai: str):
        self.matkul_id = matkul_id
        self.dosen_id = dosen_id
        self.ruangan_id = ruangan_id
        self.hari = hari
        self.jam_mulai = jam_mulai
        self.jam_selesai = jam_selesai
    
    def __repr__(self):
        return f"Gene(matkul={self.matkul_id}, dosen={self.dosen_id}, ruangan={self.ruangan_id}, {self.hari} {self.jam_mulai}-{self.jam_selesai})"

class Chromosome:
    """Representasi satu solusi jadwal lengkap"""
    def __init__(self, genes: List[Gene] = None):
        self.genes = genes if genes else []
        self.fitness = 0
        self.fitness_details = []
    
    def __len__(self):
        return len(self.genes)
    
    def __getitem__(self, index):
        return self.genes[index]
    
    def __setitem__(self, index, value):
        self.genes[index] = value
    
    def copy(self):
        """Deep copy kromosom"""
        new_genes = []
        for g in self.genes:
            new_gene = Gene(g.matkul_id, g.dosen_id, g.ruangan_id, 
                          g.hari, g.jam_mulai, g.jam_selesai)
            new_genes.append(new_gene)
        return Chromosome(new_genes)
    
    @staticmethod
    def create_random(mata_kuliah_list, dosen_list, ruangan_list):
        """Buat kromosom random"""
        genes = []
        hari_options = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
        jam_options = [
            ("07:00", "09:00"), ("09:00", "11:00"), ("11:00", "13:00"),
            ("13:00", "15:00"), ("15:00", "17:00"), ("17:00", "19:00")
        ]
        
        for mk in mata_kuliah_list:
            dosen = random.choice(dosen_list)
            ruangan = random.choice(ruangan_list)
            hari = random.choice(hari_options)
            jam_mulai, jam_selesai = random.choice(jam_options)
            
            gene = Gene(mk.id, dosen.id, ruangan.id, hari, jam_mulai, jam_selesai)
            genes.append(gene)
        
        return Chromosome(genes)