import os
import sys
import  random
import pygame
from pygame.examples.cursors import image
real_coord = [0, 0]
max_pos = [20, 20]
text_map = []

class Cell(pygame.sprite.Sprite):
    image = {"пустая": pygame.image.load("pic\\ячейка_пустая.png"),
             "луг": pygame.image.load("pic\\ячейка_луг.png"),
             "лес": pygame.image.load("pic\\ячейка_лес.png"),
             "море": pygame.image.load("pic\\ячейка_море.png")}

    def __init__(self, *group, state="пустая", pos_x=0, pos_y=0):
        super().__init__(*group)
        self.state = state
        a = ["пустая", "луг", "лес", "море"]
        self.state = a[random.randint(0, 3)]
        if self.state == "пустая":
            text_map[(pos_y  + max_pos[1] * 100 - height + 100) // 100].append(" ")
        elif self.state == "луг":
            text_map[(pos_y  + max_pos[1] * 100 - height + 100) // 100].append("L")
        elif self.state == "лес":
            text_map[(pos_y  + max_pos[1] * 100 - height + 100) // 100].append("F")
        elif self.state == "море":
            text_map[(pos_y  + max_pos[1] * 100 - height + 100) // 100].append("~")
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

if __name__ == '__main__':
    pygame.init()
    size = width, height = 1200, 900
    screen = pygame.display.set_mode(size)
    all_cell = pygame.sprite.Group()
    for i in range(height - (max_pos[1]) * 100 - 100, height, 100):
        text_map.append([])
        for j in range(0, (max_pos[0] + 1) * 100, 100):
            Cell(all_cell, pos_x=j, pos_y=i)
    print(text_map)
    for i in text_map:
        print("".join(i))
    running = True
    while running:
        # внутри игрового цикла ещё один цикл
        # приема и обработки сообщений
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.KEYDOWN:
                print(real_coord)
                if event.key == pygame.K_w:
                    if real_coord[1] + height // 100 - 1 < max_pos[1]:
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