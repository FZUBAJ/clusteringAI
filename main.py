# UI assignment 3c -> clustering, author: Filip Zubaj, date: 17.11.2023
from random import randint, choice
from typing import List, Tuple
import matplotlib.pyplot as plt

# ----- DEFINITIONS -----
point = Tuple[int, int]


# ----- QUESTIONS -----
# do points have to be unique?
# ----- TODO -----
# aglomeration -> metoid
# aglomeration -> centroid

class Cluster:
    def __init__(self, points: List[point], linkage: str):
        self.points = points
        self.linkage = linkage
        self.center = self.calculate_center(self.linkage)
        self.average_distance = self.calculate_average_distance()

    def calculate_center(self, linkage: str) -> point:
        if linkage == 'centroid':




# generate 20 points in range (-5000, 5000) with random and unique X and Y coordinates
def generate_origin_points() -> List[point]:
    origin_points = set()
    while len(origin_points) < 20:
        x = randint(-5000, 5000)
        y = randint(-5000, 5000)
        origin_points.add((x, y))

    return list(origin_points)


def generate_matrix_of_distances(points: List[point]) -> List[List[float]]:
    n = len(points)
    matrix_of_distances = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            distance_between_points = calculate_distance(points[i], points[j])
            matrix_of_distances[i][j] = distance_between_points
            matrix_of_distances[j][i] = distance_between_points
    return matrix_of_distances


def create_another_points(origin_points: List[point], number: int) -> List[point]:
    final_points = set(origin_points)

    boundary_x1 = -100
    boundary_x2 = 100
    boundary_y1 = -100
    boundary_y2 = 100

    while len(final_points) < number:
        x, y = choice(list(final_points))
        if x + boundary_x1 < -5000:
            boundary_x1 = -x - 5000
        elif x + boundary_x2 > 5000:
            boundary_x2 = abs(x - 5000)
        if y + boundary_y1 < -5000:
            boundary_y1 = -y - 5000
        elif y + boundary_y2 > 5000:
            boundary_y2 = abs(y - 5000)

        x_offset = x + randint(boundary_x1, boundary_x2)
        y_offset = y + randint(boundary_y1, boundary_y2)
        final_points.add((x_offset, y_offset))

    return list(final_points)


# I calculate centroid as integer -> average of X and Y coordinates
def calculate_centroid(points: List[point]) -> point:
    x_sum, y_sum = map(sum, zip(*points))
    return int(x_sum / len(points)), int(y_sum / len(points))


# metoid is the point, thas it has the smallest sum of distances to other points in cluster
# it is not just an imaginary point, it is one of the points in cluster
def calculate_metoid(points: List[point]) -> point:
    metoid = points[0]
    min_sum = sum(calculate_distance(metoid, one_point) for one_point in points)

    for curr_point in points:
        point_sum = sum(calculate_distance(curr_point, one_point) for one_point in points)
        if point_sum < min_sum:
            min_sum = point_sum
            metoid = curr_point

    return metoid


def calculate_distance(point1: point, point2: point) -> float:
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5


def calculate_cluster_distance(cluster1: List[point], cluster2: List[point], linkage: str) -> float:
    if linkage == 'centroid':
        center1 = calculate_centroid(cluster1)
        center2 = calculate_centroid(cluster2)
    elif linkage == 'metoid':
        center1 = calculate_metoid(cluster1)
        center2 = calculate_metoid(cluster2)
    else:
        print('Wrong linkage')
        exit(1)
    return calculate_distance(center1, center2)


def agglomerative_clustering(points: List[point], number_of_clusters: int, linkage: str) -> List[List[point]]:
    # first we create the distance matrix
    # matrix_of_distances = generate_matrix_of_distances(points)
    clusters = [[curr_point] for curr_point in points]

    while len(clusters) > number_of_clusters:
        min_distance = float('inf')
        connect_clusters = (-1, -1)

        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                distance = calculate_cluster_distance(clusters[i], clusters[j], linkage)
                if distance < min_distance:
                    min_distance = distance
                    connect_clusters = (i, j)

        if connect_clusters != (-1, -1):
            clusters[connect_clusters[0]].extend(clusters[connect_clusters[1]])
            del clusters[connect_clusters[1]]

    return clusters

# nájst najmensiu hodnotu a indexy
# spojiť tieto clusters
# vymazať druhý cluster
# update distance matrix


def validate_clusters(clusters: List[List[point]], linkage: str) -> bool:
    unsuccessful = 0
    for i, cluster in enumerate(clusters):
        if linkage == 'centroid':
            center = calculate_centroid(cluster)
        else:
            center = calculate_metoid(cluster)

        average_distance = sum(calculate_distance(center, cluster_point) for cluster_point in cluster) / len(cluster)
        if average_distance > 500:
            unsuccessful += 1
            print(f'❌Error❌: unsuccessful cluster with number {str(i + 1)}')
        else:
            print(f'✅Success✅: successful cluster with number {str(i + 1)}')

        print(f'Center: {str(center)}')
        print(f'Average distance from center: {str(average_distance)}')

    print(f'Success rate: {100 - unsuccessful / len(clusters) * 100}%')


def visualise_clusters(clusters: List[List[point]], linkage: str, filename) -> None:
    colors = ['r', 'g', 'y', 'c', 'm', 'k']

    for i, cluster in enumerate(clusters):
        x = [one_point[0] for one_point in cluster]
        y = [one_point[1] for one_point in cluster]
        plt.scatter(x, y, c=colors[i % len(colors)])
        if linkage == 'centroid':
            center = calculate_centroid(cluster)
        else:
            center = calculate_metoid(cluster)
        plt.scatter(center[0], center[1], c='black')

    plt.title(f'Clustering with {linkage} linkage')
    plt.xlabel('X - axis')
    plt.ylabel('Y - axis')
    plt.savefig(filename)
    plt.show()


def main():
    origin_points = generate_origin_points()
    another_points = create_another_points(origin_points, 200)
    linkage = 'centroid'
    clusters = agglomerative_clustering(another_points, 20, linkage)
    validate_clusters(clusters, linkage)
    visualise_clusters(clusters, linkage, 'clustering1.png')


if __name__ == '__main__':
    main()
