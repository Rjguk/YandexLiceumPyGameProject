import os
import sys
import  random
import numpy as np
import pygame
from pygame.display import update

from map_generator import generation



real_coord = [0, 0]
max_pos = [50, 50]
game_mode = ["None", 0]
person_positions = []
inf_window = [[], []]



class Cell(pygame.sprite.Sprite):
    image = {"пустая": pygame.image.load("pic\\ячейка_пустая.png"),
             "луг": pygame.image.load("pic\\ячейка_луг.png"),
             "лес": pygame.image.load("pic\\ячейка_лес.png"),
             "вода": pygame.image.load("pic\\ячейка_вода.png"),
             "болото": pygame.image.load("pic\\ячейка_болото.png")}

    def __init__(self, *group, state="пустая", pos_x=0, pos_y=0, rx=0, ry=0):
        super().__init__(*group)
        self.state = state
        if clear_map[ry, rx]:
            self.image = Cell.image[self.state]
        else:
            self.image = Cell.image["пустая"]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.rx = rx
        self.ry = ry


    def update(self, type_ev="", ev_pos=(0, 0), vision=1):
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
                if game_mode[0] == "Move":
                    if game_mode[1] == 1:
                        if self.state != "вода" and self.rect.y != 0 and self.rect.x != 1100:
                            all_person.update(type_ev="move", coord=(self.rect.x, self.rect.y))
                        game_mode[1] = 0

                    else:
                        game_mode[1] = 1
                else:
                    print(self.state)
                if game_mode[0] == "Information":
                    if game_mode[1] == 0:
                        game_mode[1] = 1
                        inf_window[0], inf_window[1] = information_menu(name=self.state, position=(self.rect.x, self.rect.y),
                                                                        )
        elif type_ev == "fog":
            vis = (vision + 1) * 100
            if ev_pos[0] - vis < self.rect.x < ev_pos[0] + vis and ev_pos[1] - vis < self.rect.y < ev_pos[1] + vis:
                clear_map[self.ry, self.rx] = 1
                self.image = Cell.image[self.state]




class Person(pygame.sprite.Sprite):
    image = {"стандартный": pygame.image.load("pic\\человек.png"),
            }

    def __init__(self, *group, state="стандартный", pos_x=127, pos_y=117, characteristics=None):
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
        person_positions.append((self.rect.x, self.rect.y))
        self.vision = characteristics["зрение"]
        self.endurance = characteristics["выносливость"]
        self.actions = self.endurance
        all_cell.update(type_ev="fog", ev_pos=(self.rect.x - 27, self.rect.y - 17), vision=self.vision)

    def wrighting(self, x=0, y=0,):
        pos = person_positions.index((self.rect.x, self.rect.y))
        self.rect.x += x - self.rect.x + 27
        self.rect.y += y - self.rect.y + 17
        person_positions[pos] = (self.rect.x, self.rect.y)

    def update(self, type_ev="", coord=(0, 0)):
        if type_ev == "up":
            pos = person_positions.index((self.rect.x, self.rect.y))
            self.rect.y += 100
            person_positions[pos] = (self.rect.x, self.rect.y)
        elif type_ev == "down":
            pos = person_positions.index((self.rect.x, self.rect.y))
            self.rect.y -= 100
            person_positions[pos] = (self.rect.x, self.rect.y)
        elif type_ev == "right":
            pos = person_positions.index((self.rect.x, self.rect.y))
            self.rect.x -= 100
            person_positions[pos] = (self.rect.x, self.rect.y)
        elif type_ev == "left":
            pos = person_positions.index((self.rect.x, self.rect.y))
            self.rect.x += 100
            person_positions[pos] = (self.rect.x, self.rect.y)
        elif type_ev == "click":
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if game_mode[0] == "None":
                    if self.actions > 0:
                        game_mode[0] = "Move"
                        self.mode = "Move"
                if game_mode[0] == "Information":
                    game_mode[1] = 1
                    inf_window[0], inf_window[1] = information_menu(name="Человек", position=(self.rect.x, self.rect.y),
                                                                    выносливость=self.endurance, зрение=self.vision,
                                                                    действия=self.actions)

        elif type_ev == "move":
            if self.mode == "Move":
                if coord[0] - 200 < self.rect.x - 27 < coord[0] + 200 and coord[1] - 200 < self.rect.y - 17 < coord[1] + 200:
                    self.wrighting(x=coord[0], y=coord[1])
                    all_cell.update(type_ev="fog", ev_pos=(self.rect.x - 27, self.rect.y - 17), vision=self.vision)
                    self.actions -= 1
                self.mode = "None"
                game_mode[0] = "None"
        elif type_ev == "next_turn":
            self.actions = self.endurance



class Bolder(pygame.sprite.Sprite):
    def __init__(self, *group, position="верхняя"):
        super().__init__(*group)
        if position == "верхняя":
            self.image = pygame.image.load("pic\\рамка верхняя.png")
            self.rect = self.image.get_rect()
            self.rect.x = 0
            self.rect.y = 0
        else:
            self.image = pygame.image.load("pic\\рамка боковая.png")
            self.rect = self.image.get_rect()
            self.rect.x = 1100
            self.rect.y = 0



