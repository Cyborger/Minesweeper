import pygame
import random


class Cell:
    SIZE = 32

    def __init__(self, x, y):
        self.covered_image = pygame.image.load("res/covered.png").convert_alpha()
        self.flagged_image = pygame.image.load("res/flagged.png").convert_alpha()
        self.image = self.covered_image.copy()
        self.rect = self.image.get_rect(x=x, y=y)
        self.covered = True
        self.flagged = False

    def uncover(self):
        raise NotImplementedError

    def mouse_is_hovering(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def invert_flag(self):
        self.flagged = not self.flagged
        if self.flagged:
            self.image = self.flagged_image.copy()
        else:
            self.image = self.covered_image.copy()


class NormalCell(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.mine_neighbors = 0

    def increment_mine_neighbors(self):
        self.mine_neighbors += 1

    def uncover(self):
        if self.mine_neighbors > 0:
            self.image = pygame.image.load("res/" + str(self.mine_neighbors) + ".png").convert_alpha()
        else:
            self.image = pygame.image.load("res/uncovered.png").convert_alpha()
        self.covered = False

    def neighbors_mine(self):
        return self.mine_neighbors > 0


class MineCell(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)

    def uncover(self):
        self.image = pygame.image.load("res/mine.png").convert_alpha()
        self.covered = False


class Board:
    CELLS_WIDE = 10
    CELLS_HIGH = 10
    NUMBER_OF_MINES = 10
    MINE_EXPLODED = pygame.USEREVENT + 1
    GAME_WON = pygame.USEREVENT + 2

    def __init__(self):
        self.cells = []
        self.create_cells()
        self.create_mines()

    def create_cells(self):
        for y in range(self.CELLS_HIGH):
            row = []
            for x in range(self.CELLS_WIDE):
                row.append(NormalCell(x * Cell.SIZE, y * Cell.SIZE))
            self.cells.append(row)

    def create_mines(self):
        mines_placed = 0
        while mines_placed < self.NUMBER_OF_MINES:
            x = random.randint(0, self.CELLS_WIDE - 1)
            y = random.randint(0, self.CELLS_HIGH - 1)
            if isinstance(self.cells[y][x], NormalCell):
                self.cells[y][x] = MineCell(x * Cell.SIZE, y * Cell.SIZE)
                mines_placed += 1
                neighbors = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1),
                             (x, y + 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]
                for position in neighbors:
                    self.increment_cell(position[0], position[1])

    def increment_cell(self, x, y):
        if 0 <= x < self.CELLS_WIDE and 0 <= y < self.CELLS_HIGH:
            if isinstance(self.cells[y][x], NormalCell):
                self.cells[y][x].increment_mine_neighbors()

    def left_clicked(self):
        for y in range(len(self.cells)):
            for x in range(len(self.cells[y])):
                if (self.cells[y][x].mouse_is_hovering() and self.cells[y][x].covered and
                    not self.cells[y][x].flagged):
                    self.uncover_cell(x, y)

    def right_clicked(self):
        for row in self.cells:
            for cell in row:
                if cell.mouse_is_hovering() and cell.covered:
                    cell.invert_flag()

    def uncover_cell(self, x, y):
        if x < 0 or x >= self.CELLS_WIDE or y < 0 or y >= self.CELLS_HIGH or not self.cells[y][x].covered:
            return
        self.cells[y][x].uncover()
        if isinstance(self.cells[y][x], MineCell):
            pygame.event.post(pygame.event.Event(self.MINE_EXPLODED))
        elif self.game_won():
            pygame.event.post(pygame.event.Event(self.GAME_WON))
        elif not self.cells[y][x].neighbors_mine():
            self.uncover_cell(x - 1, y)
            self.uncover_cell(x - 1, y - 1)
            self.uncover_cell(x - 1, y + 1)
            self.uncover_cell(x + 1, y)
            self.uncover_cell(x + 1, y - 1)
            self.uncover_cell(x + 1, y + 1)
            self.uncover_cell(x, y - 1)
            self.uncover_cell(x, y + 1)

    def draw(self, screen):
        for row in self.cells:
            for cell in row:
                screen.blit(cell.image, cell. rect)

    def game_won(self):
        cells_uncovered = 0
        for row in self.cells:
            for cell in row:
                if not cell.covered:
                    cells_uncovered += 1
        return cells_uncovered == self.CELLS_WIDE * self.CELLS_HIGH - self.NUMBER_OF_MINES


class Game:
    RESET_BOARD = pygame.USEREVENT + 3
    RESET_TIME = 1000

    def __init__(self):
        self.screen = pygame.display.set_mode((Board.CELLS_WIDE * Cell.SIZE,
                                               Board.CELLS_HIGH * Cell.SIZE))
        pygame.display.set_caption("Minesweeper")
        pygame.display.set_icon(pygame.image.load("res/mine.png").convert_alpha())
        self.board = Board()
        self.game_over = False

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    if event.button == 1:
                        self.board.left_clicked()
                    elif event.button == 3:
                        self.board.right_clicked()
                elif event.type == Board.MINE_EXPLODED:
                    pygame.time.set_timer(self.RESET_BOARD, self.RESET_TIME)
                    self.game_over = True
                elif event.type == Board.GAME_WON:
                    print("Game won")
                    pygame.time.set_timer(self.RESET_BOARD, self.RESET_TIME)
                    self.game_over = True
                elif event.type == self.RESET_BOARD:
                    self.board = Board()
                    self.game_over = False
                    pygame.time.set_timer(self.RESET_BOARD, 0)

            self.screen.fill((0, 0, 0))
            self.board.draw(self.screen)
            pygame.display.flip()


if __name__ == "__main__":
    Game().loop()
