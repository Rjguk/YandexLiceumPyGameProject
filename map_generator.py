import noise
import numpy as np

def generation(shape=20):
    shape = (shape, shape)
    scale = .5
    octaves = 6
    persistence = 0.5
    lacunarity = 2.0
    seed = np.random.randint(0, 1000)

    world = np.zeros(shape)

    x_idx = np.linspace(0, 1, shape[0])
    y_idx = np.linspace(0, 1, shape[1])
    world_x, world_y = np.meshgrid(x_idx, y_idx)

    world = np.vectorize(noise.pnoise2)(world_x / scale,
                                        world_y / scale,
                                        octaves=octaves,
                                        persistence=persistence,
                                        lacunarity=lacunarity, repeatx=40, repeaty=40, base=seed)

    return np.floor((world + .5) * 4).astype(np.uint8)
