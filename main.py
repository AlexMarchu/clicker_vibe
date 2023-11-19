import pygame
import string


class RectangleButtons(pygame.sprite.Sprite):
    def __init__(self, data, start_image, clicked_image, name, group):
        super().__init__(group)
        self.rect = pygame.rect.Rect(*data)
        self.image = start_image
        self.start_image = start_image
        self.clicked_image = clicked_image
        self.__name = name
        self.counter = 0

    def is_clicked(self, x, y) -> bool:
        return self.rect.collidepoint(x, y)

    def set_clicked_image(self):
        self.image = self.clicked_image

    def set_start_image(self):
        self.image = self.start_image

    def __repr__(self):
        return self.__name

    def update(self, *args):
        self.counter += 1
        if self.counter > 10:
            self.set_start_image()
            self.counter = 0


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Clicker')
        self.click_image = pygame.image.load('assets/images/dron.png')
        self.click_image = pygame.transform.scale(self.click_image, (500, 500))

        self.name = ''
        self.base = []
        with open("base.txt", "r") as f:
            for line in f.readlines():
                info = line.split()
                self.base.append([" ".join([i for i in info[:-1]]), float(info[-1])])

        self.width = 600
        self.height = int(self.width * 1.4)
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.SRCALPHA)
        self.bg_image = pygame.transform.scale(pygame.image.load('assets/images/background.jpeg'),
                                               (self.width, self.height))
        self.window = "start"
        self.fonts = {
            "usual_text_font": pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 30),
            "settings_text_font": pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 15),
            "settings_plus_minus_font": pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 20),
        }

        self.buttons_bottom = pygame.sprite.Group()
        self.buttons_settings = pygame.sprite.Group()
        self.buttons_passive_upgrades = pygame.sprite.Group()
        self.buttons_active_upgrades = pygame.sprite.Group()
        self.clock = pygame.time.Clock()

        self.BUTTON_SETTINGS_MUSIC_ACTIVE = RectangleButtons(
            (self.width // 7 * 4 - 10, self.height // 7 + self.height // 70 - 10, 150, 30),
            None,
            None,
            "music_active",
            self.buttons_settings
        )

        self.BUTTON_SETTINGS_SOUND_ACTIVE = RectangleButtons(
            (self.width // 7 * 4, self.height // 7 + self.height // 27 * 2 + self.height // 70 * 3, 150, 30),
            None,
            None,
            "sound_active",
            self.buttons_settings
        )

        self.BUTTON_SETTINGS_MUSIC_VOLUME = RectangleButtons(
            (self.width // 7 * 4, self.height // 7 + self.height // 27 * 1 + self.height // 70 * 2, 150, 30),
            None,
            None,
            "music_volume",
            self.buttons_settings
        )

        self.BUTTON_SETTINGS_SOUND_VOLUME = RectangleButtons(
            (self.width // 7 * 4, self.height // 7 + self.height // 27 * 3 + self.height // 70 * 4, 150, 30),
            None,
            None,
            "sound_volume",
            self.buttons_settings
        )

        self.BUTTON_PASSIVE_UPGRADES = RectangleButtons(
            (0, self.height - 75, self.width // 4, 75),
            pygame.transform.scale(pygame.image.load('assets/images/passive_button.jpeg'), (self.width // 4, 75)),
            pygame.transform.scale(pygame.image.load('assets/images/passive_pressed_button.jpeg'),
                                   (self.width // 4, 75)),
            "passive_upgrades", self.buttons_bottom
        )

        self.BUTTON_ACTIVE_UPGRADES = RectangleButtons(
            (self.width // 4, self.height - 75, self.width // 4, 75),
            pygame.transform.scale(pygame.image.load('assets/images/active_button.jpeg'), (self.width // 4, 75)),
            pygame.transform.scale(pygame.image.load('assets/images/active_pressed_button.jpeg'),
                                   (self.width // 4, 75)),
            "active_upgrades", self.buttons_bottom
        )

        self.BUTTON_SETTINGS = RectangleButtons(
            (self.width // 4 * 2, self.height - 75, self.width // 4, 75),
            pygame.transform.scale(pygame.image.load('assets/images/setting_button.jpeg'), (self.width // 4, 75)),
            pygame.transform.scale(pygame.image.load('assets/images/settings_pressed_button.jpeg'),
                                   (self.width // 4, 75)),
            "settings", self.buttons_bottom
        )

        self.BUTTON_LEADERBOARD = RectangleButtons(
            (self.width // 4 * 3, self.height - 75, self.width // 4, 75),
            pygame.transform.scale(pygame.image.load('assets/images/leaders_button.jpeg'), (self.width // 4, 75)),
            pygame.transform.scale(pygame.image.load('assets/images/leaders_pressed_button.jpeg'),
                                   (self.width // 4, 75)),
            "leaderboard", self.buttons_bottom
        )
        self.BUTTON_ALL_PASSIVE_UPGRADES = RectangleButtons(
            (self.width // 14 * 12, self.height // 7 + self.height // 70, self.width // 14,
             self.height // 70 * 7 + self.height // 27 * 7),
            None,
            None,
            "button_all_passive_upgrades", self.buttons_passive_upgrades
        )
        self.BUTTON_ALL_ACTIVE_UPGRADES = RectangleButtons(
            (self.width // 14 * 11, self.height // 7 + self.height // 70, self.width // 7,
             self.height // 7 + self.height // 27 * 4 + self.height // 70 * 5),
            None,
            None,
            "button_all_active_upgrades", self.buttons_active_upgrades
        )

        self.opened_windows = {
            "passive_upgrades": False,
            "active_upgrades": False,
            "settings": False,
            "leaderboard": False,
            "registration": False
        }

        self.passive_upgrades = {
            "general_multiply": (1, 100_000, 0.1, "умножалка", 100),
            "enrollee_course_1": (0, 50, 1, "обычный выпускник", 1.2),
            "enrollee_course_2": (0, 500, 5, "выпускник мат.лицея", 1.4),
            "enrollee_course_3": (0, 500_0, 10, "выпускник инт. МГУ", 1.1),
            "enrollee_course_4": (0, 500_00, 100, "ученик Кленина", 2.0),
            "enrollee_course_5": (0, 500_000, 1000, "t0urist", 2.0),
            "company": (0, 5_000_000, 10000, "азиат", 3.0)
        }

        self.active_upgrades = {
            "double_click": (1, 1_000, "две деньга", 2),
            "triple_click": (1, 10_000, "три деньга", 3),
            "quadro_click": (1, 50_000, "четыре деньга", 4)
        }

        self.settings = {
            "music_active": False,
            "music_volume": 0.5,
            "sound_active": True,
            "sound_volume": 0.5,
        }

        self.game_is_paused = False
        self.counter = 0
        self.running = True
        self.starting = True
        self.flag_one_click = True

    def start(self):
        while self.starting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.starting = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.starting = False
                        self.running = False

                    if event.key in range(48, 58):
                        self.name += str(self.num_to_digit(event.key))
                    if event.key in range(97, 123):
                        self.name += chr(event.key)
                    if event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    if event.key == pygame.K_SPACE:
                        self.name += " "
                    if event.key == pygame.K_KP_ENTER:
                        self.starting = False
                        pygame.mixer.music.load('assets/sounds/Checking_Manifest.mp3')
                        pygame.mixer.music.play(-1)
                        self.settings['music_active'] = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.starting = False
                    pygame.mixer.music.load('assets/sounds/Checking_Manifest.mp3')
                    pygame.mixer.music.play(-1)
                    self.settings['music_active'] = True

            self.screen.fill((0, 0, 0), (0, 0, self.width, self.height))
            self.screen.blit(self.fonts['settings_text_font'].render("ваше имя:", 1, (255, 255, 255))
                             , (self.width // 3, self.height // 2.24))
            self.screen.blit(self.fonts['settings_text_font'].render(self.name, 1, (255, 255, 255))
                             , (self.width // 4, self.height // 2))
            self.screen.blit(
                self.fonts['settings_text_font'].render("кликните на мышь для продолжения", 1, (255, 255, 255))
                , (self.width // 10, self.height // 1.5))
            pygame.display.update()
        self.run()

    def num_to_digit(self, num):
        return num - 48

    def run(self):
        while self.running:
            self.clock.tick(60)
            if not self.settings['music_active']:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()

            pygame.mixer.music.set_volume(self.settings['music_volume'])

            self.screen.blit(self.bg_image, (0, 0))
            # pygame.draw.circle(self.screen, 'purple', (self.width // 2, self.height // 2 + 175), 175, 3)
            self.screen.blit(self.click_image, (self.width // 10, self.height // 3 + self.height // 400 * 30))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.base.append([self.name, self.counter])
                    self.base.sort(key=lambda x: -x[1])
                    self.base = self.base[:6]
                    with open("base.txt", "w") as f:
                        for i in self.base:
                            f.write(f'{i[0]} {int(i[1])}\n')
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.base.append([self.name, self.counter])
                        self.base.sort(key=lambda x: -x[1])
                        self.base = self.base[:6]
                        with open("base.txt", "w") as f:
                            for i in self.base:
                                f.write(f'{i[0]} {int(i[1])}\n')
                        self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button in (1, 2, 3):
                        mouse_x, mouse_y = event.pos
                        if not self.game_is_paused:
                            if (mouse_x - self.width // 2) ** 2 + (mouse_y - (self.height // 2 + 175)) ** 2 <= 175 ** 2:
                                click_income = 1
                                for i in list(self.active_upgrades):
                                    click_income *= self.active_upgrades[i][0]
                                self.counter += click_income
                            for j in self.buttons_bottom:
                                if sum(self.opened_windows.values()) == 0:
                                    if j.is_clicked(mouse_x, mouse_y):
                                        self.game_is_paused = True
                                        self.opened_windows[str(j)] = True
                                        j.set_clicked_image()
                        else:
                            for j in self.buttons_bottom:
                                if self.opened_windows[str(j)] and j.is_clicked(mouse_x, mouse_y):
                                    self.game_is_paused = False
                                    self.opened_windows[str(j)] = False
                                    self.flag_one_click = False
                                    j.set_clicked_image()

                        if self.opened_windows["settings"]:
                            self.window = "settings"
                            for j in self.buttons_settings:
                                if j.is_clicked(mouse_x, mouse_y):
                                    if type(self.settings[str(j)]) == bool:
                                        self.settings[str(j)] = not self.settings[str(j)]
                                    else:
                                        if mouse_x > (j.rect.x * 2 + j.rect.width) // 2:
                                            self.settings[str(j)] += 0.1
                                        else:
                                            self.settings[str(j)] -= 0.1
                                        self.settings[str(j)] = min(round(self.settings[str(j)], 1), 1.0)
                                        self.settings[str(j)] = max(self.settings[str(j)], 0.0)
                        elif self.opened_windows["passive_upgrades"]:
                            self.window = "passive_upgrades"
                            if list(self.buttons_passive_upgrades)[0].is_clicked(mouse_x, mouse_y):
                                check_y = mouse_y - self.height * 11 // 70
                                for i in range(1, 8):
                                    if check_y < self.height // 70 * i + self.height // 27 * i:
                                        tup = self.passive_upgrades[list(self.passive_upgrades)[i - 1]]
                                        if self.counter >= tup[1]:
                                            self.counter -= tup[1]
                                            tup = (tup[0] + 1, int(tup[1] * tup[4]), tup[2], tup[3], tup[4])
                                            self.passive_upgrades[list(self.passive_upgrades)[i - 1]] = tup
                                        break
                        elif self.opened_windows["active_upgrades"]:
                            self.window = "active_upgrades"
                            if list(self.buttons_active_upgrades)[0].is_clicked(mouse_x, mouse_y):
                                check_y = mouse_y - self.height * 11 // 70
                                for i in range(1, 4):
                                    if check_y < self.height // 70 * i + self.height // 27 * i:
                                        tup = self.active_upgrades[list(self.active_upgrades)[i - 1]]
                                        if self.counter >= tup[1]:
                                            if tup[0] == 1:
                                                self.counter -= tup[1]
                                                tup = (tup[3], tup[1], tup[2], tup[3])
                                                self.active_upgrades[list(self.active_upgrades)[i - 1]] = tup
                                        break
                        elif self.opened_windows["leaderboard"]:
                            self.window = "leaderboard"

            if sum(self.opened_windows.values()) == 1:

                if self.window == 'settings':
                    for i in range(len(self.settings)):
                        key = list(self.settings)[i]
                        if type(self.settings[key]) != bool:
                            text_window_settings = self.fonts['settings_text_font'].render(
                                f'{key}:{self.settings[key]}', 1, (255, 255, 255))
                            self.screen.blit(text_window_settings, (
                                self.width // 7,
                                self.height // 7 + self.height // 27 * (i) + self.height // 70 * (i + 1)))

                            self.screen.blit(self.fonts["settings_plus_minus_font"].render(' -   + ', 1,
                                                                                           (255, 255, 255)),
                                             (self.width // 7 * 4,
                                              self.height // 7 + self.height // 27 * i + self.height // 70 * (i + 1)))
                        else:
                            text_window_settings = self.fonts['settings_text_font'].render(
                                f'{key}:{" " * 7 + "вкл." if self.settings[key] else " " * 7 + "выкл."}', 1,
                                (255, 255, 255))
                            self.screen.blit(text_window_settings, (
                                self.width // 7,
                                self.height // 7 + self.height // 27 * i + self.height // 70 * (i + 1)))
                elif self.window == "passive_upgrades":
                    for i in range(len(self.passive_upgrades)):
                        key = list(self.passive_upgrades)[i]
                        tuple_of_upgrades = self.passive_upgrades[key]
                        text_window_passive_upgrades = self.fonts['settings_text_font'].render(
                            f'{tuple_of_upgrades[3]} X{tuple_of_upgrades[0]} {tuple_of_upgrades[1]}',
                            1, (255, 102, 0)
                        )
                        self.screen.blit(text_window_passive_upgrades, (self.width // 14,
                                                                        self.height // 7 + self.height // 27 * i +
                                                                        self.height // 70 * (i + 1)))
                        plus_window_passive_upgrade = self.fonts['settings_text_font'].render(
                            '+', 1, (255, 102, 0))

                        self.screen.blit(plus_window_passive_upgrade, (self.width // 14 * 12,
                                                                       self.height // 7 + self.height // 27 * i +
                                                                       self.height // 70 * (i + 1)))
                elif self.window == "active_upgrades":
                    for i in range(len(self.active_upgrades)):
                        key = list(self.active_upgrades)[i]
                        tuple_of_upgrades = self.active_upgrades[key]
                        text_window_active_upgrades = self.fonts['settings_text_font'].render(
                            f"{tuple_of_upgrades[2]} {tuple_of_upgrades[1]} {' ' if tuple_of_upgrades[0] == 1 else 'pur.'}", 1, (255, 102, 0)
                        )
                        self.screen.blit(text_window_active_upgrades, (self.width // 8,
                                                                       self.height // 7 + self.height // 27 * i +
                                                                       self.height // 70 * (i + 1)))
                        plus_window_active_upgrade = self.fonts['settings_text_font'].render(
                            '+', 1, (255, 102, 0))

                        self.screen.blit(plus_window_active_upgrade, (self.width // 14 * 11,
                                                                      self.height // 7 + self.height // 27 * i +
                                                                      self.height // 70 * (i + 1)))
                elif self.window == "leaderboard":
                    for i in range(len(self.base)):
                        name = self.base[i][0]
                        score = self.base[i][1]
                        text_window_leaderboard = self.fonts['settings_text_font'].render(
                            f"{name}: {score}", 1, (255, 102, 0)
                        )
                        self.screen.blit(text_window_leaderboard, (self.width // 14,
                                                                   self.height // 7 + self.height // 27 * i +
                                                                   self.height // 70 * (i + 1)))

            self.flag_one_click = True
            self.buttons_bottom.draw(self.screen)
            self.buttons_bottom.update()
            text_counter = self.fonts["usual_text_font"].render(
                f'деняк:{int(self.counter) if self.counter < 1_000_000 else str(int(self.counter) // 1_000) + "K" if self.counter < 10_000_000 else str(int(self.counter) // 1_000_000) + "M."}'
                f'{"(мала)" if self.counter < 1_000_000 else "(многа)" if self.counter > 10_000_000 else "(средне)"}',
                1, (255, 255, 255))

            passive_income = 0

            # self.counter += 100_000
            for i in list(self.passive_upgrades)[1:]:
                cnt, price, income, name, mp = self.passive_upgrades[i]
                passive_income += (cnt * income)
            self.counter += float(passive_income * self.passive_upgrades['general_multiply'][0]) / 60.0
            text_passive_counter = self.fonts["settings_text_font"].render(
                f'{int(float(passive_income * self.passive_upgrades["general_multiply"][0]))} деньга в секунда', 1, (255, 255, 255)
            )
            self.screen.blit(text_passive_counter, (30, self.height // 10))
            self.screen.blit(text_counter, (30, 30))
            pygame.display.update()


root = Game()
root.start()

print(root.settings)
pygame.quit()
