import requests
import pygame
from PIL import Image
from io import BytesIO
import os


class Map(pygame.sprite.Sprite):
    def __init__(self, x=55.958727, y=54.735150, ro_x=1.026457, ro_y=1.0219):
        super().__init__(maps)
        self.x = x
        self.y = y
        self.ro_x = ro_x
        self.ro_y = ro_y
        picture = requests.get(
            f"https://static-maps.yandex.ru/1.x/?ll={self.x}%2C{self.y}&spn={self.ro_x},{self.ro_y}&l=map").content
        i = Image.open(BytesIO(picture))
        i.save('загруженное.png')
        self.image = pygame.image.load('загруженное.png')
        self.rect = self.image.get_rect()

    def update(self):
        if left:
            karta.x -= 0.1
        if right:
            karta.x += 0.1
        if up:
            karta.y += 0.1
        if down:
            karta.y -= 0.1
        if pgup:
            karta.ro_x += 0.5
            if karta.ro_x >= 20:
                karta.ro_x = 20
            karta.ro_y += 0.5
            if karta.ro_y >= 20:
                karta.ro_y = 20
        if pgdown:
            karta.ro_x -= 0.5
            if karta.ro_x <= 0.5:
                karta.ro_x = 0.5
            karta.ro_y -= 0.5
            if karta.ro_y <= 0.5:
                karta.ro_y = 0.5

        picture = requests.get(
            f"https://static-maps.yandex.ru/1.x/?ll={self.x}%2C{self.y}&spn={self.ro_x},{self.ro_y}&l=map").content
        i = Image.open(BytesIO(picture))
        i.save('загруженное.png')
        self.image = pygame.image.load('загруженное.png')
        self.rect = self.image.get_rect()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Биг прожект')
    size = width, height = 600, 450
    screen = pygame.display.set_mode(size)
    running = True
    clock = pygame.time.Clock()
    maps = pygame.sprite.Group()
    fps = 30
    karta = Map()
    left = False
    right = False
    down = False
    up = False
    pgup = False
    pgdown = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    up = True
                elif event.key == pygame.K_DOWN:
                    down = True
                elif event.key == pygame.K_LEFT:
                    left = True
                elif event.key == pygame.K_RIGHT:
                    right = True
                elif event.key == pygame.K_PAGEUP:
                    pgup = True
                elif event.key == pygame.K_PAGEDOWN:
                    pgdown = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    up = False
                elif event.key == pygame.K_DOWN:
                    down = False
                elif event.key == pygame.K_LEFT:
                    left = False
                elif event.key == pygame.K_RIGHT:
                    right = False
                elif event.key == pygame.K_PAGEUP:
                    pgup = False
                elif event.key == pygame.K_PAGEDOWN:
                    pgdown = False


        clock.tick(fps)
        maps.draw(screen)
        maps.update()
        pygame.display.flip()
        screen.fill((0, 0, 0))
    pygame.quit()
os.remove('загруженное.png')