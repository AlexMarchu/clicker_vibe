import pygame


class RectangleButtons(pygame.sprite.Sprite):
    def __init__(self, data, image, name, group):
        super().__init__(group)
        self.rect = pygame.rect.Rect(*data)
        self.image = image
        self.__name = name
        self.flag_for_click = False

    def is_clicked(self, x, y) -> bool:
        return self.rect.collidepoint(x, y)

    def __repr__(self):
        return self.__name


class Game:

    def __init__(self):

        pygame.init()
        pygame.display.set_caption('Clicker')

        self.width = 600
        self.height = int(self.width * 1.4)
        self.bg_image = pygame.transform.scale(pygame.image.load('assets/images/background.jpeg'),
                                               (self.width, self.height))
        self.fonts = {
            "usual_text_font": pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 30),
            "settings_text_font": pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 15),
            "settings_plus_minus_font": pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 20),
        }

        self.screen = pygame.display.set_mode((self.width, self.height), pygame.SRCALPHA)
        self.buttons_bottom = pygame.sprite.Group()
        self.buttons_settings = pygame.sprite.Group()

        self.BUTTON_SETTINGS_MUSIC_ACTIVE = RectangleButtons(
            (self.width // 7 * 4 - 10, self.height // 7 + self.height // 70 - 10, 150, 30),
            None,
            "music_active",
            self.buttons_settings
        )

        self.BUTTON_SETTINGS_SOUND_ACTIVE = RectangleButtons(
            (self.width // 7 * 4, self.height // 7 + self.height // 27 * 2 + self.height // 70 * 3, 150, 30),
            None,
            "sound_active",
            self.buttons_settings
        )

        self.BUTTON_SETTINGS_MUSIC_VOLUME = RectangleButtons(
            (self.width // 7 * 4, self.height // 7 + self.height // 27 * 1 + self.height // 70 * 2, 150, 30),
            None,
            "music_volume",
            self.buttons_settings
        )

        self.BUTTON_SETTINGS_SOUND_VOLUME = RectangleButtons(
            (self.width // 7 * 4, self.height // 7 + self.height // 27 * 3 + self.height // 70 * 4, 150, 30),
            None,
            "sound_volume",
            self.buttons_settings
        )

        self.BUTTON_PASSIVE_UPGRADES = RectangleButtons(
            (0, self.height - 75, self.width // 4, 75),
            pygame.transform.scale(pygame.image.load('assets/images/passive_button.jpeg'), (self.width // 4, 75)),
            "passive_upgrades", self.buttons_bottom
        )

        self.BUTTON_ACTIVE_UPGRADES = RectangleButtons(
            (self.width // 4, self.height - 75, self.width // 4, 75),
            pygame.transform.scale(pygame.image.load('assets/images/active_button.jpeg'),
                                   (self.width // 4, 75)), "active_upgrades", self.buttons_bottom
        )

        self.BUTTON_SETTINGS = RectangleButtons(
            (self.width // 4 * 2, self.height - 75, self.width // 4, 75),
            pygame.transform.scale(pygame.image.load('assets/images/setting_button.jpeg'),
                                   (self.width // 4, 75)), "settings", self.buttons_bottom
        )

        self.BUTTON_LEADERBOARD = RectangleButtons(
            (self.width // 4 * 3, self.height - 75, self.width // 4, 75),
            pygame.transform.scale(pygame.image.load('assets/images/leaders_button.jpeg'),
                                   (self.width // 4, 75)), "leaderboard", self.buttons_bottom
        )

        self.opened_windows = {
            "passive_upgrades": False,
            "active_upgrades": False,
            "settings": False,
            "leaderboard": False
        }

        self.passive_upgrades = {
            "click_multiply": 1.0,
            "general_multiply": 1.0,
        }

        self.active_upgrades = {

        }

        self.settings = {
            "music_active": True,
            "music_volume": 0.5,
            "sound_active": True,
            "sound_volume": 0.5,
        }

        self.game_is_paused = False
        self.counter = 0.0
        self.running = True
        self.flag_one_click = True

    def run(self):

        while self.running:

            self.screen.blit(self.bg_image, (0, 0))
            pygame.draw.circle(self.screen, 'lightblue', (self.width // 2, self.height // 2 + 175), 175)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_x, mouse_y = event.pos
                        if not self.game_is_paused:
                            if (mouse_x - self.width // 2) ** 2 + (mouse_y - (self.height // 2 + 175)) ** 2 <= 175 ** 2:
                                print("[eq")
                                self.counter += 1
                        else:
                            for j in self.buttons_bottom:
                                if self.opened_windows[str(j)] and j.is_clicked(mouse_x, mouse_y):
                                    self.game_is_paused = False
                                    self.opened_windows[str(j)] = False
                                    self.flag_one_click = False
                        for j in self.buttons_bottom:
                            if sum(self.opened_windows.values()) == 0:
                                if j.is_clicked(mouse_x, mouse_y) and self.flag_one_click:
                                    print(j)
                                    self.game_is_paused = True
                                    self.opened_windows[str(j)] = True
                        if sum(self.opened_windows.values()) == 1:
                            for j in self.buttons_settings:
                                if j.is_clicked(mouse_x, mouse_y):
                                    print(j)
                                    if type(self.settings[str(j)]) == bool:
                                        self.settings[str(j)] = not self.settings[str(j)]
                                    else:
                                        print(mouse_x, (2 * j.rect.x + j.rect.width) // 2)
                                        if mouse_x > (j.rect.x * 2 + j.rect.width) // 2:
                                            self.settings[str(j)] += 0.1
                                        else:
                                            self.settings[str(j)] -= 0.1
                                        self.settings[str(j)] = min(round(self.settings[str(j)], 1), 1.0)
                                        self.settings[str(j)] = max(self.settings[str(j)], 0.0)

            if sum(self.opened_windows.values()) == 1:

                window = [i for i in self.opened_windows.keys() if self.opened_windows[i]][0]
                # pygame.draw.rect(self.screen, (0, 0, 0, 0),
                #                  (self.width // 7, self.height // 7, self.width // 7 * 5, self.height // 7 * 5))

                if window == 'settings':
                    for i in range(0, len(self.settings)):
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

            self.flag_one_click = True
            self.buttons_bottom.draw(self.screen)

            text_counter = self.fonts["usual_text_font"].render(
                f'деняк:{int(self.counter)}{"(мала)" if self.counter < 1_000_000 else "(многа)" if self.counter > 2_000_000 else "(средне)"}',
                1, (255, 255, 255))

            self.screen.blit(text_counter, (30, 30))
            pygame.display.update()


root = Game()
root.run()

pygame.quit()
