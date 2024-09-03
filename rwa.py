import math
import random

#1
def to_radians(degrees):
    return degrees * math.pi / 180

# Fonction pour calculer la distance géographique entre deux points
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

###############################################
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

#  distance totale d un chemin 
def calculate_total_distance(solution, node_coordinates):
    total_distance = 0.0
    num_nodes = len(solution)
    for i in range(num_nodes):
        node1 = node_coordinates[solution[i]]
        node2 = node_coordinates[solution[(i + 1) % num_nodes]]
        total_distance += geo_distance(node1, node2)
    return total_distance

# initialisation de la population
def initialize_population(num_nodes, population_size):
    population = []
    for _ in range(population_size):
        solution = list(range(num_nodes))
        random.shuffle(solution)
        population.append(solution)
    return population

# selection des meilleures solutions
def select_best_solutions(population, node_coordinates, num_selected):
    fitness_scores = [(calculate_total_distance(solution, node_coordinates), solution) for solution in population]
    fitness_scores.sort()
    selected_solutions = [solution for _, solution in fitness_scores[:num_selected]]
    return selected_solutions

# Processus de pluie generer de nouvelles solutions
def move_water(selected_solutions):
    new_population = []
    for solution in selected_solutions:
        new_solution = perturb_solution(solution)
        new_population.append(new_solution)
    return new_population

# Opérateur de perturbation pour générer de nouvelles solutions
def perturb_solution(solution):
    new_solution = solution[:]
    idx1, idx2 = random.sample(range(len(solution)), 2)
    new_solution[idx1], new_solution[idx2] = new_solution[idx2], new_solution[idx1]
    return new_solution

# Algorithme RWA pour le TSP
def rain_water_algorithm(node_coordinates, population_size, max_iterations, evaporation_rate):
    num_nodes = len(node_coordinates)
    population = initialize_population(num_nodes, population_size)
    best_solution = None
    best_distance = float('inf')

    for iteration in range(max_iterations):
        selected_solutions = select_best_solutions(population, node_coordinates, population_size // 2)
        new_population = move_water(selected_solutions)

        # Evaporation: ajout de solutions aléatoires
        for _ in range(int(evaporation_rate * population_size)):
            new_population.append(random.choice(population))

        # Sélection de la meilleure solution de la nouvelle population
        for solution in new_population:
            distance = calculate_total_distance(solution, node_coordinates)
            if distance < best_distance:
                best_solution = solution
                best_distance = distance

        population = new_population

    return best_solution, best_distance

# Main
if __name__ == "__main__":
    tsp_file = 'ulysses22.tsp' 
    population_size = 50  
    max_iterations = 2000  
    evaporation_rate = 0.9  # Taux d'évaporation (50%)- 80-90 ...

    node_coordinates = load_tsp_data(tsp_file)

    best_solution, best_distance = rain_water_algorithm(node_coordinates, population_size, max_iterations, evaporation_rate)

    print(f"Meilleure solution trouvée : {best_solution}")
    print(f"Distance totale de la meilleure solution : {best_distance}")
