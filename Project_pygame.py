import os
import sys
from random import choice

import pygame

# Изображение не получится загрузить
# без предварительной инициализации pygame
# установка звуковых параметров перед
# инициализации pygame
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
# Название окна игры
pygame.display.set_caption('flash car')
# размеры окна по умолчанию
size = width, height = 450, 900
# создание окна
screen = pygame.display.set_mode(size)
# создание переменной для управления временем в игре
clock = pygame.time.Clock()
# Частота кадров в секунду по умолчанию
FPS = 60
# список чит-кодов для игры
CHEAT_CODES = ['nyancat', 'black', 'red', 'green']
# чит-код по умолчанию
code = 'green'
# создание групп спрайтов для игры по умолчанию
all_sprites = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()


# функция для загрузки изображения
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


# Спрайт дороги
class Road(pygame.sprite.Sprite):
    def __init__(self, x1, y1, y2):
        super(Road, self).__init__(all_sprites)
        self.image = pygame.Surface((19, y2 - y1))
        self.rect = self.image.get_rect()
        self.rect.x = x1
        self.rect.y = y1
        self.image.fill(pygame.Color('white'))

    # в течении времени линия меняет своё положение
    def update(self, *args):
        if self.rect.y == 900:
            self.rect.y = 0 - self.rect.height
        else:
            self.rect.y += 10


# Спрайт машины игрока
class Car(pygame.sprite.Sprite):
    cars = {'red': load_image('car_red.png'),
            'green': load_image('car_green.png'),
            'black': load_image('car_black.png'),
            'nyan_cat': load_image('nyncat.png')
            }

    # в зависимости от чит-кода задаётся изображение машины
    def __init__(self, code):
        super(Car, self).__init__(all_sprites)
        if code != 'nyancat':
            self.image = pygame.transform.scale(Car.cars[code], (120, 200))
        else:
            self.image = pygame.transform.scale(Car.cars['nyan_cat'], (110, 190))
        self.rect = self.image.get_rect()
        self.rect.x = 170
        self.rect.y = 900 - self.rect.height

    # Изменение положения машины
    # В зависимости соответствующей клавиши
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


# Спрайт препятствия
class Obstacle(pygame.sprite.Sprite):
    stone = load_image('large.png')
    tree = load_image('tree.png')
    sweet = load_image('sweet.png')

    # в зависимости от чит-кода задаётся изображение препятствия
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

    # если препятствие пройдено, то добавляется 1 очко и меняется положение препятствия
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


# функция аварийного закрытия игр
def terminate():
    pygame.quit()
    sys.exit()


# функция начала игры
def start_screen():
    # чит-код пользователя
    main_cod = ''
    # размер окна начала игры
    size = (920, 600)
    screen = pygame.display.set_mode(size)
    # после каждой новой игры значения ставятся по умолчанию
    global all_sprites, obstacle_group, code
    all_sprites = pygame.sprite.Group()
    obstacle_group = pygame.sprite.Group()
    code = 'green'
    # текст к заставке игры и её рендер
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
                # нажатие пробела для начала игры
                if event.key == pygame.K_SPACE:
                    return game(code)
                # проверка на нажатия нужных клавишь для активации чит-кода
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
    # размер окна игры
    size = width, height = 450, 900
    screen = pygame.display.set_mode(size)
    # загрузка музыки для игры и создание препятствий
    if code != 'nyancat':
        pygame.mixer.music.load(f'music/Sounds/{choice(range(1, 25))}.mp3')
        pygame.mixer.music.play(-1)
        obs = Obstacle(False)
    else:
        pygame.mixer.music.load(f'music/Nyan cat/Nyan Cat - Theme (8-bit).mp3')
        pygame.mixer.music.play(-1)
        obs = Obstacle(True)
    # создание спрайта машины и дороги
    car = Car(code)
    Road(150, 0, 200)
    Road(150, 250, 450)
    Road(150, 500, 700)
    Road(150, 750, 950)
    Road(300, 50, 250)
    Road(300, 300, 500)
    Road(300, 550, 750)
    Road(300, 800, 1000)
    # отображение очков на экран
    font = pygame.font.Font('font/pixel.ttf', 50)
    text_coord = 10
    run = True
    while run:
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            # событие нажатия клавиши для передвижения машины
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
        # проверка на столкновение машины с препятствием
        if pygame.sprite.spritecollideany(car, obstacle_group):
            run = False
    return game_over(obs.get_score())


# функция окончания игры
def game_over(score):
    # размер окна окончания игры
    size = (1024, 640)
    screen = pygame.display.set_mode(size)
    # загрузка музыки для окончания игры
    pygame.mixer.music.load(f'music/Game_over/{choice(range(1, 3))}.mp3')
    pygame.mixer.music.play(0)
    # текст окончания игры и его рендер
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
            # событие на нажатие кнопки для перезапуска игры
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pygame.mixer.music.stop()
                    return start_screen()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    start_screen()
