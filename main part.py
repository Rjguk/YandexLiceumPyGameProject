import os
import sys
import  random
import pygame
import noise
import numpy as np


real_coord = [0, 0]
max_pos = [40, 40]
text_map = []

class Cell(pygame.sprite.Sprite):
    image = {"пустая": pygame.image.load("pic\\ячейка_пустая.png"),
             "луг": pygame.image.load("pic\\ячейка_луг.png"),
             "лес": pygame.image.load("pic\\ячейка_лес.png"),
             "вода": pygame.image.load("pic\\ячейка_вода.png"),
             "болото": pygame.image.load("pic\\ячейка_болото.png")}

    def __init__(self, *group, state="пустая", pos_x=0, pos_y=0):
        super().__init__(*group)
        self.state = state
        self.image = Cell.image[self.state]
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self, type_ev=""):
        if type_ev == "up":
            self.rect.y += 100
        elif type_ev == "down":
            self.rect.y -= 100
        elif type_ev == "right":
            self.rect.x -= 100
        elif type_ev == "left":
            self.rect.x += 100
        elif type_ev == "click":
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                print(self.state)



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





if __name__ == '__main__':
    pygame.init()
    size = width, height = 1200, 900
    screen = pygame.display.set_mode(size)
    all_cell = pygame.sprite.Group()
    stop = 1
    while stop != 0:
        stop = 1
        np_map = generation(shape=max_pos[0])
        for j in range(max_pos[0]):
            test = []
            for i in range(max_pos[1]):
                test.append(np_map[i][j])
            if len(set(test)) == 1:
                stop = 2
                break
        if stop != 2:
            stop = 0



    i = 0
    j = 0
    for y in range(height - (max_pos[1]) * 100, height, 100):
        text_map.append([])
        j = 0
        for x in range(0, (max_pos[0]) * 100, 100):
            num = np_map[i][j]
            if num == 0:
                text_map[i].append("~")
                Cell(all_cell, pos_x=x, pos_y=y, state="вода")
            if num == 1:
                text_map[i].append("L")
                Cell(all_cell, pos_x=x, pos_y=y, state="луг")
            if num == 2:
                text_map[i].append("F")
                Cell(all_cell, pos_x=x, pos_y=y, state="лес")
            if num > 2:
                text_map[i].append("B")
                Cell(all_cell, pos_x=x, pos_y=y, state="болото")
            j += 1
        i += 1


    for i in text_map:
        print("".join(i))
    running = True
    while running:
        # внутри игрового цикла ещё один цикл
        # приема и обработки сообщений
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print(real_coord)
                if event.key == pygame.K_w:
                    if real_coord[1] + height // 100  < max_pos[1]:
                        all_cell.update(type_ev="up")
                        real_coord[1] += 1
                if event.key == pygame.K_d:
                    if real_coord[0] + width // 100 - 1 < max_pos[0]:
                        all_cell.update(type_ev="right")
                        real_coord[0] += 1
                if event.key == pygame.K_s:
                    if real_coord[1] > 0:
                        all_cell.update(type_ev="down")
                        real_coord[1] -= 1
                if event.key == pygame.K_a:
                    if real_coord[0] > 0:
                        all_cell.update(type_ev="left")
                        real_coord[0] -= 1
                print(real_coord)
            if event.type == pygame.MOUSEBUTTONDOWN:
                all_cell.update(type_ev="click")
            if event.type == pygame.QUIT:
                running = False
            all_cell.update(event)

        # отрисовка и изменение свойств объектов
        # ...
        all_cell.draw(screen)
        # обновление экрана
        pygame.display.flip()
    pygame.quit()