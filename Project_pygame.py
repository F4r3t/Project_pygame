import os
import sys
from random import choice

import pygame

# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
pygame.display.set_caption('flash car')
size = width, height = 450, 900
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 60
CHEAT_CODES = ['nyancat', 'black', 'red', 'green']
code = 'green'
all_sprites = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('cache', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Road(pygame.sprite.Sprite):
    def __init__(self, x1, y1, y2):
        super(Road, self).__init__(all_sprites)
        self.image = pygame.Surface((19, y2 - y1))
        self.rect = self.image.get_rect()
        self.rect.x = x1
        self.rect.y = y1
        self.image.fill(pygame.Color('white'))

    def update(self, *args):
        if self.rect.y == 900:
            self.rect.y = 0 - self.rect.height
        else:
            self.rect.y += 10


class Car(pygame.sprite.Sprite):
    cars = {'red': load_image('car_red.png'),
            'green': load_image('car_green.png'),
            'black': load_image('car_black.png'),
            'nyan_cat': load_image('nyncat.png')
            }

    def __init__(self, code):
        super(Car, self).__init__(all_sprites)
        if code != 'nyancat':
            self.image = pygame.transform.scale(Car.cars[code], (120, 200))
        else:
            self.image = pygame.transform.scale(Car.cars['nyan_cat'], (110, 190))
        self.rect = self.image.get_rect()
        self.rect.x = 170
        self.rect.y = 900 - self.rect.height

    def update(self, *args):
        if args:
            if args[0].key == pygame.K_LEFT:
                if self.rect.x == 320:
                    self.rect.x = 170
                elif self.rect.x == 170:
                    self.rect.x = 20
            elif args[0].key == pygame.K_RIGHT:
                if self.rect.x == 20:
                    self.rect.x = 170
                elif self.rect.x == 170:
                    self.rect.x = 320


class Obstacle(pygame.sprite.Sprite):
    stone = load_image('large.png')
    tree = load_image('tree.png')
    sweet = load_image('sweet.png')

    def __init__(self, nyancat):
        super(Obstacle, self).__init__(all_sprites, obstacle_group)
        self.code = nyancat
        if not nyancat:
            self.image = pygame.transform.scale(choice([Obstacle.stone, Obstacle.tree]), (120, 90))
        else:
            self.image = pygame.transform.scale(Obstacle.sweet, (120, 90))
        self.rect = self.image.get_rect()
        self.rect.x = choice([20, 170, 320])
        self.rect.y = 0 - self.rect.height
        self.v = 10
        self.score = 0

    def update(self, *args):
        if self.rect.y >= height:
            if self.code:
                self.image = pygame.transform.scale(Obstacle.sweet, (120, 90))
            else:
                self.image = pygame.transform.scale(choice([Obstacle.stone, Obstacle.tree]),
                                                    (120, 90))
            self.v += 0.1
            self.score += 1
            self.rect.x = choice([20, 170, 320])
            self.rect.y = 0 - self.rect.height
        else:
            self.rect.y += self.v

    def get_score(self):
        return self.score


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    main_cod = ''
    size = (920, 600)
    screen = pygame.display.set_mode(size)
    global all_sprites, obstacle_group, code
    all_sprites = pygame.sprite.Group()
    obstacle_group = pygame.sprite.Group()
    code = 'green'
    intro_text = ['Игра "Flash car"',
                  "Правила игры:",
                  "Ехать на машине, не задевая препятствия;",
                  'Управление происходит с помощью срелок влево и вправо.'
                  '',
                  'Нажмите кнопку space, чтобы начать игру']

    fon = pygame.transform.scale(load_image('fon.jpg'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font('font/pixel.ttf', 30)
    text_coord = 20
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('Red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return game(code)
                if event.key == pygame.K_r:
                    main_cod += 'r'
                elif event.key == pygame.K_e:
                    main_cod += 'e'
                elif event.key == pygame.K_d:
                    main_cod += 'd'
                elif event.key == pygame.K_n:
                    main_cod += 'n'
                elif event.key == pygame.K_g:
                    main_cod += 'g'
                elif event.key == pygame.K_y:
                    main_cod += 'y'
                elif event.key == pygame.K_a:
                    main_cod += 'a'
                elif event.key == pygame.K_c:
                    main_cod += 'c'
                elif event.key == pygame.K_t:
                    main_cod += 't'
                elif event.key == pygame.K_b:
                    main_cod += 'b'
                elif event.key == pygame.K_k:
                    main_cod += 'k'
                elif event.key == pygame.K_l:
                    main_cod += 'l'
                elif event.key == pygame.K_EQUALS:
                    main_cod = ''
        if len(main_cod) > len(max(CHEAT_CODES, key=lambda x: len(x))):
            main_cod = ''
        for cheat_code in CHEAT_CODES:
            if main_cod == cheat_code:
                code = cheat_code
        pygame.display.flip()
        clock.tick(FPS)


def game(code):
    size = width, height = 450, 900
    screen = pygame.display.set_mode(size)
    if code != 'nyancat':
        pygame.mixer.music.load(f'music/Sounds/{choice(range(1, 25))}.mp3')
        pygame.mixer.music.play(-1)
        obs = Obstacle(False)
    else:
        pygame.mixer.music.load(f'music/Nyan cat/Nyan Cat - Theme (8-bit).mp3')
        pygame.mixer.music.play(-1)
        obs = Obstacle(True)
    car = Car(code)
    Road(150, 0, 200)
    Road(150, 250, 450)
    Road(150, 500, 700)
    Road(150, 750, 950)
    Road(300, 50, 250)
    Road(300, 300, 500)
    Road(300, 550, 750)
    Road(300, 800, 1000)

    font = pygame.font.Font('font/pixel.ttf', 50)
    text_coord = 10
    run = True
    while run:
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                all_sprites.update(event)
        string_rendered = font.render(str(obs.get_score()), True, pygame.Color('White'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = width // 2
        text_coord = intro_rect.height
        screen.blit(string_rendered, intro_rect)
        all_sprites.update()
        clock.tick(FPS)
        pygame.display.flip()
        if pygame.sprite.spritecollideany(car, obstacle_group):
            run = False
    return game_over(obs.get_score())


def game_over(score):
    size = (1024, 640)
    screen = pygame.display.set_mode(size)
    pygame.mixer.music.load(f'music/Game_over/{choice(range(1, 3))}.mp3')
    pygame.mixer.music.play(0)
    text = ['    Game Over',
            f'    Score:{score}',
            '    Нажмите кнопку "R", чтобы начать заново']
    fon = pygame.transform.scale(load_image('game_over.jpg'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font('font/pixel.ttf', 30)
    text_coord = 50
    for line in text:
        string_rendered = font.render(line, True, pygame.Color('White'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pygame.mixer.music.stop()
                    return start_screen()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    start_screen()
