# Разбиение пространства на домены
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
import keyboard # Для остановки цикла печати клавишей "q"

levels = 3

# Заданные точки
points_ = np.array([
    (2, 2, 8.4, 1), (2, 2, 6.1, 1), (2, 2, 4, 1), (2, 2, 2.5, 0), (9, 2, 13.3, 1), (9, 2, 10, 1), (9, 2, 7.5, 1),
    (9, 2, 5, 1), (9, 2, 3, 0), (17, 2, 18.6, 1), (17, 2, 15.6, 1), (17, 2, 13.6, 1), (17, 2, 12.8, 0), (28, 2, 20, 1),
    (28, 2, 16.8, 1), (28, 2, 14, 1), (28, 2, 23, 0), (37, 2, 24, 1), (37, 2, 24.5, 0), (37, 2, 21, 0), (37, 2, 18, 0),
    (2, 5, 13.4, 1), (2, 5, 11.1, 1), (2, 5, 9, 1), (2, 5, 7.5, 0), (9, 5, 18.3, 1), (9, 5, 15, 1), (9, 5, 13.5, 1),
    (9, 5, 10, 1), (9, 5, 8, 0), (17, 5, 23.6, 1), (17, 5, 20.6, 1), (17, 5, 18.6, 1), (17, 5, 17.8, 0),
    (28, 5, 25, 1), (28, 5, 21.8, 1), (28, 5, 19, 1), (28, 5, 28, 0), (37, 5, 29, 1), (37, 5, 29.5, 0), (37, 5, 26, 0),
    (37, 5, 23, 0), (2, 9, 18.4, 1), (2, 9, 16.1, 1), (2, 9, 14, 1), (2, 9, 12.5, 0), (9, 7, 23.3, 1), (9, 7, 20, 1),
    (9, 7, 18.5, 1), (9, 7, 15, 1), (9, 7, 13, 0), (37, 9, 34, 1), (37, 9, 31, 0), (37, 9, 28, 0)
])

points = points_[:,[0,1,2]]
xx = points[:,0]
yy = points[:,1]
zz = points[:,2]


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


def is_point_inside(point, parallelepiped):
    x, y, z = point
    x_min, y_min, z_min = min(parallelepiped)
    x_max, y_max, z_max = max(parallelepiped)
    return x_min <= x <= x_max and y_min <= y <= y_max and z_min <= z <= z_max

def plot_domains(w_, h_, d_):
    # Размеры пространства X
    min_xyz = np.min(points_[:, :3], axis=0) - 20
    max_xyz = np.max(points_[:, :3], axis=0) + 20
    X_width, X_height, X_depth = max_xyz - min_xyz

    # Сколько блоков поместится в пространстве X по каждому измерению
    blocks_xyz = ((X_width, X_height, X_depth) // np.array([w_, h_, d_])).astype(int)


    interrupted = False

    while not interrupted:
        
        for i, j, k in np.ndindex(*blocks_xyz):

            # Остановка цикла по требованию пользователя.
            if keyboard.is_pressed('q'):
                interrupted = True
                break


            x = min_xyz[0] + i * w_
            y = min_xyz[1] + j * h_
            z = min_xyz[2] + k * d_
            parallelepiped = compute_block_coordinates(x, y, z, w_, h_, d_)

            center_x = x + w_ / 2
            center_y = y + h_ / 2
            center_z = z + d_ / 2
            center = (center_x, center_y, center_z)

            section_x = np.array([[center_x, y, z], [center_x, y, z + d_], [center_x, y + h_, z + d_], [center_x, y + h_, z]])
            section_y = np.array([[x, center_y, z], [x, center_y, z + d_], [x + w_, center_y, z + d_], [x + w_, center_y, z]])
            section_z = np.array([[x, y + h_, center_z], [x + w_, y + h_, center_z], [x + w_, y, center_z], [x, y, center_z]])

            # Разделение блока пополам на два подблока A и B
            longest_side = np.argmax([w_, h_, d_])
            if longest_side == 0:
                section = section_x
            elif longest_side == 1:
                section = section_y
            else:
                section = section_z

            A_coords = parallelepiped[parallelepiped[:, longest_side] < center[longest_side]]
            B_coords = parallelepiped[parallelepiped[:, longest_side] > center[longest_side]]

            A = np.vstack([A_coords, section])
            B = np.vstack([B_coords, section])

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            for data in [A, B]:
                hull = ConvexHull(data)
                for simplex in hull.simplices:

                    verts = [data[simplex[0]], data[simplex[1]], data[simplex[2]]]
                    ax.add_collection3d(Poly3DCollection([verts], facecolors='green' if data is A else 'yellow', alpha=0.1))

            ax.scatter(xx, yy, zz, c='black', marker='.')
            ax.bar3d(min_xyz[0], min_xyz[1], min_xyz[2], X_width, X_height, X_depth, color='b', alpha=0.05)
            ax.scatter(center_x, center_y, center_z, c='black', marker='x')
            ax.scatter(A[:, 0], A[:, 1], A[:, 2], c='green', marker='v')
            ax.scatter(B[:, 0], B[:, 1], B[:, 2], c='yellow', marker='v')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            plt.show()

plot_domains(30, 15, 30)