class GameButton(pygame.sprite.Sprite):
    image = {"информация": pygame.image.load("pic\\кнопка_информация.png"),
             }
    def __init__(self, *group, state="информация", pos_x=1100, pos_y=100):
        super().__init__(*group)
        self.state = state
        self.image = GameButton.image[self.state]
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self, type_ev=""):
        if self.state == "информация":
            if type_ev == "click":
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    if game_mode[0] != "Information":
                        game_mode[0] = "Information"
                    else:
                        game_mode[0] = "None"
                        game_mode[1] = 0
            if type_ev == "information":
                if game_mode[0] != "Information":
                    game_mode[0] = "Information"
                else:
                    game_mode[0] = "None"
                    game_mode[1] = 0



def world_generation(size):
    stop = 1
    text_map_func = []
    while stop != 0:
        stop = 1
        np_map = generation(shape=size)
        for j in range(size):
            test = []
            for i in range(size):
                test.append(np_map[i][j])
            if len(set(test)) == 1:
                stop = 2
                break
        if stop != 2:
            stop = 0
    i = 0
    j = 0
    for y in range(height - size * 100, height, 100):
        text_map_func.append([])
        j = 0
        for x in range(0, size * 100, 100):
            num = np_map[i][j]
            if num == 0:
                text_map_func[i].append("~")
                Cell(all_cell, pos_x=x, pos_y=y, state="вода", rx=j, ry=i)
            if num == 1:
                text_map_func[i].append("L")
                Cell(all_cell, pos_x=x, pos_y=y, state="луг", rx=j, ry=i)
            if num == 2:
                text_map_func[i].append("F")
                Cell(all_cell, pos_x=x, pos_y=y, state="лес", rx=j, ry=i)
            if num > 2:
                text_map_func[i].append("B")
                Cell(all_cell, pos_x=x, pos_y=y, state="болото", rx=j, ry=i)
            j += 1
        i += 1
    char = {
        "зрение" : 3,
        "выносливость" : 2
    }
    Person(all_person, characteristics=char)
    char = {
        "зрение": 2,
        "выносливость": 3
    }
    Person(all_person, pos_x=227, pos_y=217, characteristics=char)
    Bolder(all_inter)
    Bolder(all_inter, position="боковая")
    GameButton(all_inter)

    for i in text_map_func:
        print("".join(i))
    return text_map_func

def information_menu(name="", position=(300, 300), **inf):
    window_x = 300
    window_y = (len(inf) + 1) * 40
    if window_x + position[0] > 1200:
        new_position_x = position[0] - window_x
    else:
        new_position_x = position[0]
    if window_y + position[1] > 900:
        new_position_y = position[1] - window_y
    else:
        new_position_y = position[1]

    pos_new_screen = [(new_position_x, new_position_y), (new_position_x + 10, new_position_y + 10)]
    new_screen = [pygame.Surface((window_x, window_y))]
    pygame.draw.rect(new_screen[0], (139, 139, 139), (0, 0, window_x, window_y))
    pygame.draw.rect(new_screen[0], (57, 57, 57), (0, 0, window_x, window_y), 5)
    #bahnschrift semibold
    font = pygame.font.SysFont(None, 31)
    new_screen.append(font.render(name, True, (0, 0, 0)))
    for el in inf:
        new_screen.append(font.render(str(el) + ":   " + str(inf[el]), True, (0, 0, 0)))
        pos_new_screen.append((pos_new_screen[-1][0], pos_new_screen[-1][1] + 40))
    return  new_screen, pos_new_screen


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1200, 900
    screen = pygame.display.set_mode(size)
    clear_map = np.zeros(size)
    all_cell = pygame.sprite.Group()
    all_person = pygame.sprite.Group()
    all_inter = pygame.sprite.Group()
    text_map = world_generation(max_pos[0])
    turn = 1
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print(real_coord)
                if event.key == pygame.K_w:
                    if real_coord[1] + height // 100 - 1 < max_pos[1]:
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
                if event.key == pygame.K_SPACE:
                    all_cell.update(type_ev="next_turn")
                    all_person.update(type_ev="next_turn")
                if event.key == pygame.K_q:
                    all_inter.update(type_ev="information")
                print(real_coord)
            if event.type == pygame.MOUSEBUTTONDOWN:
                all_person.update(type_ev="click")
                all_cell.update(type_ev="click")
                all_inter.update(type_ev="click")
            if event.type == pygame.QUIT:
                running = False
            all_cell.update(event)

        # отрисовка и изменение свойств объектов
        # ...
        all_cell.draw(screen)
        all_person.draw(screen)
        all_inter.draw(screen)
        if game_mode == ["Information", 1]:

            window, window_pos = inf_window[0], inf_window[1]
            j = 0
            for i in window:
                screen.blit(i, window_pos[j])
                j += 1
        # обновление экрана
        pygame.display.flip()
    pygame.quit()