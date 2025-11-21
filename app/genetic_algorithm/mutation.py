import random

class Mutation:
    """Mutation operator untuk variasi genetik"""
    
    def __init__(self, dosen_list, ruangan_list):
        self.dosen_list = dosen_list
        self.ruangan_list = ruangan_list
        self.hari_options = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
        self.jam_options = [
            ("07:00", "09:00"), ("09:00", "11:00"), ("11:00", "13:00"),
            ("13:00", "15:00"), ("15:00", "17:00"), ("17:00", "19:00")
        ]
    
    def mutate(self, chromosome, mutation_rate):
        """Mutasi kromosom dengan probabilitas tertentu"""
        for gene in chromosome.genes:
            if random.random() < mutation_rate:
                mutation_type = random.choice(['time', 'room', 'dosen', 'day'])
                
                if mutation_type == 'time':
                    # Mutasi waktu
                    jam_mulai, jam_selesai = random.choice(self.jam_options)
                    gene.jam_mulai = jam_mulai
                    gene.jam_selesai = jam_selesai
                
                elif mutation_type == 'room':
                    # Mutasi ruangan
                    gene.ruangan_id = random.choice(self.ruangan_list).id
                
                elif mutation_type == 'dosen':
                    # Mutasi dosen
                    gene.dosen_id = random.choice(self.dosen_list).id
                
                elif mutation_type == 'day':
                    # Mutasi hari
                    gene.hari = random.choice(self.hari_options)
        
        return chromosome
    
    def smart_mutate(self, chromosome, mutation_rate, fitness_calculator):
        """Mutasi cerdas: fokus pada gen dengan fitness rendah"""
        # Identifikasi gen dengan score rendah
        low_score_indices = []
        for i, detail in enumerate(chromosome.fitness_details):
            if detail['skor'] < 0:
                low_score_indices.append(i)
        
        # Mutasi gen dengan score rendah lebih agresif
        for i in low_score_indices:
            if random.random() < mutation_rate * 2:  # 2x lebih besar
                gene = chromosome.genes[i]
                mutation_type = random.choice(['time', 'room', 'day'])
                
                if mutation_type == 'time':
                    jam_mulai, jam_selesai = random.choice(self.jam_options)
                    gene.jam_mulai = jam_mulai
                    gene.jam_selesai = jam_selesai
                elif mutation_type == 'room':
                    gene.ruangan_id = random.choice(self.ruangan_list).id
                elif mutation_type == 'day':
                    gene.hari = random.choice(self.hari_options)
        
        # Mutasi normal untuk gen lainnya
        for i, gene in enumerate(chromosome.genes):
            if i not in low_score_indices and random.random() < mutation_rate:
                mutation_type = random.choice(['time', 'room'])
                if mutation_type == 'time':
                    jam_mulai, jam_selesai = random.choice(self.jam_options)
                    gene.jam_mulai = jam_mulai
                    gene.jam_selesai = jam_selesai
                elif mutation_type == 'room':
                    gene.ruangan_id = random.choice(self.ruangan_list).id
        
        return chromosome