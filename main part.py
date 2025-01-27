import os
import sys
import  random
import pygame
from map_generator import generation


real_coord = [0, 0]
max_pos = [50, 50]
text_map = []
person_mode = ["None", 0]


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
        self.mask = pygame.mask.from_surface(self.image)
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
                if person_mode[0] == "Move":
                    if person_mode[1] == 1:
                        if self.state != "вода":
                            all_person.update(type_ev="move", coord=(self.rect.x, self.rect.y))
                            person_mode[1] = 0
                    else:
                        person_mode[1] = 1
                else:
                    print(self.state)



class Person(pygame.sprite.Sprite):
    image = {"стандартный": pygame.image.load("pic\\человек.png"),
            }

    def __init__(self, *group, state="стандартный", pos_x=27, pos_y=17):
        super().__init__(*group)
        self.state = state
        self.image = Person.image[self.state]
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.mode = "None"

    def update(self, type_ev="", coord=(0, 0)):
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
                if person_mode[0] == "None":
                    person_mode[0] = "Move"
                    self.mode = "Move"
        elif type_ev == "move":
            if self.mode == "Move":
                self.rect.x += coord[0] - self.rect.x + 27
                self.rect.y += coord[1] - self.rect.y + 17
                self.mode = "None"
                person_mode[0] = "None"



def world_generation():
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
    Person(all_person)
    Person(all_person, pos_x=127, pos_y=117)
    for i in text_map:
        print("".join(i))


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1200, 900
    screen = pygame.display.set_mode(size)
    all_cell = pygame.sprite.Group()
    all_person = pygame.sprite.Group()
    world_generation()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print(real_coord)
                if event.key == pygame.K_w:
                    if real_coord[1] + height // 100  < max_pos[1]:
                        all_cell.update(type_ev="up")
                        all_person.update(type_ev="up")
                        real_coord[1] += 1
                if event.key == pygame.K_d:
                    if real_coord[0] + width // 100 - 1 < max_pos[0]:
                        all_cell.update(type_ev="right")
                        all_person.update(type_ev="right")
                        real_coord[0] += 1
                if event.key == pygame.K_s:
                    if real_coord[1] > 0:
                        all_cell.update(type_ev="down")
                        all_person.update(type_ev="down")
                        real_coord[1] -= 1
                if event.key == pygame.K_a:
                    if real_coord[0] > 0:
                        all_cell.update(type_ev="left")
                        all_person.update(type_ev="left")
                        real_coord[0] -= 1
                print(real_coord)
            if event.type == pygame.MOUSEBUTTONDOWN:
                all_person.update(type_ev="click")
                all_cell.update(type_ev="click")
            if event.type == pygame.QUIT:
                running = False
            all_cell.update(event)

        # отрисовка и изменение свойств объектов
        # ...
        all_cell.draw(screen)
        all_person.draw(screen)
        # обновление экрана
        pygame.display.flip()
    pygame.quit()