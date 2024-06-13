import os
from pprint import pprint

import dill
import numpy as np
from matplotlib import pyplot as plt
import keyboard # Для остановки цикла печати клавишей "q"

direct_path = os.getcwd()
data_path = os.path.join(direct_path, 'data')
grid_data_path = os.path.join(data_path, 'grid_data.dill')
grid_data = dill.load(open(grid_data_path, "rb"))
indexed_blocks_dict = {}
decomposition_dict = {}

# -----------------------------------------------
# инициализация координат глобального домена (блока) и размера подблоков
dl = 3
subblock_size = [6,5,5]
coords = np.array([
     [12., -3., 14.7],
     [42., -3., 14.7],
     [42., 12., 14.7],
     [12., 12., 14.7],
     [12., -3., 29.7],
     [42., -3., 29.7],
     [42., 12., 29.7],
     [12., 12., 29.7]
])
# -----------------------------------------------


def find_points_between_planes(points_, L, R):
    """Функция для нахождения точек между плоскостями"""
    points = points_[:, :3]

    planes = np.array([L, R])

    # Вычисляем массивы нормалей и коэффициентов сдвига одной операцией
    normals = np.cross(planes[:, 1] - planes[:, 0], planes[:, 2] - planes[:, 0])
    ds = -np.sum(normals * planes[:, 0], axis=1)

    # Проверяем принадлежность точек к области между L и R
    LR_mask = np.logical_and(np.dot(normals[0], points.T) + ds[0] >= 0, np.dot(normals[1], points.T) + ds[1] <= 0)
    filtered_points = points_[LR_mask]

    return filtered_points


def compute_block_coordinates(x, y, z, w, h, d):
    """Функция для вычисления координат блока"""

    # Вершины блока
    vertices = [
        (x, y, z),
        (x + w, y, z),
        (x + w, y + h, z),
        (x, y + h, z),
        (x, y, z + d),
        (x + w, y, z + d),
        (x + w, y + h, z + d),
        (x, y + h, z + d),
    ]

    # Преобразуем список вершин в массив numpy
    return np.array(vertices)


def binary_decomposition(block, points_in_block, level):
    """Функция для бинарного разделения блока"""

    if level == 0:
        return

    dimension_lengths = block.max(axis=0) - block.min(axis=0)
    longest_dimension = np.argmax(dimension_lengths)

    indexed_values = block[:, longest_dimension]
    L = block[indexed_values == np.min(indexed_values)]
    R = block[indexed_values == np.max(indexed_values)]
    C = np.copy(L)
    C[:, longest_dimension] = (L[:, longest_dimension] + R[:, longest_dimension]) / 2

    LC = np.concatenate((L, C))
    CR = np.concatenate((C, R))

    LC_points = find_points_between_planes(points_in_block, L, C)
    CR_points = find_points_between_planes(points_in_block, C, R)

    if level not in decomposition_dict:
        decomposition_dict[level] = [[block], [LC], [CR]]
    else:
        decomposition_dict[level][0].extend([block])
        decomposition_dict[level][1].extend([LC])
        decomposition_dict[level][2].extend([CR])

    binary_decomposition(LC, LC_points, level - 1)
    binary_decomposition(CR, CR_points, level - 1)


# -----------------------------------------------

# Определение координат блоков по осям X, Y и Z с учетом приоритета наибольшего измерения и индексирование каждого блока
min_xyz = np.min(coords, axis=0)
max_xyz = np.max(coords, axis=0)
X_width, X_height, X_depth = max_xyz - min_xyz
blocks_xyz = ((X_width, X_height, X_depth) // np.array([subblock_size[0],subblock_size[1],subblock_size[2]])).astype(int)
longest_dimension = np.argmax([subblock_size[0], subblock_size[1], subblock_size[2]])

for idx in np.ndindex(*blocks_xyz):
    i, j, k = idx
    x = min_xyz[0] + i * subblock_size[0]
    y = min_xyz[1] + j * subblock_size[1]
    z = min_xyz[2] + k * subblock_size[2]

    block = compute_block_coordinates(x, y, z, subblock_size[0], subblock_size[1], subblock_size[2])

    points_inside = grid_data[((grid_data[:, 0] >= block[0][0]) & (grid_data[:, 0] <= block[1][0]) &
                                 (grid_data[:, 1] >= block[0][1]) & (grid_data[:, 1] <= block[2][1]) &
                                 (grid_data[:, 2] >= block[0][2]) & (grid_data[:, 2] <= block[4][2]))]

    indexed_blocks_dict[f'{i}{j}{k}'] = {
        'block_coords': block,
        'points_in_block': points_inside,
        'longest_dimension': longest_dimension
    }

for key, subkeys in indexed_blocks_dict.items():
    if len(subkeys['points_in_block']) > 1:
        binary_decomposition(subkeys['block_coords'], subkeys['points_in_block'], dl)


# ------------------------------------------------

origin1 = None
origin2 = None
coef = 1

interrupted = False

while not interrupted:

    for key, subkeys in decomposition_dict.items():

        print('Уровень:', key, '\n-----------------------------')

        if key == dl:
            origin1 = subkeys[0]
        else:
            coef *= 2
            origin2 = [o for o in origin1 for _ in range(coef)]

            block = subkeys[0]
            left = subkeys[1]
            right = subkeys[2]

            for i, _ in enumerate(block):
                
                # Остановка цикла по требованию пользователя.
                if keyboard.is_pressed('q'):
                    interrupted = True
                    break

                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.scatter(origin2[i][:, 0], origin2[i][:, 1], origin2[i][:, 2], c='b', marker='v')
                ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], c='black', marker='x')
                ax.scatter(left[i][:, 0], left[i][:, 1], left[i][:, 2], c='y', marker='o')
                ax.scatter(right[i][:, 0], right[i][:, 1], right[i][:, 2], c='g', marker='o')
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')
                plt.show()
