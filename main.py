from perlin_noise import PerlinNoise
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random

# ---------------- WORLD GENERATION ----------------

def WorldGen(size_x, size_y, seed_id):

    color_map = np.zeros((size_x, size_y, 3))
    height_map = np.zeros((size_x, size_y))

    noise1 = PerlinNoise(octaves=3, seed=seed_id)
    noise2 = PerlinNoise(octaves=6, seed=seed_id)

    for i in range(size_x):
        for j in range(size_y):

            noise_val = noise1([i / 50, j / 50])
            noise_val += noise2([i / 50, j / 50]) + 0.2

            height_map[i, j] = noise_val

            if noise_val < 0:
                color_map[i, j] = (0, 0, 1)  # water

            elif noise_val < 0.15:
                color_map[i, j] = (1, 1, 0)  # sand

            elif noise_val < 0.5:
                color_map[i, j] = (0, 1, 0)  # grass

            elif noise_val < 0.7:
                color_map[i, j] = (0.5, 0.3, 0.1)  # mountain

            else:
                color_map[i, j] = (1, 1, 1)  # snow

    return color_map, height_map

# ---------------- FOOD ----------------

class Food:

    def __init__(self, height_map):

        while True:

            x = random.randint(0, len(height_map) - 1)
            y = random.randint(0, len(height_map[0]) - 1)

            if height_map[x, y] > 0:
                self.pos_x = x
                self.pos_y = y
                break

# ---------------- ANT ----------------

class Ant:

    def __init__(self, height_matrix):

        self.height_matrix = height_matrix

        while True:

            x = random.randint(0, len(height_matrix) - 1)
            y = random.randint(0, len(height_matrix[0]) - 1)

            if height_matrix[x, y] > 0:
                self.pos_x = x
                self.pos_y = y
                break

    def move(self):

        # možné smery
        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        dx, dy = random.choice(directions)

        new_x = self.pos_x + dx
        new_y = self.pos_y + dy

        # kontrola hraníc mapy
        if (
            0 <= new_x < len(self.height_matrix)
            and
            0 <= new_y < len(self.height_matrix[0])
        ):

            # nesmie ísť do vody
            if self.height_matrix[new_x, new_y] > 0:
                self.pos_x = new_x
                self.pos_y = new_y

# ---------------- MAIN ----------------

color_matrix, height_matrix = WorldGen(100, 100, 50)

foods = []

for _ in range(10):
    foods.append(Food(height_matrix))

ant = Ant(height_matrix)

# ---------------- PLOT ----------------

fig, ax = plt.subplots()

ax.imshow(color_matrix)

# vykreslenie jedla
for food in foods:
    ax.scatter(food.pos_y, food.pos_x, c='red', s=10)

# mravec
ant_plot = ax.scatter(
    ant.pos_y,
    ant.pos_x,
    c='orange',
    s=30,
    marker='s'
)

ax.axis('off')

# ---------------- ANIMATION ----------------

def update(frame):

    ant.move()

    # update pozície mravca
    ant_plot.set_offsets([ant.pos_y, ant.pos_x])

    return ant_plot,

ani = animation.FuncAnimation(
    fig,
    update,
    interval=20,   # 200 ms = 0.2 s
    blit=False
)

plt.show()
