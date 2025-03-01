import os
import sys
import  random
import numpy as np
import pygame
from map_generator import generation
from name_generator import name_generation


real_coord = [0, 0]
max_pos = [250, 250]
game_mode = ["None", 0]
person_positions = []
rect_of_choice = [0]
inf_window = [[], []]
building_place = [[]]
date_pic = [0]
num_text = []
nums = []
cost = []
window_pos = []
places = [0]
is_trader = [0]
landing_pos = [-1, -1]

resources = {"брёвна" : 1000,
             "торф" : 1000,
             "камни" : 600,
             "железная руда": 1000,
             "железный слиток": 0,
             "золотая руда": 1000,
             "золотой слиток": 0,
             "золотое изделие": 0,
             "золотая бижутерия": 0,
             "ружьё": 0,
             "еда": 2000,
             "инструменты": 30,
             "науч. оборуд.": 100,
             "исследования" : 1,}

build = [["Дом (позволяет поселить в нём трёх человек)", {"брёвна": 25, "камни": 10}],
             ["Лесопилка (добывает брёвна)", {"брёвна": 10, "инструменты" : 3, "камни": 10}],
             ["Карьер (добывает камни и полезные ископаемые)", {"брёвна": 8, "инструменты": 3}],
             ["Станция по добыче торфа (добывает торф)", {"брёвна": 10, "инструменты": 3}],
             ["Кузница", {"камни": 30, "брёвна": 20, "инструменты": 6}],
             ["Посадочная площадка (позволяет торговцам прилетать в поселение)", {"камни": 40}],
             ["Научный дом (приносит исследования)", {"брёвна": 25, "камни": 10, "науч. оборуд.": 5}],]

forge = {"инструменты": [3, "железный слиток"],
         "железный слиток": [1, "железная руда"],
         "золотой слиток": [1, "золотая руда"],
         "золотое изделие": [3, "золотой слиток"],
         "золотая бижутерия": [1, "золотой слиток"],
         "ружьё": [6, "железный слиток"],
         }

trade = {"брёвна" : 10,
         "торф" : 5,
         "железный слиток": 20,
         "золотой слиток": 25,
         "золотое изделие": 90,
         "золотая бижутерия": 30,
         "ружьё": 100,
         "еда": 1,
         "инструменты": 60,
         "науч. оборуд.": 200,
         }

trade_f = {}
trade_s = {}

