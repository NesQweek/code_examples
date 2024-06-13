import os

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
# init
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
        decomposition_dict[level] = [[block], [LC], [CR], [LC_points], [CR_points]]
    else:
        decomposition_dict[level][0].extend([block])
        decomposition_dict[level][1].extend([LC])
        decomposition_dict[level][2].extend([CR])
        decomposition_dict[level][3].extend([LC_points])
        decomposition_dict[level][4].extend([CR_points])

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


def plotting(coords, o, lp, rp, center_o, main_direction_j, first_principal_orientations):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], c='black', marker='x')

    ax.scatter(o[:, 0], o[:, 1], o[:, 2], c='b', marker='v')
    ax.scatter(lp[j][:, 0], lp[j][:, 1], lp[j][:, 2], c='y', marker='o')
    ax.scatter(rp[j][:, 0], rp[j][:, 1], rp[j][:, 2], c='g', marker='o')

    # Добавляем визуализацию основного направления
    ax.quiver(center_o[0], center_o[1], center_o[2], main_direction_j[0], main_direction_j[1],
            main_direction_j[2], color='g')
    # Добавляем визуализацию основного направления
    ax.quiver(center_o[0], center_o[1], center_o[2], first_principal_orientations[0], first_principal_orientations[1],
            first_principal_orientations[2], color='r')

    # Подписи осей
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()


origin_size = None
coef = 1


interrupted = False

while not interrupted:
    for k, subkeys in decomposition_dict.items():
        print(f'Уровень: {k}\n-----------------------------')

        if k == dl:
            origin_size = subkeys[0]
        else:
            coef *= 2
            origin2 = [o for o in origin_size for _ in range(coef)]

        if k == 1:
            for i in range(0, len(origin2), coef):
                # Остановка цикла по требованию пользователя.
                if keyboard.is_pressed('q'):
                    interrupted = True
                    break

                o = origin2[i]
                o_ = subkeys[0][i:i + coef]
                l = subkeys[1][i:i + coef]
                r = subkeys[2][i:i + coef]
                lp = subkeys[3][i:i + coef]
                rp = subkeys[4][i:i + coef]

                center_o = np.mean(o, axis=0)
                first_principal_orientations = np.zeros(3)

                for j in range(coef):

                    if len(rp[j]) == 0 and len(lp[j]) == 0:
                        continue

                    if len(lp[j]) > 0 and len(rp[j]) > 0:
                        center_l = np.mean(lp[j], axis=0)
                        centered_l = center_l - center_o
                        _, _, Vl = np.linalg.svd(centered_l.reshape(1, -1))
                        main_direction_l = Vl[0]
                        center_r = np.mean(rp[j], axis=0)
                        centered_r = center_r - center_o
                        _, _, Vr = np.linalg.svd(centered_r.reshape(1, -1))
                        main_direction_r = Vr[0]
                        combined_points = np.vstack((centered_l, centered_r))
                        _, _, Vj = np.linalg.svd(combined_points)
                        main_direction_j = Vj[0]
                        first_principal_orientations += main_direction_j

                    elif len(lp[j]) > 0 and len(rp[j]) == 0:
                        center_l = np.mean(lp[j], axis=0)
                        centered_l = center_l - center_o
                        _, _, Vl = np.linalg.svd(centered_l.reshape(1, -1))
                        main_direction_j = Vl[0]
                        first_principal_orientations += main_direction_j

                    elif len(rp[j]) > 0 and len(lp[j]) == 0:
                        center_r = np.mean(rp[j], axis=0)
                        centered_r = center_r - center_o
                        _, _, Vr = np.linalg.svd(centered_r.reshape(1, -1))
                        main_direction_j = Vr[0]
                        first_principal_orientations += main_direction_j

                    first_principal_orientations /= np.linalg.norm(first_principal_orientations)

                    plotting(coords, o, lp, rp, center_o, main_direction_j, first_principal_orientations)





                # fig = plt.figure()
                # ax = fig.add_subplot(111, projection='3d')
                # ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], c='black', marker='x')
                #
                # ax.scatter(o[:, 0], o[:, 1], o[:, 2], c='b', marker='v')
                #
                # ax.scatter(lp[j][:, 0], lp[j][:, 1], lp[j][:, 2], c='y', marker='o')
                # ax.scatter(rp[j][:, 0], rp[j][:, 1], rp[j][:, 2], c='g', marker='o')
                # ax.scatter(l[j][:, 0], l[j][:, 1], l[j][:, 2], c='y', marker='o')
                # ax.scatter(r[j][:, 0], r[j][:, 1], r[j][:, 2], c='g', marker='o')
                # ax.set_xlabel('X')
                # ax.set_ylabel('Y')
                # ax.set_zlabel('Z')
                # plt.show()









