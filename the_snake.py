"""Игра змейка."""
from random import randint
from sys import exit

import pygame


# Константы для размеров
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

CENTRAL_POSITION_DELAULT = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
FRAME_SIZE_DEFAULT = 5

BOARD_BACKGROUND_COLOR = (200, 200, 200)
COLOR_DEFAULT = (123, 123, 123)
COLOR_FRAME_DEFAULT = (93, 216, 228)
APPLE_COLOR = (10, 110, 230)
SNAKE_COLOR = (255, 255, 255)

# Настройка игрового окна
SPEED = 2
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля
pygame.display.set_caption('Змейка')

# Настройка времени
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс."""

    def __init__(
        self, position=CENTRAL_POSITION_DELAULT,
        body_color=COLOR_DEFAULT,
        color_frame=COLOR_FRAME_DEFAULT,
        frame=FRAME_SIZE_DEFAULT
    ):
        """Инициализатор."""
        self.position = position
        self.body_color = body_color
        self.color_frame = color_frame
        self.frame = frame

    def draw(self, surface=None):
        """Отрисовка."""
        pass

    def draw_rect(self, position, color=True, surface=screen):
        """Отрисовка элемента."""
        color_obj = color_frame = BOARD_BACKGROUND_COLOR
        if color:
            color_obj = self.body_color
            color_frame = self.color_frame

        rect = pygame.Rect(
            (position[0], position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, color_obj, rect)
        pygame.draw.rect(surface, color_frame, rect, self.frame)


class Apple(GameObject):
    """Яблоко."""

    def __init__(
        self,
        position=CENTRAL_POSITION_DELAULT,
        body_color=COLOR_DEFAULT,
        color_frame=COLOR_FRAME_DEFAULT,
        frame=FRAME_SIZE_DEFAULT
    ) -> None:
        """Инициализатор."""
        super().__init__(body_color=body_color)
        self.randomize_position()

    def draw(self, surface=screen):
        """Отрисовка."""
        self.draw_rect(self.position)

    def randomize_position(self, positions=[CENTRAL_POSITION_DELAULT]):
        """Рандомная позиция."""
        while self.position in positions:
            self.position = [
                randint(0, GRID_SIZE - 1) * GRID_SIZE,
                randint(0, GRID_SIZE - 1) * GRID_SIZE
            ]


class Snake(GameObject):
    """Змея."""

    def __init__(self) -> None:
        """Инициализатор."""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновление направления."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Достать голову."""
        return self.positions[0]

    def move(self):
        """Движение на следующую клетку."""
        head_position = self.get_head_position()
        new_head_position = [
            (
                head_position[0] + self.direction[0] * GRID_SIZE
            ) % SCREEN_WIDTH,
            (
                head_position[1] + self.direction[1] * GRID_SIZE
            ) % SCREEN_HEIGHT
        ]
        self.positions.insert(0, new_head_position)

        if self.length < len(self.positions):
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self, surface=screen):
        """Отрисовка."""
        if self.last:
            self.draw_rect(self.last, False)
        self.draw_rect(self.get_head_position())

    def reset(self):
        """Сброс к началу."""
        self.length = 1
        self.positions = [CENTRAL_POSITION_DELAULT]
        self.direction = RIGHT
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(self):
    """События клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit('Выводим')
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != DOWN:
                self.next_direction = UP
            elif event.key == pygame.K_DOWN and self.direction != UP:
                self.next_direction = DOWN
            elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                self.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                self.next_direction = RIGHT


def main():
    """Функция управления."""
    # Тут нужно создать экземпляры классов
    pygame.init()
    screen.fill(BOARD_BACKGROUND_COLOR)
    apple = Apple()
    snake_obj = Snake()
    apple.draw()
    while True:
        clock.tick(SPEED)
        handle_keys(snake_obj)
        snake_obj.update_direction()
        snake_obj.move()
        if snake_obj.get_head_position() in snake_obj.positions[1:]:
            snake_obj.reset()
        if apple.position == snake_obj.get_head_position():
            apple.randomize_position(snake_obj.positions)
            snake_obj.length += 1
            apple.draw()
        snake_obj.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
