# UI assignment 3c -> clustering, author: Filip Zubaj, date: 17.11.2023
from random import randint, choice, sample
import time
import matplotlib.pyplot as plt


# ----- TODO -----
# aglomeration -> metoid
# aglomeration -> centroid


class Cluster:
    def __init__(self, points, linkage):
        self.points = points
        self.linkage = linkage
        self.center = self.calculate_center(self.linkage)
        self.average_distance = self.calculate_average_distance()
        self.avg_distance_under_500 = True

    def calculate_center(self, linkage):
        if linkage == 'centroid':
            x_sum, y_sum = map(sum, zip(*self.points))
            return int(x_sum / len(self.points)), int(y_sum / len(self.points))
        elif linkage == 'metoid':
            metoid = self.points[0]
            min_sum = sum(calculate_distance(metoid, one_point) for one_point in self.points)

            for curr_point in self.points:
                point_sum = sum(calculate_distance(curr_point, one_point) for one_point in self.points)
                if point_sum < min_sum:
                    min_sum = point_sum
                    metoid = curr_point

            return metoid
        else:
            print('Wrong linkage')
            exit(1)

    def calculate_average_distance(self):
        center = self.calculate_center(self.linkage)
        return sum(calculate_distance(center, cluster_point) for cluster_point in self.points) / len(self.points)

    def update_center_and_distance(self):
        self.center = self.calculate_center(self.linkage)
        self.average_distance = self.calculate_average_distance()


# generate 20 points in range (-5000, 5000) with random and unique X and Y coordinates
def generate_origin_points():
    x_coordinates = sample(range(-5000, 5001), 20)
    y_coordinates = sample(range(-5000, 5001), 20)
    origin_points = list(zip(x_coordinates, y_coordinates))
    return origin_points


def generate_matrix_of_distances(points):
    n = len(points)
    matrix_of_distances = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            distance_between_points = calculate_distance(points[i], points[j])
            matrix_of_distances[i][j] = distance_between_points
            matrix_of_distances[j][i] = distance_between_points
    return matrix_of_distances


def create_another_points(origin_points, number):
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


def calculate_distance(point1, point2):
    return abs(point2[0] - point1[0]) + abs(point2[1] - point1[1])
    #return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5


def calculate_cluster_distance(cluster1, cluster2):
    return calculate_distance(cluster1.center, cluster2.center)


def agglomerative_clustering(points, number_of_clusters, linkage, num_points):
    # first we create the distance matrix
    # matrix_of_distances = generate_matrix_of_distances(points)
    clusters = [Cluster([curr_point], linkage) for curr_point in points]

    while len(clusters) > number_of_clusters:

        if len(clusters) == int(num_points * 0.75):
            print("25% . . .")
        elif len(clusters) == int(num_points / 2):
            print("50% . . .")
        elif len(clusters) == int(num_points / 4):
            print("75% . . .")

        min_distance = float('inf')
        connect_clusters = (-1, -1)

        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                distance = calculate_cluster_distance(clusters[i], clusters[j])
                if distance < min_distance:
                    min_distance = distance
                    connect_clusters = (i, j)

        if connect_clusters != (-1, -1):
            clusters[connect_clusters[0]].points.extend(clusters[connect_clusters[1]].points)
            clusters[connect_clusters[0]].update_center_and_distance()
            del clusters[connect_clusters[1]]

    return clusters


def validate_clusters(clusters):
    unsuccessful = 0
    for i, cluster in enumerate(clusters):
        center, avg_distance = cluster.center, cluster.average_distance
        if avg_distance > 500:
            unsuccessful += 1
            print('❌Error❌: unsuccessful cluster with number ' + str(i + 1))
        else:
            print('✅Success✅: successful cluster with number ' + str(i + 1))

        print('Center: ' + str(center))
        print('Average distance from center: ' + str(avg_distance))

    print('Success rate: {}%'.format(100 - unsuccessful / len(clusters) * 100))


def visualise_clusters(clusters, filename):
    colors = ['r', 'g', 'y', 'c', 'm', 'k']

    for i, cluster in enumerate(clusters):
        x = [one_point[0] for one_point in cluster.points]
        y = [one_point[1] for one_point in cluster.points]
        plt.scatter(x, y, c=colors[i % len(colors)])
        plt.scatter(cluster.center[0], cluster.center[1], c='b')

    plt.title('Clustering with ' + clusters[0].linkage + ' linkage')
    plt.xlabel('X - axis')
    plt.ylabel('Y - axis')
    plt.savefig(filename)
    plt.show()


def main():
    num_points = 5000
    origin_points = generate_origin_points()
    another_points = create_another_points(origin_points, num_points)
    linkage = 'centroid'
    start_time = time.time()  # Record the start time
    clusters = agglomerative_clustering(another_points, 20, linkage, num_points)
    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate the elapsed time
    print(f"Elapsed Time: {elapsed_time} seconds")
    validate_clusters(clusters)
    visualise_clusters(clusters, 'clustering1.png')


if __name__ == '__main__':
    main()
