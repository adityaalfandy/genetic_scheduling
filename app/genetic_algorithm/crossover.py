import random
from app.genetic_algorithm.chromosome import Chromosome, Gene

class Crossover:
    """Crossover operator untuk menghasilkan offspring"""
    
    @staticmethod
    def two_point_crossover(parent1, parent2):
        """Two-point crossover: tukar sebagian gen antara dua parent"""
        if len(parent1) < 2:
            return parent1.copy(), parent2.copy()
        
        point1 = random.randint(0, len(parent1) - 1)
        point2 = random.randint(point1, len(parent1) - 1)
        
        child1_genes = []
        child2_genes = []
        
        for i in range(len(parent1)):
            if point1 <= i <= point2:
                # Swap genes
                gene1 = parent2[i]
                gene2 = parent1[i]
            else:
                gene1 = parent1[i]
                gene2 = parent2[i]
            
            # Copy genes
            child1_genes.append(Gene(gene1.matkul_id, gene1.dosen_id, gene1.ruangan_id,
                                    gene1.hari, gene1.jam_mulai, gene1.jam_selesai))
            child2_genes.append(Gene(gene2.matkul_id, gene2.dosen_id, gene2.ruangan_id,
                                    gene2.hari, gene2.jam_mulai, gene2.jam_selesai))
        
        return Chromosome(child1_genes), Chromosome(child2_genes)
    
    @staticmethod
    def uniform_crossover(parent1, parent2):
        """Uniform crossover: setiap gen dipilih random dari parent1 atau parent2"""
        child1_genes = []
        child2_genes = []
        
        for i in range(len(parent1)):
            if random.random() < 0.5:
                gene1 = parent1[i]
                gene2 = parent2[i]
            else:
                gene1 = parent2[i]
                gene2 = parent1[i]
            
            child1_genes.append(Gene(gene1.matkul_id, gene1.dosen_id, gene1.ruangan_id,
                                    gene1.hari, gene1.jam_mulai, gene1.jam_selesai))
            child2_genes.append(Gene(gene2.matkul_id, gene2.dosen_id, gene2.ruangan_id,
                                    gene2.hari, gene2.jam_mulai, gene2.jam_selesai))
        
        return Chromosome(child1_genes), Chromosome(child2_genes)