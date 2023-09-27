import pygame
import math
import random
pygame.init()


class Window:
    ## colours to be used for the window
    black = 0, 0, 0
    white = 255, 255, 255
    green = 0, 255, 0
    red = 255, 0, 0
    background_colour = white

    list_colours = [(128, 128, 128), (160, 160, 160), (192, 192, 192)]

    text_font = pygame.font.Font('Assets/League.otf', 40)

    side_padding = 100 ## padding distance for the side of the window
    top_padding = 200 ## padding distance for the top of the screen

    def __init__(self, width, height, lst) -> None:
        ## sets up the window
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Sorting Visualiser')
        self.set_list(lst)

    def set_list(self, lst): ## list to be sorted
        self.lst = lst
        self.min = min(lst)
        self.max = max(lst)

        self.data_width = round((self.width - self.side_padding)) / len(lst) ## works out the pixel width for each bar of data
        self.data_height = math.floor((self.height - self.top_padding) / (self.max - self.min)) ## works out the max drawable area height for the bars
        self.start_x = self.side_padding // 2 ## works out x pos of the first bar


def main():
    running = True
    clock = pygame.time.Clock()

    ## values for the list
    list_n = 50
    list_min = 0
    list_max = 100
    lst = generate_list(list_n, list_min, list_max)
    window = Window(1280, 800, lst) ## instantiates window

    sorting = False
    ascending = False

    current_Sort = bubble_sort
    current_name = 'Bubble Sort'
    algo_generator = None

    while running:
        clock.tick(60) ## fps = 60

        if sorting:
            try:
                next(algo_generator)
            except StopIteration:
                sorting = False
        else:
            draw_window(window)

        draw_window(window)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: ## makes sure program can quit
                running = False
            
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r: ## if r key is pressed, reset list
                lst = generate_list(list_n, list_min, list_max)
                window.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False: ## if space key is pressed, start sorting
                sorting = True
                algo_generator = current_Sort(window, ascending)
            elif event.key == pygame.K_a and sorting == False:
                ascending = True
            elif event.key == pygame.K_d and sorting == False:
                ascending = False
                


def generate_list(n, min_value, max_value):
    starting_list = []

    for i in range(n):
        val = random.randint(min_value, max_value)
        starting_list.append(val)

    return starting_list


def draw_window(Window):
    Window.window.fill(Window.background_colour)

    control_text = Window.text_font.render('R - RESET | SPACE - Start | A - Ascending | D - Descending', 1, Window.black)
    Window.window.blit(control_text, (Window.width/2 - control_text.get_width()/2, 10))

    algorithm_text = Window.text_font.render('B - Bubble | I - Insertion | M - Merge | Q - Quick', 1, Window.black)
    Window.window.blit(algorithm_text, (Window.width/2 - algorithm_text.get_width()/2, 60))

    draw_list(Window)
    pygame.display.update()


def draw_list(Window, positions = {}, clear_background = False):
    lst = Window.lst

    if clear_background:
        area = (Window.side_padding//2, Window.top_padding, Window.width - Window.side_padding, Window.height - Window.top_padding)
        pygame.draw.rect(Window.window, Window.background_colour, area)

    for i, val in enumerate(lst): ## gives indix and val
        x = Window.start_x + i * Window.data_width
        y = Window.height - (val - Window.min) * Window.data_height

        colour = Window.list_colours[i % 3]

        if i in positions:
            colour = positions[i]

        pygame.draw.rect(Window.window, colour, (x, y, Window.data_width, Window.height))

    if clear_background:
        pygame.display.update()

def bubble_sort(wndw, ascending=True):
    lst = wndw.lst
    n = len(lst)

    for i in range(n):
        for j in range(0, n - i - 1):
            if (lst[j] > lst[j + 1] and ascending) or (lst[j] < lst[j + 1] and not ascending):
                # Swap the elements
                lst[j], lst[j + 1] = lst[j + 1], lst[j]

                # Visualize the swap and yeild
                draw_list(wndw, {j: wndw.green, j + 1: wndw.red}, True)
                yield True

    # Return the sorted list
    return lst


def insetion_sort(wndw, ascending=True):
    pass


def marge_sort(wndw, ascending=True):
    pass


def quick_sort(wndw, ascending=True):
    pass

if __name__ == '__main__':
    main()
