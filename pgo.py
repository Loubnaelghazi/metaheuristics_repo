import math
import random

#  convertir les coordonnées en radians
def to_radians(degrees):
    return degrees * math.pi / 180

#  calculer la distance géographique entre deux points
def geo_distance(coord1, coord2):
    R = 6371.0  # Rayon de la Terre en kilomètres
    lat1, lon1 = to_radians(coord1[0]), to_radians(coord1[1])
    lat2, lon2 = to_radians(coord2[0]), to_radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

# Chargement des données du fichier TSP
def load_tsp_data(file_path):
    node_coordinates = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        start_reading = False
        for line in lines:
            if line.startswith('NODE_COORD_SECTION'):
                start_reading = True
                continue
            if line.startswith('EOF'):
                break
            if start_reading:
                parts = line.strip().split()
                x_coord = float(parts[1])
                y_coord = float(parts[2])
                node_coordinates.append((x_coord, y_coord))
    return node_coordinates

# Calcul de la distance totale d'un chemin (solution) pour le TSP
def calculate_total_distance(solution, node_coordinates):
    total_distance = 0.0
    num_nodes = len(solution)
    for i in range(num_nodes):
        node1 = node_coordinates[solution[i]]
        node2 = node_coordinates[solution[(i + 1) % num_nodes]]
        total_distance += geo_distance(node1, node2)
    return total_distance

# Initialisation de la population
def initialize_population(num_nodes, population_size):
    population = []
    for _ in range(population_size):
        solution = list(range(num_nodes))
        random.shuffle(solution)
        population.append(solution)
    return population

# Sélection des meilleures solutions
def select_best_solutions(population, node_coordinates, num_selected):
    fitness_scores = [(calculate_total_distance(solution, node_coordinates), solution) for solution in population]
    fitness_scores.sort()
    selected_solutions = [solution for _, solution in fitness_scores[:num_selected]]
    return selected_solutions

# Opérateur de croissance des plantes
def grow_plant(plant, growth_rate, node_coordinates):
    new_plant = plant[:]  #une copie de la solution actuelle pour éviter de modifier la solution d'origine.

    # le mécanisme de croissance 
    idx1, idx2 = random.sample(range(len(plant)), 2) #Deux indices aléatoires sont sélectionnés dans la liste représentant la solution
    new_plant[idx1], new_plant[idx2] = new_plant[idx2], new_plant[idx1] #echange de valeurs 
    return new_plant

def grow_plants(selected_solutions, growth_rate, node_coordinates):
    new_population = []
    for solution in selected_solutions:
        for _ in range(growth_rate):
            new_solution = grow_plant(solution, growth_rate, node_coordinates)
            new_population.append(new_solution)
    return new_population

# Algorithme PGO pour le TSP
def plant_growth_optimizer(node_coordinates, population_size, max_iterations, growth_rate):
    num_nodes = len(node_coordinates)
    population = initialize_population(num_nodes, population_size)
    best_solution = None
    best_distance = float('inf')

    for iteration in range(max_iterations):
        selected_solutions = select_best_solutions(population, node_coordinates, population_size // 2)
        new_population = grow_plants(selected_solutions, growth_rate, node_coordinates)

        for solution in new_population:
            distance = calculate_total_distance(solution, node_coordinates)
            if distance < best_distance:
                best_solution = solution
                best_distance = distance

        population = new_population

    return best_solution, best_distance



############### main 
if __name__ == "__main__":
    tsp_file = 'ulysses22.tsp' 
    population_size = 50  
    max_iterations = 1700  
    growth_rate = 14  

    node_coordinates = load_tsp_data(tsp_file)
    best_solution, best_distance = plant_growth_optimizer(node_coordinates, population_size, max_iterations, growth_rate)

    print(f"Meilleure solution trouvée : {best_solution}")
    print(f"Distance totale de la meilleure solution : {best_distance}")
