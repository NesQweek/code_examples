import numpy
import numpy as np
import matplotlib.pyplot as plt
import math, pickle, os
from scipy.spatial import cKDTree

current_dir = os.path.dirname(__file__)
test_well_data = os.path.join(current_dir, 'data', 'test_well_data.pkl')
with open(test_well_data, 'rb') as file:
    points = pickle.load(file)

search_radius = 10 # радиус поиска точек с пробами
angle_tolerance = 30 # угловой допуск

def calculate_angle(v1, v2):
    """Функция для вычисления угла между векторами"""
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    cosine_angle = dot_product / (norm_v1 * norm_v2)
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)

def calculate_distance(point1, point2):
    """Функция для вычисления расстояния между двумя точками"""
    x1, y1, z1 = point1[0], point1[1], point1[2]
    x2, y2, z2 = point2[0], point2[1], point2[2]
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    return distance

well_names = []  # список для хранения множества n1,n2,..., n э N имен скважин (n1,n2,...,n)
points_data = [] # список для хранения множества p1,p2,..., p э P данных точек опробования (x,y,z,is ore/is not ore)

for key, value in points.items():
    for well_name, xyz_coords in value.items():
        well_names.extend([key] * len(xyz_coords))
        points_data.extend([(coord[0], coord[1], coord[2], well_name) for coord in xyz_coords])

points_space = np.array(points_data)
tree = cKDTree(points_space) # сложность O(logN)

interpolated_points = set() # множество для полученных после интерполяции точек

# Интерполяция и заполнение interpolated_points
for i, point_i in enumerate(points_space):
    group = well_names[i]

    group_indices = np.where(np.array(well_names) != group)[0]
    j_candidates = tree.query_ball_point(points_space, r=search_radius)
    relevant_j_candidates = np.intersect1d(j_candidates[i], group_indices)

    for j_idx in relevant_j_candidates:
        vector_i = points_space[i]
        vector_j = points_space[j_idx]
        angle = calculate_angle(vector_i, vector_j)
        if angle < angle_tolerance:
            dist = calculate_distance(vector_i, vector_j)
            center = [(vector_i[0] + vector_j[0]) / 2, (vector_i[1] + vector_j[1]) / 2,
                      (vector_i[2] + vector_j[2]) / 2, (vector_i[3] + vector_j[3]) / 2]
            center = np.array(center)
            if center[3] >= 0.5:
                interpolated_points.add(tuple(center))

interpolated_points = np.array(list(interpolated_points))


## вывод 3D графика


x = [point[0] for point in points_space]
y = [point[1] for point in points_space]
z = [point[2] for point in points_space]

x_ = [point[0] for point in interpolated_points]
y_ = [point[1] for point in interpolated_points]
z_ = [point[2] for point in interpolated_points]

# инициализация фигуры и оси 3D графика
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# отображение точек разными цветами и маркерами
ax.scatter(x, y, z, c='g', marker='o')
ax.scatter(x_, y_, z_, c='black', marker='.')

# подпись осей
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# показать график
plt.show()

# out = current_dir + '\\kdtree_points.pkl'
# with open(out, 'wb') as file:
#     pickle.dump(combined_points,file)

