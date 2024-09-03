import math
import random

def to_radians(degrees):
    return degrees * math.pi / 180

# calcule la distance géographique entre deux points
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

# la distance totale 
def calculate_total_distance(solution, node_coordinates):
    total_distance = 0.0
    num_nodes = len(solution)
    for i in range(num_nodes):
        node1 = node_coordinates[solution[i]]
        node2 = node_coordinates[solution[(i + 1) % num_nodes]]
        total_distance += geo_distance(node1, node2)
    return total_distance





#initialisation
def initialize_population(num_nodes, population_size):
    population = []
    for _ in range(population_size):
        solution = list(range(num_nodes))
        random.shuffle(solution)
        population.append(solution)
    return population


#Selection des solutions bases sur leur qualite.
# Fonction de selection basee sur la competition


# la qualité distance totale de chaque solution dans la pop.

def select_best_solutions(population, node_coordinates, num_selected):
    fitness_scores = [(calculate_total_distance(solution, node_coordinates), solution) for solution in population]
    fitness_scores.sort()
    selected_solutions = [solution for _, solution in fitness_scores[:num_selected]]
    return selected_solutions

# Opérateur de propagation des plantes (création de nouvelles solutions)
#Propager les bonnes solutions en créant de nouvelles solutions par croisement
def propagate_plants(selected_solutions):
    new_population = []
    num_selected = len(selected_solutions)
    for i in range(num_selected):
        for j in range(i + 1, num_selected):
            new_solution = crossover(selected_solutions[i], selected_solutions[j])
            new_population.append(new_solution)
    return new_population

#  crossover pour creer de nouvelles solutions
def crossover(solution1, solution2):
    num_nodes = len(solution1)
    start = random.randint(0, num_nodes - 1)
    end = random.randint(start + 1, num_nodes)
    new_solution = [-1] * num_nodes
    for i in range(start, end):
        new_solution[i] = solution1[i]
    index = 0
    for i in range(num_nodes):
        if new_solution[i] == -1:
            while solution2[index] in new_solution:
                index += 1
            new_solution[i] = solution2[index]
            index += 1
    return new_solution

# PPA pour le TSP
def plant_propagation_algorithm(node_coordinates, population_size, max_iterations):
    num_nodes = len(node_coordinates)
    population = initialize_population(num_nodes, population_size)
    best_solution = None
    best_distance = float('inf')    #La distance de la meilleure solution trouvee initialisée à l'infini.





    for iteration in range(max_iterations):
        selected_solutions = select_best_solutions(population, node_coordinates, population_size // 2)
        new_population = propagate_plants(selected_solutions)

        # Sélection de la meilleure solution de la nouvelle population
        for solution in new_population:
            distance = calculate_total_distance(solution, node_coordinates)
            if distance < best_distance:
                best_solution = solution
                best_distance = distance

        population = new_population

    return best_solution, best_distance

# Exemple d'utilisation avec les paramètres
if __name__ == "__main__":
    tsp_file = 'ulysses22.tsp'  # Chemin vers le fichier TSP
    population_size = 50  # Taille de la population
    max_iterations = 2500  # Nombre maximum d'itérations

    # Chargement des coordonnées des nœuds à partir du fichier TSP
    node_coordinates = load_tsp_data(tsp_file)

    best_solution, best_distance = plant_propagation_algorithm(node_coordinates, population_size, max_iterations)

    print(f"Meilleure solution trouvée : {best_solution}")
    print(f"Distance totale de la meilleure solution : {best_distance}")
