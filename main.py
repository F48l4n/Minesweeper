import math
import time
from random import randrange

import pygame as pygame


def generate_new_grid(_width, _height, mines):
    def generate_random_mine():
        x = randrange(_width - 1)
        y = randrange(_height - 1)
        if new_grid[y][x] == 0:
            new_grid[y][x] = 1
        else:
            generate_random_mine()

    new_grid = [[0 for j in range(_width)] for i in range(_height)]
    for i in range(mines):
        generate_random_mine()
    return new_grid


def new_player_grid(_width, _height):
    return [["#" for j in range(_width)] for i in range(_height)]


def reveal_cell(x, y, new_unrevealed_cells):
    bombs = neighbour_bombs(x, y, grid)
    if grid[y][x] == 1:
        show_death_screen()
        print("You Lost, Cell was a Mine")
        exit()
    elif not playerGrid[y][x] == "#":
        return new_unrevealed_cells
    elif bombs == 0:
        playerGrid[y][x] = "."
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if j in range(0, len(grid)) and i in range(0, len(grid[0])):
                    new_unrevealed_cells = reveal_cell(i, j, new_unrevealed_cells)
    else:
        playerGrid[y][x] = bombs
    new_unrevealed_cells -= 1
    return new_unrevealed_cells


def show_death_screen():
    screen.fill((200, 50, 50))
    losing_text = my_font.render("You Lost !!!", True, (255, 255, 255))
    losing_text2 = my_font.render("Cell was a Mine", True, (255, 255, 255))
    losing_rect = losing_text.get_rect(center=(width * 100 / 2, height * 100 / 2 - 90))
    losing_rect2 = losing_text2.get_rect(center=(width * 100 / 2, height * 100 / 2 + 90))

    screen.blit(losing_text, losing_rect)
    screen.blit(losing_text2, losing_rect2)
    pygame.display.flip()
    time.sleep(3)


def print_player_grid():
    for i in playerGrid:
        print(*i)


def print_grid():
    for i in grid:
        print(*i)
    bomb_grid = [[neighbour_bombs(j, i, grid) for j in range(len(grid[0]))] for i in range(len(grid))]
    for i in bomb_grid:
        print(*i)


def neighbour_bombs(x, y, _grid):
    bombs = 0
    for i in range(y - 1, y + 2):
        for j in range(x - 1, x + 2):
            if i in range(0, len(_grid)) and j in range(0, len(_grid[0])):
                bombs += _grid[i][j]
    bombs -= _grid[y][x]
    return bombs


def render(player_grid):
    for i in range(len(player_grid)):
        for j in range(len(player_grid[0])):
            cell = player_grid[i][j]
            if cell == "X":
                pygame.draw.rect(screen, pygame.Color(200, 50, 50), pygame.Rect(i * 50, j * 50, 45, 45))
            elif cell == "#":
                pygame.draw.rect(screen, pygame.Color(140, 200, 140), pygame.Rect(i * 50, j * 50, 45, 45))
            else:
                bombs = neighbour_bombs(j, i, grid)
                strength_list = [240, 200, 160, 130, 100, 80, 60, 40, 20]
                strength = strength_list[bombs]
                color = (strength, strength, strength)
                pygame.draw.rect(screen, color, pygame.Rect(i * 50, j * 50, 45, 45))
                # text_surface = my_font.render(str(bombs), False, (255, 255, 255))
                # screen.blit(text_surface, (i * 100, j * 100))


def mark_bomb(x, y):
    if playerGrid[y][x] == "#":
        playerGrid[y][x] = "X"
    elif playerGrid[y][x] == "X":
        playerGrid[y][x] = "#"


if __name__ == '__main__':
    height, width, bomb_count = 10, 10, 10

    un_revealed_cells = height * width
    grid = generate_new_grid(width, height, bomb_count)
    playerGrid = new_player_grid(width, height)

    running = True
    pygame.init()
    pygame.font.init()
    my_font = pygame.font.SysFont("Ariel", 180)
    pygame.display.set_caption("MineSweeper")
    screen = pygame.display.set_mode((width * 50, height * 50))
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                posY = math.trunc(pos[0] / 50)
                posX = math.trunc(pos[1] / 50)
                if event.button == 1:
                    un_revealed_cells = reveal_cell(posX, posY, un_revealed_cells)
                if event.button == 3:
                    mark_bomb(posX, posY)

        screen.fill((240, 240, 240))
        render(playerGrid)
        pygame.display.flip()
        if un_revealed_cells == bomb_count:
            screen.fill((50, 200, 50))
            winning_text = my_font.render("You Won !!!", True, (255, 255, 255))
            rect = winning_text.get_rect(center=(width * 100 / 2, height * 100 / 2))
            screen.blit(winning_text, rect)
            pygame.display.flip()
            time.sleep(3)
            print("You won !!!")
            exit()

        clock.tick(30)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
