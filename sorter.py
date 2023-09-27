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
    background_colour = 32, 32, 32

    list_colours = [(255, 255, 255), (224, 224, 224), (192, 192, 192)]

    side_padding = 75 ## padding distance for the side of the window
    top_padding = 150 ## padding distance for the top of the screen

    def __init__(self, width, height, lst) -> None:
        ## sets up the window
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Sorting Visualiser')
        icon = pygame.image.load('Assets/Icon/icon.png')
        pygame.display.set_icon(icon)
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
    list_n = 250
    list_min = 0
    list_max = 100
    lst = generate_list(list_n, list_min, list_max)
    window = Window(1280, 800, lst) ## instantiates window

    sorting = False
    ascending = True

    current_Sort = bubble_sort
    algo_generator = None

    while running:
        clock.tick(60) ## fps = 60

        if sorting:
            try:
                next(algo_generator)
            except StopIteration:
                sorting = False
        else:
            draw_window(window, current_Sort, ascending)

        draw_window(window, current_Sort, ascending)
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
            elif event.key == pygame.K_s and sorting == False: ## if s key is pressed, start sorting
                sorting = True
                algo_generator = current_Sort(window, ascending)
            elif event.key == pygame.K_a and sorting == False:
                ascending = True
            elif event.key == pygame.K_d and sorting == False:
                ascending = False
            elif event.key == pygame.K_b and sorting == False:
                current_Sort = bubble_sort
            elif event.key == pygame.K_i and sorting == False:
                current_Sort = insertion_sort
            elif event.key == pygame.K_m and sorting == False:
                current_Sort = merge_sort
            elif event.key == pygame.K_q and sorting == False:
                current_Sort = quick_sort
                


def generate_list(n, min_value, max_value):
    starting_list = []

    for i in range(n):
        val = random.randint(min_value, max_value)
        starting_list.append(val)

    return starting_list


def draw_window(Window, current_sort, ascending):
    Window.window.fill(Window.background_colour)

    draw_gui(Window, current_sort, ascending)
    draw_list(Window)
    pygame.display.update()


def draw_gui(Window, sort, ascending = False):
    command_gui =  pygame.image.load('Assets/Gui/commands.png')

    if ascending:
        order_gui = pygame.image.load('Assets/Gui/ascending.png')
    elif not ascending:
        order_gui = pygame.image.load('Assets/Gui/descending.png')

    if sort == bubble_sort:
        sort_gui =  pygame.image.load('Assets/Gui/bubble.png')
    elif sort == insertion_sort:
        sort_gui =  pygame.image.load('Assets/Gui/insertion.png')
    elif sort == merge_sort:
        sort_gui =  pygame.image.load('Assets/Gui/merge.png')
    elif sort == quick_sort:
        sort_gui =  pygame.image.load('Assets/Gui/quick.png')

    Window.window.blit(command_gui, (0,0))
    Window.window.blit(order_gui, (0, 50))
    Window.window.blit(sort_gui, (0, 100))
    

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

                # Visualize the swap if required
                draw_list(wndw, {j: wndw.green, j + 1: wndw.red}, True)

                # Yield True if this step was performed
                yield True

    # Return the sorted list
    return lst



def insertion_sort(wndw, ascending=True):
    lst = wndw.lst
    n = len(lst)

    for i in range(1, n):
        key = lst[i]
        j = i - 1

        while j >= 0 and ((key < lst[j] and ascending) or (key > lst[j] and not ascending)):
            lst[j + 1] = lst[j]
            j -= 1

            # Visualize the swap if required
            draw_list(wndw, {j + 1: wndw.green, j: wndw.red}, True)

            # Yield True if this step was performed
            yield True

        lst[j + 1] = key

    # Return the sorted list
    return lst


def merge_sort(wndw, ascending=True):
    def merge(lst, left, right, low, mid, high):
        i = j = 0
        k = low

        while i < len(left) and j < len(right):
            if (left[i] <= right[j] and ascending) or (left[i] >= right[j] and not ascending):
                lst[k] = left[i]
                i += 1
            else:
                lst[k] = right[j]
                j += 1
            k += 1

            # Visualize the comparison step
            draw_list(wndw, {k - 1: wndw.red, i + low: wndw.green, j + mid + 1: wndw.green}, True)
            yield True

        while i < len(left):
            lst[k] = left[i]
            i += 1
            k += 1
            yield True

        while j < len(right):
            lst[k] = right[j]
            j += 1
            k += 1
            yield True

    def merge_sort_recursive(lst, low, high):
        if low < high:
            mid = (low + high) // 2

            yield from merge_sort_recursive(lst, low, mid)
            yield from merge_sort_recursive(lst, mid + 1, high)

            left = lst[low:mid + 1]
            right = lst[mid + 1:high + 1]

            yield from merge(lst, left, right, low, mid, high)

    lst = wndw.lst
    n = len(lst)
    yield from merge_sort_recursive(lst, 0, n - 1)

    # Return the sorted list
    return lst



def quick_sort(wndw, ascending=True):
    def partition(lst, low, high):
        pivot = lst[high]
        i = low - 1

        for j in range(low, high):
            if (lst[j] < pivot and ascending) or (lst[j] > pivot and not ascending):
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
                # Visualize the swap if required
                draw_list(wndw, {i: wndw.green, j: wndw.red}, True)
                yield True

        lst[i + 1], lst[high] = lst[high], lst[i + 1]
        # Visualize the swap if required
        draw_list(wndw, {i + 1: wndw.green, high: wndw.red}, True)
        yield True

        yield from quick_sort_recursive(lst, low, i)
        yield from quick_sort_recursive(lst, i + 2, high)

    def quick_sort_recursive(lst, low, high):
        if low < high:
            yield from partition(lst, low, high)

    lst = wndw.lst
    n = len(lst)
    yield from quick_sort_recursive(lst, 0, n - 1)

    # Return the sorted list
    return lst


if __name__ == '__main__':
    main()
