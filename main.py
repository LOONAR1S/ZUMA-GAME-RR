from game.Path import Path
from game.Sprites import *
from game.BallGenerator import BallGenerator
from game.ShootingManager import ShootingManager
from game.BonusManager import BonusManager
from game.ScoreManager import ScoreManager
from game.ui import *


class Level:
    def __init__(self, number, score_manager):
        self.number = number
        self.path = Path(number)
        self.ball_generator = BallGenerator(self.path, number * 20, score_manager)
        self.bonus_manager = BonusManager(self.ball_generator)
        self.player = Player(number)
        self.finish = Finish(self.path, self.ball_generator.balls, score_manager)
        self.shooting_manager = ShootingManager(self.ball_generator, self.player.pos, self.bonus_manager, score_manager)

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Zuma")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.level_num = 1
        self.score_manager = ScoreManager()
        self.setup_new_game()
        self.is_quit = False
        self.is_paused = False  # Состояние паузы

    def play(self):
        self.continue_game(self.ui_manager.start_game_btn, self.ui_manager.start_game_display)
        while not self.is_quit:
            self.setup_new_game()
            self.play_game()

        pygame.quit()

    def setup_new_game(self):
        self.level = Level(self.level_num, self.score_manager)
        self.ui_manager = UiManager(self.screen, self.level)

    def draw_pause_message(self):
        if self.is_paused:
            pause_label = Label("PAUSED", (WIDTH // 2, HEIGHT // 2), color=WHITE)
            self.ui_manager.put_label(pause_label)

    def play_game(self):
        game_finished = False

        while not game_finished and not self.is_quit:
            if not self.is_paused:  # Обновлять игру только если не в состоянии паузы
                self.level.ball_generator.generate()
                self.clock.tick(FPS)
                self.update_sprites()

            self.update_display(self.ui_manager.game_display)  # Обновить интерфейс игры
            self.draw_pause_message()  # Показать сообщение о паузе, если необходимо

            if not self.is_paused:  # Проверять состояние выигрыша/проигрыша только если не на паузе
                if self.score_manager.is_win:
                    game_finished = True
                    self.handle_win()
                elif self.score_manager.is_lose:
                    game_finished = True
                    self.handle_lose()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_quit = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Обработка кнопки паузы
                    if self.ui_manager.is_pause_clicked(mouse_pos):
                        self.is_paused = not self.is_paused  # Переключение состояния паузы
                    elif not self.is_paused:  # Стрелять только если не на паузе
                        self.level.shooting_manager.shoot(mouse_pos)

    def handle_win(self):
        if self.level_num == 3:
            self.win_game()
        else:
            self.continue_game(self.ui_manager.continue_btn, self.ui_manager.win_level_display)
            self.level_num += 1
            self.score_manager.setup_next_level()

    def handle_lose(self):
        """
        Метод обработки, когда игрок проигрывает игру:

        Уменьшить количество жизней игрока.
        Показать соответствующий интерфейс (проигрыш игры или проигрыш уровня).
        Если у игрока закончились жизни, перезапустить игру с начала.
        Если у игрока еще есть жизни, разрешить начать уровень заново.
        Переменные:
        self.score_manager: Управление счетом и жизнями игрока.
        self.ui_manager: Управление интерфейсом отображения.
        self.level_num: Переменная, хранящая текущий уровень игры.
        """
        # 1. Уменьшить количество жизней игрока при проигрыше
        self.score_manager.take_live()

        # 2. Проверить, если у игрока закончились жизни (полный проигрыш игры)
        if self.score_manager.lose_game:  
            # Показать интерфейс полного проигрыша игры
            self.continue_game(self.ui_manager.new_game_button, self.ui_manager.lose_game_display)
            
            # Перезапустить игру: 
            # - Уровень вернется к 1.
            # - Инициализировать ScoreManager заново, чтобы сбросить счет и жизни.
            self.level_num = 1
            self.score_manager = ScoreManager()

        # 3. У игрока еще есть жизни, разрешить начать текущий уровень заново
        else:
            # Показать интерфейс проигрыша текущего уровня и разрешить игроку начать уровень заново
            self.continue_game(self.ui_manager.start_level_again_btn, self.ui_manager.lose_level_display)
            
            # Сбросить состояние для следующего уровня
            self.score_manager.setup_next_level()

    def continue_game(self, button, window):
        """
        Этот метод помогает приостановить игру на конкретном экране
        (например: экран победы, проигрыша или начала) и продолжить только когда игрок
        нажмет на определенную кнопку.

        Аргументы:
            button: Кнопка, которую игрок должен нажать, чтобы продолжить игру.
            window: Текущий интерфейс экрана (отображает кнопку и другие элементы).

        Переменные:
            game_continued: Флаг, указывающий, нажал ли игрок кнопку, чтобы продолжить.
            mouse: Текущая позиция курсора мыши.
        """
        game_continued = False  # Инициализировать флаг, указывающий, что игра еще не продолжена

        while not game_continued and not self.is_quit:  # Цикл ожидания, пока игрок не нажмет кнопку
            mouse = pygame.mouse.get_pos()  # Получить текущую позицию мыши
            
            for event in pygame.event.get():  # Перебор событий в очереди событий
                if event.type == pygame.QUIT:  # Проверка, хочет ли игрок выйти из игры
                    self.is_quit = True  # Установить флаг выхода в True
                elif event.type == pygame.MOUSEBUTTONDOWN:  # Проверка, было ли нажатие мыши
                    if button.rect.collidepoint(mouse):  # Проверка, нажата ли указанная кнопка
                        game_continued = True  # Обновить флаг, указывающий на выход из цикла

            # Обновить экран интерфейса паузы (экран победы, проигрыша или начала)
            self.update_display(window)

    def win_game(self):
        on_win_window = True
        while on_win_window and not self.is_quit:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_quit = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.ui_manager.start_game_again_btn.rect.collidepoint(mouse):
                        on_win_window = False
                        self.level_num = 1
                    elif self.ui_manager.finish_btn.rect.collidepoint(mouse):
                        self.is_quit = True

            self.update_display(self.ui_manager.win_game_display)

    def update_sprites(self):
        self.level.player.update()
        self.level.shooting_manager.update()
        self.level.ball_generator.update()
        self.level.bonus_manager.update()
        self.level.finish.update()

    def update_display(self, display):
        self.ui_manager.draw_window(display)
        if display is self.ui_manager.game_display:
            self.ui_manager.show_score(self.score_manager.score)
            self.ui_manager.show_lives(self.score_manager.lives)
        pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.play()