import os

import dill
import numpy as np
from matplotlib import pyplot as plt
import keyboard # Для остановки цикла печати клавишей "q"

direct_path = os.getcwd()
data_path = direct_path + '\data'
grid_data_path = data_path + '\grid_data.dill'
grid_data = dill.load(open(grid_data_path, "rb"))

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

block = np.array([
     [12., -3., 14.7],
     [42., -3., 14.7],
     [42., 12., 14.7],
     [12., 12., 14.7],
     [12., -3., 29.7],
     [42., -3., 29.7],
     [42., 12., 29.7],
     [12., 12., 29.7]
])


subblock_size = [6,5,5]

min_xyz = np.min(block, axis=0)
max_xyz = np.max(block, axis=0)
X_width, X_height, X_depth = max_xyz - min_xyz
blocks_xyz = ((X_width, X_height, X_depth) // np.array([subblock_size[0],subblock_size[1],subblock_size[2]])).astype(int)

interrupted = False

while not interrupted:

    for idx in np.ndindex(*blocks_xyz):
        # Остановка цикла по требованию пользователя.
        if keyboard.is_pressed('q'):
            interrupted = True
            break

        i, j, k = idx
        x = min_xyz[0] + i * subblock_size[0]
        y = min_xyz[1] + j * subblock_size[1]
        z = min_xyz[2] + k * subblock_size[2]

        block = compute_block_coordinates(x, y, z, subblock_size[0], subblock_size[1], subblock_size[2])

        points_inside = grid_data[((grid_data[:, 0] >= block[0][0]) & (grid_data[:, 0] <= block[1][0]) &
                                (grid_data[:, 1] >= block[0][1]) & (grid_data[:, 1] <= block[2][1]) &
                                (grid_data[:, 2] >= block[0][2]) & (grid_data[:, 2] <= block[4][2]))]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(block[:, 0], block[:, 1], block[:, 2], c='b', marker='v')
        ax.scatter(points_inside[:, 0], points_inside[:, 1], points_inside[:, 2], c='green', marker='x')
        ax.scatter(grid_data[:, 0], grid_data[:, 1], grid_data[:, 2], c='red', marker='o', alpha=0.1)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()



