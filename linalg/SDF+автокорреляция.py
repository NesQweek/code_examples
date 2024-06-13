import numpy as np
from matplotlib import pyplot as plt

wells = {
    'M-1': [[2.0, 2.0, 9.0, 20, 0.0], [2.0, 2.0, 8.4, 9.0, 1.0], [2.0, 2.0, 6.1, 8.4, 1.0], [2.0, 2.0, 4.0, 6.1, 1.0],
            [2.0, 2.0, -6, 4.0, 0.0]],
    'M-11': [[2.0, 6.0, 9.0, 20, 0.0], [2.0, 6.0, 8.4, 9.0, 0.0], [2.0, 6.0, 6.1, 8.4, 0.0], [2.0, 6.0, 4.0, 6.1, 1.0],
            [2.0, 6.0, -6, 4.0, 1.0]],
    'M-111': [[2.0, 9.0, 19, 27, 0], [2.0, 9.0, 18.4, 19.0, 1.0], [2.0, 9.0, 16.1, 18.4, 1.0], [2.0, 9.0, 14.0, 16.1, 1.0],
              [2.0, 9.0, 7, 14.0, 0.0]],
    'M-2': [[9.0, 2.0, 14, 28.0, 0.0], [9.0, 2.0, 13.3, 14.0, 1.0], [9.0, 2.0, 10.0, 13.3, 1.0], [9.0, 2.0, 7.5, 10.0, 1.0],
            [9.0, 2.0, 5.0, 7.5, 1.0], [9.0, 2.0, -3, 5.0, 0.0]],
    'M-222': [[9.0, 7.0, 24, 31, 0.0], [9.0, 7.0, 23.3, 24.0, 1.0], [9.0, 7.0, 20.0, 23.3, 1.0], [9.0, 7.0, 17.5, 20.0, 1.0],
              [9.0, 7.0, 15.0, 17.5, 1.0], [9.0, 7.0, 6.0, 15.0, 0.0]],
    'M-3': [[17.0, 2.0, 20, 27, 0], [17.0, 2.0, 18.6, 20.0, 1.0], [17.0, 2.0, 15.6, 18.6, 1.0], [17.0, 2.0, 13.6, 15.6, 1.0],
            [17.0, 2.0, 5, 13.6, 0.0]],
    'M-31': [[14.0, 4.0, 20, 27, 0], [14.0, 4.0, 18.6, 20.0, 1.0], [14.0, 4.0, 15.6, 18.6, 1.0],
            [14.0, 4.0, 13.6, 15.6, 1.0], [17.0, 2.0, 5, 13.6, 0.0]],
    'M-4': [[28.0, 2.0, 20.0, 23.0, 1.0], [28.0, 2.0, 16.8, 20.0, 1.0], [28.0, 2.0, 14.0, 16.8, 1.0],[28.0, 2.0, 6, 14, 0.0],
            [28.0, 2.0, 23.0, 30, 0.0]],
    'M-55': [[37.0, 2.0, 29.0, 29.5, 1.0], [37.0, 2.0, 29.5, 31.1, 0.0], [37.0, 2.0, 26.0, 29.0, 0.0], [37.0, 2.0, 31.1, 38, 0.0],
             [37.0, 2.0, 18, 26.0, 0.0]],
    'M-555': [[37.0, 9.0, 34.0, 34.5, 1.0], [37.0, 9.0, 34.0, 41, 0.0], [37.0, 9.0, 31.0, 34.0, 0.0],
              [37.0, 9.0, 25.0, 31.0, 0.0]],
    'M-556': [[37.0, 6, 34.0, 24.5, 1.0], [37.0, 6, 29.0, 36, 0.0], [37.0, 6, 26.0, 29, 0.0],
              [37.0, 6, 20.0, 26.0, 0.0]]
}
# Разбиение интервалов на точки
def interpolate_points(top, bottom, num_points):
    top, bottom = np.array(top), np.array(bottom)
    return [top + (bottom - top) * (i / num_points) for i in range(1, num_points + 1)]
sampling_interval = 1
sampled_points = []
well_names = []
for well_name, intervals in wells.items():
    max_interval = max(intervals, key=lambda x: x[2])
    sampled_points.append([max_interval[0], max_interval[1], max_interval[3], max_interval[4]])
    well_names.append(well_name)

    for x, y, z1, z2, interval in intervals:
        num_points = int((z2 - z1) / sampling_interval) + 1
        new_points = interpolate_points([x, y, z1, interval], [x, y, z2, interval], num_points)
        sampled_points.extend(new_points)
        well_names.extend([well_name] * num_points)
sampled_points = np.array(sampled_points)

# Удаление дубликатов строк
points_ = np.unique(np.array(sampled_points), axis=0)


#SDF ---------
def calculate_sdf(sampled_points):

    category_1 = []
    f = np.zeros(len(sampled_points))  # Initialize an empty vector for SDF values
    for i, p in enumerate(sampled_points):
        distances = np.linalg.norm(sampled_points[:, :3] - p[:3], axis=1)  # Calculate distances
        sorted_distances = np.sort(distances)
        j = 0
        while sampled_points[i][-1] == sampled_points[np.where(distances == sorted_distances[j])[0][0]][-1]:
            j += 1
        f[i] = sorted_distances[j]
        if sampled_points[i][3] == 1:
            category_1.append([sampled_points[i][0],sampled_points[i][1],sampled_points[i][2],f[i]])
    category_1 = np.array(category_1)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = sampled_points[:, 0]
    y = sampled_points[:, 1]
    z = sampled_points[:, 2]
    values = -f
    ax.scatter(x, y, z, c=values, cmap='hot')
    plt.show()

    return category_1
points = calculate_sdf(points_)

import statsmodels.api as sm
# Строим коррелограммы для каждой из осей
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 6))
for i, col in enumerate(['x', 'y', 'z']):
    sm.graphics.tsa.plot_acf(points[:, i], lags=50, ax=axes[i], title=f'Autocorrelation for {col}')

plt.tight_layout()
plt.show()
