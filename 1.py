import requests
import pygame
from PIL import Image
from io import BytesIO
import os

picture = requests.get(
    "https://static-maps.yandex.ru/1.x/?ll=55.958727%2C54.735150&spn=1.026457,1.0219&l=map").content
i = Image.open(BytesIO(picture))
i.save('загруженное.png')
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Покажи мне её!')
    size = width, height = 600, 450
    screen = pygame.display.set_mode(size)
    running = True
    pic = pygame.image.load('загруженное.png')
    screen.blit(pic, pic.get_rect())
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    pygame.quit()
os.remove('загруженное.png')