class Cell(pygame.sprite.Sprite):
    image = {"пустая": pygame.image.load("pic\\ячейка_пустая.png"),
             "луг": pygame.image.load("pic\\ячейка_луг.png"),
             "лес": pygame.image.load("pic\\ячейка_лес.png"),
             "вода": pygame.image.load("pic\\ячейка_вода.png"),
             "болото": pygame.image.load("pic\\ячейка_болото.png"),
             "кузница": pygame.image.load("pic\\ячейка_кузница.png"),
             "лесопилка": pygame.image.load("pic\\ячейка_лесопилка.png"),
             "исследовательский дом": pygame.image.load("pic\\ячейка_центр_исследований.png"),
             "дом": pygame.image.load("pic\\ячейка_дом.png"),
             "станция по добыче торфа": pygame.image.load("pic\\ячейка_добыча_торфа.png"),
             "карьер": pygame.image.load("pic\\ячейка_карьер.png"),
             "площадка для дирижабля": pygame.image.load("pic\\ячейка_площадка.png"),
             "стройка": pygame.image.load("pic\\ячейка_стройка.png")}

    all_b = ["дом", "лесопилка", "карьер", "станция по добыче торфа", "кузница",
             "площадка для дирижабля", "исследовательский дом"]

    all_b_l = ["D", "T", "M", "S", "K", "A", "C"]

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
        self.selected = 0
        self.rx = rx
        self.ry = ry
        self.timer = []
        self.task = []
        self.fuel = "брёвна"
        self.stock = 0
        self.metal = random.choice(["R", "R", "R", "R" "R", "R", "I", "I", "I", "G"])
        if self.state == "лес":
            self.stock = 60
        elif self.state == "болото":
            self.stock = 180
        elif self.state == "луг":
            self.stock = 60

    def update(self, type_ev="", ev_pos=(0, 0), vision=1, building=0, forge_task=None):
        CELL_LEN = 100
        if type_ev == "up":
            self.rect.y += CELL_LEN
        elif type_ev == "down":
            self.rect.y -= CELL_LEN
        elif type_ev == "right":
            self.rect.x -= CELL_LEN
        elif type_ev == "left":
            self.rect.x += CELL_LEN
        elif type_ev == "click":
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if game_mode[0] == "None" and self.state == "кузница":
                    game_mode[0] = "Forge"
                    self.selected = 1
                    inf_window[0], inf_window[1] = forge_menu(forge, fuel=self.fuel)
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
                        self.selected = 1
                        game_mode[1] = 1
                        if self.state == "стройка":
                            inf_window[0], inf_window[1] = information_menu(name=self.state,
                                                                            осталось=self.timer[0][0],
                                                                            position=(self.rect.x, self.rect.y),)
                        else:
                            inf_window[0], inf_window[1] = information_menu(name=self.state,
                                                                            position=(self.rect.x, self.rect.y), )
                if game_mode[0] == "Building":
                    if game_mode[1] == 0:
                        game_mode[1] = 1
                        building_place[0] = [self.ry, self.rx]
                        inf_window[0], inf_window[1] = building_menu(position=(self.rect.x, self.rect.y),)
        elif type_ev == "fog":
            vis = (vision + 1) * CELL_LEN
            if ev_pos[0] - vis < self.rect.x < ev_pos[0] + vis and ev_pos[1] - vis < self.rect.y < ev_pos[1] + vis:
                clear_map[self.ry, self.rx] = 1
                self.image = Cell.image[self.state]
        elif type_ev == "building" and building_place[0] == [self.ry, self.rx]:
            building_res = build[building][-1]
            if (self.state == "луг" and building in [0, 2, 4, 5 ,5]) or (self.state == "болото" and building == 3)\
                    or (self.state == "лес" and building == 1):
                for k in building_res:
                    if not (k in resources and building_res[k] <= resources[k]):
                        break
                else:
                    for l in building_res:
                        resources[l] -= building_res[l]
                        self.state = "стройка"
                        self.image = Cell.image[self.state]


                    self.timer.append([[20, 12, 12, 12, 40, 80, 20][building], building])
        elif type_ev == "next_turn":
            for p in all_person:
                if pygame.sprite.collide_mask(self, p):
                    if self.state == "лесопилка":
                        resources["брёвна"] += 1 + p.strength // 2 + max(p.strength, 2) % 2
                    elif self.state == "карьер" and self.stock > 1:
                        resources["камни"] += 1 + p.strength // 2 + max(p.strength, 2) % 2
                        if self.metal == "I":
                            resources["железная руда"] += 1
                            self.stock -= 1
                        elif self.metal == "G":
                            resources["золотая руда"] += 1
                            self.stock -= 1
                        self.stock -= 1 + p.strength // 2 + max(p.strength, 2) % 2
                    elif self.state == "станция по добыче торфа":
                        resources["торф"] += 1 + p.strength // 2 + max(p.strength, 2) % 2
                        self.stock -= 1 + p.strength // 2 + max(p.strength, 2) % 2
                    elif self.state == "исследовательский дом":
                        self.stock -= 1 + p.scince // 2 + max(p.scince, 2) % 2
                        1 + p.scince // 2 + max(p.scince, 2) % 2
                    elif self.state == "кузница":
                        if self.task:
                            need_res = forge[self.task[0]]
                            if (need_res[0]  <= resources[need_res[1]] and
                                    ["торф", "0", "брёвна"].index(self.fuel) + 1 <= resources[self.fuel]):
                                print(need_res[0])
                                print(need_res[1])
                                resources[need_res[1]] -= need_res[0]

                                resources[self.fuel] -= ["торф", "0", "брёвна"].index(self.fuel) + 1
                                resources[self.task[0]] += 1
                                del self.task[0]
                                print("end")
                    if self.stock < 1:
                        self.state = "луг"
                        self.image = Cell.image[self.image]
                    break
            for t in range(len(self.timer)):
                self.timer[t][0] -= 1
                if self.timer[t][0] == 0:
                    self.state = self.all_b[self.timer[t][1]]
                    b = list(text_map[self.ry])
                    b[self.rx] = self.all_b_l[self.timer[t][1]]
                    text_map[self.ry] = b
                    self.image = Cell.image[self.state]
                    if self.state == "дом":
                        places[0] += 3
                    del self.timer[t]
        elif type_ev == "dsel":
            self.selected = 0
        elif type_ev == "update_inf":
            if self.selected == 1:
                inf_window[0], inf_window[1] = information_menu(name=self.state,
                                                                position=(self.rect.x, self.rect.y), )
        elif type_ev == "forge" and self.state == "кузница" and self.selected == 1:
            print(0)
            for f in range(forge_task[1]):
                self.task.append(list(forge)[forge_task[0]])
        elif type_ev == "update_fuel":
            if self.selected == 1:
                if self.fuel == "брёвна":
                    self.fuel = "торф"
                else:
                    self.fuel = "брёвна"
                inf_window[0], inf_window[1] = forge_menu(forge, fuel=self.fuel)
        elif type_ev == "landing":
            if self.state == "площадка для дирижабля":
                landing_pos[0], landing_pos[1] = self.rect.x, self.rect.y



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
        self.selected = 0
        person_positions.append((self.rect.x, self.rect.y))
        self.vision = characteristics["зрение"]
        self.endurance = characteristics["выносливость"]
        self.actions = self.endurance
        self.saturation = characteristics["сытость"]
        self.mood = characteristics["настроение"]
        self.mhealth = characteristics["максимальное здоровье"]
        self.health = characteristics["здоровье"]
        self.science = characteristics["ум"]
        self.craft = characteristics["ремесло"]
        self.strength = characteristics["сила"]
        self.name = characteristics["имя"]

        all_cell.update(type_ev="fog", ev_pos=(self.rect.x - 27, self.rect.y - 17), vision=self.vision)

    def wrighting(self, x=0, y=0,):
        pos = person_positions.index((self.rect.x, self.rect.y))
        self.rect.x += x - self.rect.x + 27
        self.rect.y += y - self.rect.y + 17
        person_positions[pos] = (self.rect.x, self.rect.y)

    def update(self, type_ev="", coord=(0, 0)):
        CELL_LEN = 100
        if type_ev == "up":
            pos = person_positions.index((self.rect.x, self.rect.y))
            self.rect.y += CELL_LEN
            person_positions[pos] = (self.rect.x, self.rect.y)
        elif type_ev == "down":
            pos = person_positions.index((self.rect.x, self.rect.y))
            self.rect.y -= CELL_LEN
            person_positions[pos] = (self.rect.x, self.rect.y)
        elif type_ev == "right":
            pos = person_positions.index((self.rect.x, self.rect.y))
            self.rect.x -= CELL_LEN
            person_positions[pos] = (self.rect.x, self.rect.y)
        elif type_ev == "left":
            pos = person_positions.index((self.rect.x, self.rect.y))
            self.rect.x += CELL_LEN
            person_positions[pos] = (self.rect.x, self.rect.y)
        elif type_ev == "click":
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if game_mode[0] == "None":
                    if self.actions > 0:
                        game_mode[0] = "Move"
                        self.mode = "Move"
                if game_mode[0] == "Information":
                    self.selected = 1
                    game_mode[1] = 1
                    inf_window[0], inf_window[1] = information_menu(name=self.name, position=(self.rect.x, self.rect.y),
                                                                    выносливость=self.endurance, сила=self.strength,
                                                                    зрение=self.vision,
                                                                    ремесло=self.craft, ум=self.science,
                                                                    здоровье=str(self.health) + "/" + str(self.mhealth),
                                                                    настроение=str(self.mood * 20) + "%",
                                                                    сытость=self.saturation,
                                                                    действия=self.actions)

        elif type_ev == "move":
            if self.mode == "Move":
                if (coord[0] - CELL_LEN * 2 < self.rect.x - 27 < coord[0] + CELL_LEN * 2 and coord[1] - CELL_LEN * 2 <
                        self.rect.y - 17 < coord[1] + CELL_LEN * 2):
                    self.wrighting(x=coord[0], y=coord[1])
                    all_cell.update(type_ev="fog", ev_pos=(self.rect.x - 27, self.rect.y - 17), vision=self.vision)
                    self.actions -= 1
                self.mode = "None"
                game_mode[0] = "None"
        elif type_ev == "next_day":
            if resources["еда"] > 1:
                resources["еда"] -= 2
                self.saturation = 10
            elif resources["еда"] > 0:
                resources["еда"] -= 1
                self.saturation -= 1
            else:
                self.saturation -= 2
            if self.saturation < 1:
                self.kill()
        elif type_ev == "next_turn":
            self.actions = max(0, self.endurance - (2 - (self.saturation + 1) // 5))
        elif type_ev == "dsel":
            self.selected = 0
        elif type_ev == "update_inf":
            if self.selected == 1:
                inf_window[0], inf_window[1] = information_menu(name=self.name, position=(self.rect.x, self.rect.y),
                                                                выносливость=self.endurance, сила=self.strength,
                                                                зрение=self.vision,
                                                                ремесло=self.craft, ум=self.science,
                                                                здоровье=str(self.health) + "/" + str(self.mhealth),
                                                                настроение=str(self.mood * 20) + "%",
                                                                сытость=self.saturation,
                                                                действия=self.actions)



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
             "строительство": pygame.image.load("pic\\кнопка_строительства.png"),
             "ресурсы": pygame.image.load("pic\\кнопка_ресурсы.png"),
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
                        all_cell.update(type_ev="dsel")
                        all_person.update(type_ev="dsel")
            if type_ev == "information":
                if game_mode[0] != "Information":
                    game_mode[0] = "Information"
                else:
                    game_mode[0] = "None"
                    game_mode[1] = 0
                    all_cell.update(type_ev="dsel")
                    all_person.update(type_ev="dsel")
        if self.state == "строительство":
            if type_ev == "click":
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    if game_mode[0] != "Building":
                        game_mode[0] = "Building"
                    else:
                        game_mode[0] = "None"
                        game_mode[1] = 0

            if type_ev == "building":
                if game_mode[0] != "Building":
                    game_mode[0] = "Building"
                else:
                    game_mode[0] = "None"
                    game_mode[1] = 0
        if self.state == "ресурсы":
            if type_ev == "click":
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    if game_mode[0] != "Resources":
                        game_mode[0] = "Resources"
                        inf_window[0], inf_window[1] = resources_menu(resources)

                    else:
                        game_mode[0] = "None"
                        game_mode[1] = 0
            if type_ev == "resources":
                if game_mode[0] != "Resources":
                    game_mode[0] = "Resources"
                    inf_window[0], inf_window[1] = resources_menu(resources)
                else:

                    game_mode[0] = "None"
                    game_mode[1] = 0
            if type_ev == "update_inf":
                inf_window[0], inf_window[1] = resources_menu(resources)



class DateInterface(pygame.sprite.Sprite):
    image = {"1": pygame.image.load("pic\\ход1.png"),
             "2": pygame.image.load("pic\\ход2.png"),
             "3": pygame.image.load("pic\\ход3.png"),
             "4": pygame.image.load("pic\\ход4.png"),
             }

    def __init__(self, *group, state="1"):
        super().__init__(*group)
        self.state = state
        self.image = DateInterface.image[self.state]
        self.rect = self.image.get_rect()
        self.rect.x = 1051
        self.rect.y = 0

    def update(self, type_ev="next_turn"):
        if type_ev == "next_turn":
            self.state = str(turn)
            self.image = DateInterface.image[self.state]
            font = pygame.font.SysFont(None, 30)
            date_pic[0] = font.render(".".join(list(map(str, date))), True, (0, 0, 0))



class Trader(pygame.sprite.Sprite):
    def __init__(self, *group, x_pos=0, y_pos=0):
        super().__init__(*group)
        self.image = pygame.image.load("pic\\дирижабль.png")
        self.rect = self.image.get_rect()
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.rect.x = x_pos
        self.rect.y = y_pos
    def update(self, *args, type_ev="", pos=(0, 0)):
        if type_ev == "trade":
            if game_mode[0] != "Trade":
                game_mode[0] = "Trade"
                inf_window[0], inf_window[1] = trade_menu(resources, trade)
            else:
                game_mode[0] = "None"
        elif type_ev == "spawn":
            print(pos)
            print(is_trader)
            self.rect.x, self.rect.y = pos




def world_generation(size):
    stop = 1
    text_map_func = []
    np_metal_map = []
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
    while stop != 0:
        stop = 1
        np_metal_map = generation(shape=size)
        for j in range(size):
            test = []
            for i in range(size):
                test.append(np_metal_map[i][j])
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
    for p in range(9):
        char = {
            "зрение": random.randint(1, 4),
            "выносливость": random.randint(1, 4),
            "сытость": random.randint(7, 10),
            "максимальное здоровье": 5,
            "здоровье": 5,
            "настроение": 5,
            "ремесло": random.randint(1, 3),
            "сила": random.randint(1, 3),
            "ум": random.randint(0, 3),
            "имя": name_generation()
        }
        Person(all_person, characteristics=char, pos_y=random.choice([100, 200, 300, 400, 500, 600, 700, 800]) + 17,
               pos_x=random.choice([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]) + 27)
    Bolder(all_inter)
    Bolder(all_inter, position="боковая")
    GameButton(all_inter)
    GameButton(all_inter, state="строительство", pos_x=1100, pos_y=200)
    GameButton(all_inter, state="ресурсы", pos_x=1100, pos_y=300)
    DateInterface(all_inter, state="1")
    Trader(all_trader)

    for i in text_map_func:
        print("".join(i))
    return text_map_func, np_metal_map


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


def building_menu(position=(300, 300)):
    window_x = 550
    window_y = 350
    if window_x + position[0] > 1200:
        new_position_x = position[0] - window_x
    else:
        new_position_x = position[0]
    if window_y + position[1] > 900:
        new_position_y = position[1] - window_y
    else:
        new_position_y = position[1]
    font = pygame.font.SysFont(None, 20)
    pos_new_screen = [(new_position_x, new_position_y), [new_position_x + 10, new_position_y + 50],
                      (new_position_x + 10, new_position_y + 10)]
    new_screen = [pygame.Surface((window_x, window_y)),  pygame.Surface((535, 20)),
                  font.render("Строения", True, (0, 0, 0))]
    pygame.draw.rect(new_screen[0], (139, 139, 139), (0, 0, window_x, window_y))
    pygame.draw.rect(new_screen[0], (57, 57, 57), (0, 0, window_x, window_y), 5)
    pygame.draw.rect(new_screen[1], (255, 255, 255), (0, 0, 535, 20))
    rect_of_choice[0] = pos_new_screen[1][1]
    #bahnschrift semibold
    for el in build:
        res_line = ""
        for i in el[1]:
            res_line += i + " " + str(el[1][i]) + "  "
        new_screen.append(font.render(el[0] + ": " + res_line, True, (0, 0, 0)))
        pos_new_screen.append((pos_new_screen[-1][0], pos_new_screen[-1][1] + 40))
    return  new_screen, pos_new_screen


def resources_menu(inf):
    window_x = 300
    window_y = (len(inf) + 1) * 40
    for i in inf:
        if inf[i] == 0:
            window_y -= 40
    position_x = 0
    position_y = 100

    pos_new_screen = [(position_x, position_y), (position_x + 10, position_y + 10)]
    new_screen = [pygame.Surface((window_x, window_y))]
    pygame.draw.rect(new_screen[0], (139, 139, 139), (0, 0, window_x, window_y))
    pygame.draw.rect(new_screen[0], (57, 57, 57), (0, 0, window_x, window_y), 5)
    #bahnschrift semibold
    font = pygame.font.SysFont(None, 31)
    new_screen.append(font.render("Склад:", True, (0, 0, 0)))
    for el in inf:
        if inf[el] != 0:
            new_screen.append(font.render(str(el) + ":   " + str(inf[el]), True, (0, 0, 0)))
            pos_new_screen.append((pos_new_screen[-1][0], pos_new_screen[-1][1] + 40))
    return  new_screen, pos_new_screen


def forge_menu(inf, fuel="брёвна"):
    window_x = 600
    window_y = (len(inf) + 2) * 40
    position_x = 0
    position_y = 100
    font = pygame.font.SysFont(None, 20)
    pos_new_screen = [(position_x, position_y), [position_x + 10, position_y + 50],
                      (position_x + 10, position_y + 10)]
    new_screen = [pygame.Surface((window_x, window_y)), pygame.Surface((280, 20)),
                  font.render(fuel, True, (0, 0, 0))]
    pygame.draw.rect(new_screen[0], (139, 139, 139), (0, 0, window_x, window_y))
    pygame.draw.rect(new_screen[0], (57, 57, 57), (0, 0, window_x, window_y), 5)
    pygame.draw.rect(new_screen[1], (255, 255, 255), (0, 0, 280, 20))
    rect_of_choice[0] = pos_new_screen[1][1]
    # bahnschrift semibold
    for el in forge:
        res_line = el + ": " + str(forge[el][0]) + " " + forge[el][1]
        new_screen.append(font.render(res_line, True, (0, 0, 0)))
        pos_new_screen.append((pos_new_screen[-1][0], pos_new_screen[-1][1] + 40))
    return new_screen, pos_new_screen


def trade_menu(inf, trade_d):
    window_x = 600
    window_y = (len(trade_d) + 3) * 40
    position_x = 0
    position_y = 100
    font = pygame.font.SysFont(None, 20)
    pos_new_screen = [(position_x, position_y), [position_x + 10, position_y + 50],
                      (position_x + 10, position_y + 10)]
    new_screen = [pygame.Surface((window_x, window_y)), pygame.Surface((280, 20)),
                  font.render("Торговля", True, (0, 0, 0))]
    pygame.draw.rect(new_screen[0], (139, 139, 139), (0, 0, window_x, window_y))
    pygame.draw.rect(new_screen[0], (57, 57, 57), (0, 0, window_x, window_y), 5)
    pygame.draw.rect(new_screen[1], (255, 255, 255), (0, 0, 280, 20))
    rect_of_choice[0] = pos_new_screen[1][1]
    # bahnschrift semibold
    for el in inf:
        if inf[el] != 0 and el in trade_d:
            new_screen.append(font.render(str(el) + ":   " + str(trade_d[el]), True, (0, 0, 0)))
            pos_new_screen.append((pos_new_screen[-1][0], pos_new_screen[-1][1] + 40))
    for el in trade_d:
        new_screen.append(font.render(str(el) + ":   " + str(trade_d[el]), True, (0, 0, 0)))
        if pos_new_screen[-1][0] < 100:
            pos_new_screen.append((pos_new_screen[-1][0] + 300, 150))
        else:
            pos_new_screen.append((pos_new_screen[-1][0], pos_new_screen[-1][1] + 40))
    return new_screen, pos_new_screen


def number_input(key=None):
    if len(num_text) < 10:
        if key == pygame.K_1:
            num_text.append("1")
        elif key == pygame.K_2:
            num_text.append("2")
        elif key == pygame.K_3:
            num_text.append("3")
        elif key == pygame.K_4:
            num_text.append("4")
        elif key == pygame.K_5:
            num_text.append("5")
        elif key == pygame.K_6:
            num_text.append("6")
        elif key == pygame.K_7:
            num_text.append("7")
        elif key == pygame.K_8:
            num_text.append("8")
        elif key == pygame.K_9:
            num_text.append("9")
        elif key == pygame.K_0:
            num_text.append("0")
    if key == pygame.K_BACKSPACE:
        if num_text:
            del num_text[-1]
    font = pygame.font.SysFont(None, 21)
    if nums:
        nums[0] = font.render("".join(num_text), True, (0, 0, 0))
    else:
        nums.append(font.render("".join(num_text), True, (0, 0, 0)))

if __name__ == '__main__':
    pygame.init()
    size = width, height = 1200, 900
    screen = pygame.display.set_mode(size)
    screen.fill((190, 180, 145))
    font = pygame.font.SysFont("times new roman", 40)
    screen.blit(font.render("Загрузка", True, (0, 0, 0)), (500, 450))
    pygame.display.flip()
    clear_map = np.zeros(size)
    all_cell = pygame.sprite.Group()
    all_person = pygame.sprite.Group()
    all_inter = pygame.sprite.Group()
    all_trader = pygame.sprite.Group()
    text_map, text_metal = world_generation(max_pos[0])
    timer = 38
    turn = 1
    date = [1, 1, 1834]
    CELL_LEN = 100
    INDENTATION = 40
    COLUMN_WIDTH = 300
    all_inter.update()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if real_coord[1] + height // CELL_LEN - 1 < max_pos[1]:
                        all_cell.update(type_ev="up")
                        all_person.update(type_ev="up")
                        real_coord[1] += 1
                if event.key == pygame.K_d:
                    if real_coord[0] + width // CELL_LEN - 1 < max_pos[0]:
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
                    if game_mode[0] != "Forge" or "Building":
                        if turn < 4:
                            turn += 1
                        else:
                            all_cell.update(type_ev="next_day")
                            all_person.update(type_ev="next_day")
                            timer += 1
                            if is_trader[0]:
                                is_trader[0] = 0
                            if timer % 60 == 0 and timer > 59:
                                all_cell.update(type_ev="landing")
                                if landing_pos != [-1, -1]:
                                    is_trader[0] = 1
                                    all_trader.update(type_ev="spawn", pos=(landing_pos[0], landing_pos[1]))
                                    if len(all_person) < places[0]:
                                        for p in range(places[0] - len(all_person)):
                                            if p < 5:
                                                char = {
                                                    "зрение": random.randint(1, 4),
                                                    "выносливость": random.randint(1, 4),
                                                    "сытость": random.randint(7, 10),
                                                    "максимальное здоровье": 5,
                                                    "здоровье": 5,
                                                    "настроение": 5,
                                                    "ремесло": random.randint(1, 3),
                                                    "сила": random.randint(1, 3),
                                                    "ум": random.randint(0, 3),
                                                    "имя": name_generation()
                                                }
                                                Person(all_person, characteristics=char, pos_y=random.choice(
                                                    range(0, height, CELL_LEN)) + 17,
                                                       pos_x=random.choice(
                                                           range(0, width - CELL_LEN, CELL_LEN)) + 27)

                            DAYS_AT_MONTH = 30
                            MONTHS_AT_YEAR = 12
                            turn = 1
                            if date[0] < DAYS_AT_MONTH:
                                date[0] += 1
                            else:
                                date[0] = 1
                                if date[1] < MONTHS_AT_YEAR:
                                    date[1] += 1
                                else:
                                    date[1] = 1
                                    date[2] += 1
                        all_cell.update(type_ev="next_turn")
                        all_person.update(type_ev="next_turn")
                        all_inter.update(type_ev="next_turn")
                        if game_mode == ["Information", 1]:
                            all_cell.update(type_ev="update_inf")
                            all_person.update(type_ev="update_inf")
                        if game_mode[0] == "Resources":
                            all_inter.update(type_ev="update_inf")
                    else:
                        game_mode[0] = "None"
                        all_cell.update(type_ev="dsel")
                if event.key == pygame.K_q:
                    all_inter.update(type_ev="information")
                if event.key == pygame.K_b:
                    all_inter.update(type_ev="building")
                if event.key == pygame.K_r:
                    all_inter.update(type_ev="resources")
                if event.key == pygame.K_t:
                    if is_trader[0]:
                        all_trader.update(type_ev="trade")
                if game_mode == ["Building", 1] or game_mode[0] == "Forge":
                    max_len = len(inf_window[0]) - 3
                    if event.key == pygame.K_DOWN:
                        if window_pos[1][1] + INDENTATION < rect_of_choice[0] + max_len * INDENTATION:
                            window_pos[1][1] += INDENTATION
                        else:
                            window_pos[1][1] -= (max_len - 1) * INDENTATION
                    if event.key == pygame.K_UP:
                        if window_pos[1][1] - INDENTATION >= rect_of_choice[0]:
                            window_pos[1][1] -= INDENTATION
                        else:
                            window_pos[1][1] += (max_len - 1) * INDENTATION
                    if event.key == pygame.K_RETURN:
                        if game_mode == ["Building", 1]:
                            all_cell.update(type_ev="building", building=(window_pos[1][1] - rect_of_choice[0])
                                                                         // INDENTATION)
                        else:
                            if num_text:
                                all_cell.update(type_ev="forge",
                                                forge_task=[(window_pos[1][1] - rect_of_choice[0]) // INDENTATION,
                                                            int("".join(num_text))])
                        game_mode = ["None", 0]
                if game_mode[0] == "Trade":
                    max_len_t = len(trade)
                    max_len_r = 0
                    for i in resources:
                        if resources[i] != 0:
                            if i in trade:
                                max_len_r += 1
                    if window_pos:
                        if window_pos[1][0] < COLUMN_WIDTH:
                            max_len = max_len_r
                        else:
                            max_len = max_len_t
                    if event.key == pygame.K_DOWN:
                        if window_pos[1][1] + INDENTATION < rect_of_choice[0] + max_len * INDENTATION:
                            window_pos[1][1] += INDENTATION
                        else:
                            window_pos[1][1] -= (max_len - 1) * INDENTATION
                    if event.key == pygame.K_UP:
                        if window_pos[1][1] - INDENTATION >= rect_of_choice[0]:
                            window_pos[1][1] -= INDENTATION
                        else:
                            window_pos[1][1] += (max_len - 1) * INDENTATION
                    if event.key == pygame.K_RIGHT:
                        if window_pos[1][0] < COLUMN_WIDTH:
                            window_pos[1][0] += COLUMN_WIDTH
                            window_pos[1][1] = rect_of_choice[0]
                        else:
                            window_pos[1][0] -= COLUMN_WIDTH
                            window_pos[1][1] = rect_of_choice[0]
                    if event.key == pygame.K_RETURN:
                        if window_pos[1][0] < COLUMN_WIDTH:
                            if num_text:
                                res_to_trade = []
                                for r in resources:
                                    if resources[r] > 0 and r in trade:
                                        res_to_trade.append(r)
                                th = (window_pos[1][1] - rect_of_choice[0]) // INDENTATION
                                trade_f[res_to_trade[th]] = int("".join(num_text)) * trade[res_to_trade[th]]
                        else:
                            if num_text:
                                th = (window_pos[1][1] - rect_of_choice[0]) // INDENTATION
                                trade_s[list(trade)[th]] = int("".join(num_text)) * trade[list(trade)[th]]
                    if event.key == pygame.K_g:
                        if trade_f:
                            if trade_s:
                                sum_d = 0
                                for td in trade_f:
                                    sum_d += trade_f[td]
                                for td in trade_s:
                                    sum_d -= trade_s[td]
                                if sum_d >= 0:
                                    for td in trade_f:
                                        resources[td] -= trade_f[td] // trade[td]
                                    for td in trade_s:
                                        resources[td] += trade_s[td] // trade[td]
                                    trade_f = {}
                                    trade_s = {}

                if game_mode[0] == "Forge":
                    number_input(event.key)
                    if event.key == pygame.K_f:
                        all_cell.update(type_ev="update_fuel")
                if game_mode[0] == "Trade":
                    number_input(event.key)

            if event.type == pygame.MOUSEBUTTONDOWN:
                all_person.update(type_ev="click")
                all_cell.update(type_ev="click")
                all_inter.update(type_ev="click")
            if event.type == pygame.QUIT:
                running = False

        # отрисовка и изменение свойств объектов
        all_cell.draw(screen)
        all_person.draw(screen)
        all_inter.draw(screen)
        if is_trader[0] == 1:
            all_trader.draw(screen)
        if game_mode == ["Information", 1]:
            window, window_pos = inf_window[0], inf_window[1]
            j = 0
            for i in window:
                screen.blit(i, window_pos[j])
                j += 1
        elif game_mode == ["Building", 1]:
            window, window_pos = inf_window[0], inf_window[1]
            j = 0
            for i in window:
                screen.blit(i, window_pos[j])
                j += 1
        elif game_mode[0] == "Resources":
            window, window_pos = inf_window[0], inf_window[1]
            j = 0
            for i in window:
                screen.blit(i, window_pos[j])
                j += 1
        elif game_mode[0] == "Forge":
            window, window_pos = inf_window[0], inf_window[1]
            j = 0
            for i in window:
                screen.blit(i, window_pos[j])
                j += 1
            num_x, num_y = window_pos[-1][0], window_pos[-1][1] + INDENTATION
            if nums:
                screen.blit(nums[0], (num_x, num_y))
        elif game_mode[0] == "Trade":
            window, window_pos = inf_window[0], inf_window[1]
            j = 0
            for i in window:
                screen.blit(i, window_pos[j])
                j += 1
            num_x, num_y = window_pos[-1][0], window_pos[-1][1] + INDENTATION
            if nums:
                if nums:
                    screen.blit(nums[0], (num_x - COLUMN_WIDTH, num_y))
                    screen.blit(nums[0], (num_x, num_y))
            font_for_sum = pygame.font.SysFont(None, 20)
            if trade_f:
                sum_d = 0
                for td in trade_f:
                    sum_d += trade_f[td]

                screen.blit(font_for_sum.render(str(sum_d), True, (0, 0, 0)), (num_x - COLUMN_WIDTH, num_y + INDENTATION))
            if trade_s:
                sum_d = 0
                for td in trade_s:
                    sum_d += trade_s[td]

                screen.blit(font_for_sum.render(str(sum_d), True, (0, 0, 0)), (num_x, num_y + INDENTATION))

        screen.blit(date_pic[0], (1071, 20))
        # обновление экрана
        pygame.display.flip()
    pygame.quit()