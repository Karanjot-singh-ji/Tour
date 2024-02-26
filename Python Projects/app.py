from flask import Flask, render_template, request

app = Flask(__name__)

def nearest_neighbor(distances, place_names):
    num_nodes = len(distances)
    visited = [False] * num_nodes
    path = [0]  # Start from node 0
    visited[0] = True

    for _ in range(num_nodes - 1):
        current_node = path[-1]
        nearest_node = None
        min_distance = float('inf')
        for next_node in range(num_nodes):
            if not visited[next_node] and distances[current_node][next_node] < min_distance:
                nearest_node = next_node
                min_distance = distances[current_node][next_node]
        path.append(nearest_node)
        visited[nearest_node] = True

    # Add distance back to starting node
    total_distance = sum(distances[path[i]][path[i+1]] for i in range(num_nodes - 1))
    total_distance += distances[path[-1]][path[0]]

    return path, total_distance

def get_distances(place_names):
    num_places = len(place_names)
    distances = [[0] * num_places for _ in range(num_places)]
    for i in range(num_places):
        for j in range(i + 1, num_places):
            distance = int(request.form.get(f"distance_{i}_{j}"))
            distances[i][j] = distances[j][i] = distance
    return distances

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_places = int(request.form.get("num_places"))
        place_names = [request.form.get(f"place_{i}") for i in range(num_places)]
        distances = get_distances(place_names)
        shortest_path, shortest_dist = nearest_neighbor(distances, place_names)
        return render_template('result.html', shortest_path=shortest_path, place_names=place_names, shortest_dist=shortest_dist)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
