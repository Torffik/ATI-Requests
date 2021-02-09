import requests
import pygame
from PIL import Image
from io import BytesIO
import os


class Pole(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(maps)
        self.image = pygame.Surface((200, 50))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, (255, 255, 255), self.rect, 3)
        self.checked = False
        self.text = ''
        self.font = pygame.font.Font(None, 20)
        self.rect.x = x
        self.rect.y = y

    def on_it(self, pos):
        global record
        x = pos[0]
        y = pos[1]
        if self.rect.x <= x <= (self.rect.x + self.rect.width) and self.rect.y <= y <= (self.rect.y + self.rect.height):
            record = True
            print('не скосил')
        else:
            record = False
            print('cкосил')

    def update(self):
        if record:
            pygame.draw.rect(screen, pygame.Color('green'), self.rect, 3)
        else:
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 3)
        line = self.font.render(self.text, True, (255, 255, 255))
        line_rect = line.get_rect()
        line_rect.x = self.rect[0] + 2
        line_rect.y = self.rect[1] + 2
        screen.blit(line, line_rect)


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
        updates = False
        if left:
            karta.x -= 0.1
            updates = True
        if right:
            karta.x += 0.1
            updates = True
        if up:
            karta.y += 0.1
            updates = True
        if down:
            karta.y -= 0.1
            updates = True
        if pgup:
            updates = True
            karta.ro_x += 0.5
            if karta.ro_x >= 20:
                karta.ro_x = 20
            karta.ro_y += 0.5
            if karta.ro_y >= 20:
                karta.ro_y = 20
        if pgdown:
            updates = True
            karta.ro_x -= 0.5
            if karta.ro_x <= 0.005:
                karta.ro_x = 0.005
            karta.ro_y -= 0.5
            if karta.ro_y <= 0.005:
                karta.ro_y = 0.005
        if updates:
            picture = requests.get(
                f"https://static-maps.yandex.ru/1.x/?ll={self.x}%2C{self.y}&spn={self.ro_x},{self.ro_y}&l=map").content
            i = Image.open(BytesIO(picture))
            i.save('загруженное.png')
            self.image = pygame.image.load('загруженное.png')
            self.rect = self.image.get_rect()

def search(text):
    global karta
    text = '+'.join(text.split())
    print('Отправляемый запрос: ', text)
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={text}&format=json"
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        print(toponym_coodrinates, 'координаты запроса')
        coords = toponym_coodrinates.split()
        x = coords[0]
        y = coords[1]
        karta = Map(x, y)
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Биг прожект')
    size = width, height = 600, 600
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
    record = False
    text_line = Pole(10, 460)
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
                elif event.key == pygame.K_RETURN:
                    search(text_line.text)
                    text_line.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text_line.text = text_line.text[:-1]
                else:
                    if record:
                        text_line.text += event.unicode
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                text_line.on_it(event.pos)

        clock.tick(fps)
        maps.draw(screen)
        maps.update()
        pygame.display.flip()
        screen.fill((0, 0, 0))
    pygame.quit()
os.remove('загруженное.png')
