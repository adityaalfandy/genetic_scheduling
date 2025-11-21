from app.genetic_algorithm.chromosome import Chromosome
from app.genetic_algorithm.fitness import FitnessCalculator
from app.genetic_algorithm.selection import TournamentSelection
from app.genetic_algorithm.crossover import Crossover
from app.genetic_algorithm.mutation import Mutation
import random

class Population:
    """Kelola populasi kromosom"""
    
    def __init__(self, mata_kuliah_list, dosen_list, ruangan_list, 
                 preferensi_dict, population_size=50):
        self.mata_kuliah_list = mata_kuliah_list
        self.dosen_list = dosen_list
        self.ruangan_list = ruangan_list
        self.preferensi_dict = preferensi_dict
        self.population_size = population_size
        self.chromosomes = []
        
        # Setup dictionaries untuk fitness calculator
        self.mata_kuliah_dict = {mk.id: mk for mk in mata_kuliah_list}
        self.dosen_dict = {d.id: d for d in dosen_list}
        self.ruangan_dict = {r.id: r for r in ruangan_list}
        
        self.fitness_calculator = FitnessCalculator(
            self.mata_kuliah_dict, self.dosen_dict, 
            self.ruangan_dict, preferensi_dict
        )
        self.selector = TournamentSelection(tournament_size=3)
        self.mutation = Mutation(dosen_list, ruangan_list)
    
    def initialize(self):
        """Inisialisasi populasi random"""
        self.chromosomes = []
        for _ in range(self.population_size):
            chromosome = Chromosome.create_random(
                self.mata_kuliah_list, self.dosen_list, self.ruangan_list
            )
            self.chromosomes.append(chromosome)
        self.evaluate_fitness()
    
    def evaluate_fitness(self):
        """Hitung fitness semua kromosom"""
        for chromosome in self.chromosomes:
            self.fitness_calculator.calculate(chromosome)
    
    def get_best_chromosome(self):
        """Dapatkan kromosom terbaik"""
        if not self.chromosomes:
            return None
        return max(self.chromosomes, key=lambda x: x.fitness)
    
    def evolve(self, mutation_rate=0.1, elitism_count=2):
        """Evolusi satu generasi"""
        new_population = []
        
        # Elitism: simpan N kromosom terbaik
        sorted_population = sorted(self.chromosomes, key=lambda x: x.fitness, reverse=True)
        new_population.extend([c.copy() for c in sorted_population[:elitism_count]])
        
        # Buat offspring sampai populasi penuh
        while len(new_population) < self.population_size:
            # Seleksi parent
            parent1 = self.selector.select(self.chromosomes)
            parent2 = self.selector.select(self.chromosomes)
            
            # Crossover
            if random.random() < 0.8:  # 80% crossover rate
                child1, child2 = Crossover.two_point_crossover(parent1, parent2)
            else:
                child1 = parent1.copy()
                child2 = parent2.copy()
            
            # Mutasi
            child1 = self.mutation.mutate(child1, mutation_rate)
            child2 = self.mutation.mutate(child2, mutation_rate)
            
            new_population.append(child1)
            if len(new_population) < self.population_size:
                new_population.append(child2)
        
        self.chromosomes = new_population[:self.population_size]
        self.evaluate_fitness()
    
    def run_genetic_algorithm(self, max_generations=100, mutation_rate=0.1, 
                            target_fitness=None, verbose=True):
        """Jalankan algoritma genetika"""
        self.initialize()
        
        best_fitness_history = []
        
        for generation in range(max_generations):
            self.evolve(mutation_rate)
            
            best = self.get_best_chromosome()
            best_fitness_history.append(best.fitness)
            
            if verbose and generation % 10 == 0:
                print(f"Generation {generation}: Best Fitness = {best.fitness}")
            
            # Early stopping jika mencapai target
            if target_fitness and best.fitness >= target_fitness:
                if verbose:
                    print(f"Target fitness reached at generation {generation}")
                break
        
        return self.get_best_chromosome(), best_fitness_history