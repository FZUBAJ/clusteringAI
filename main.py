# UI assignment 3c -> clustering, author: Filip Zubaj, date: 17.11.2023
from random import randint, choice
from typing import List, Tuple
# import matplotlib.pyplot as plt

point = Tuple[int, int]

# ----- QUESTIONS -----
# do points have to be unique?
# ----- TODO -----
# aglomeration -> metoid
# aglomeration -> centroid


# generate 20 points in range (-5000, 5000) with random and unique X and Y coordinates
def generate_origin_points() -> List[point]:
    origin_points = []
    while len(origin_points) < 20:
        x = randint(-5000, 5000)
        y = randint(-5000, 5000)
        if (x, y) not in origin_points:
            origin_points.append((x, y))
    return origin_points


def create_another_points(origin_points: List[point], number: int) -> List[point]:
    another_points = []
    boundary_x1 = -100
    boundary_x2 = 100
    boundary_y1 = -100
    boundary_y2 = 100
    for i in range(number):
        x, y = choice(origin_points)
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
        another_points.append((x_offset, y_offset))

    return origin_points + another_points


def calculate_centroid(points: List[point]) -> point:
    x_sum = sum(x[0] for x in points)
    y_sum = sum(y[1] for y in points)
    x, y = int(x_sum / len(points)), int(y_sum / len(points))
    return x, y


def calculate_distance(point1: point, point2: point) -> float:
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5


def agglomerative_clustering(points: List[point], number_of_clusters: int, linkage: str) -> List[List[point]]:
    clusters = [[point] for point in points]
    while len(clusters) > number_of_clusters:
        pass


def main():
    pass
    # origin_points = generate_origin_points()
    # another_points = create_another_points(origin_points, 50)


if __name__ == '__main__':
    main()
