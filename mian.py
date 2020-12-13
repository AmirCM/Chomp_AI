from gui import *
from utils import *
from tkinter import *
from PIL import Image
from PIL import ImageTk

panelA = None
game_board = Field()


def show_image(image):
    global panelA
    # image = cv2.resize(image, (480, 400))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    # if the panels are None, initialize them
    if panelA is None:
        panelA = Label(image=image)
        panelA.image = image
        panelA.pack(side="left", padx=10, pady=10)
    else:
        panelA.configure(image=image)
        panelA.image = image
    print('img updated')


def BFS():
    global game_board
    st_point = input('Insert start position separated by comma: ')
    end_point = input('Insert start position separated by comma: ')

    start = {'row': int(st_point.split(',')[1]), 'column': int(st_point.split(',')[0])}
    game_board.change_cube((start['column'], start['row']))
    show_image(game_board.get_img())
    cv2.waitKey(500)
    end = {'row': int(end_point.split(',')[1]), 'column': int(end_point.split(',')[0])}
    game_board.change_cube((end['column'], end['row']), color=(int("0xFF", 0), int("0x00", 0), int("0x00", 0)))
    show_image(game_board.get_img())

    result = breadth_first_search(maze.board, start, end)
    print(result)
    if result['result'] is True:
        for pixel in result['solution']:
            print(pixel)
            game_board.change_cube((pixel['column'], pixel['row']))
            show_image(game_board.get_img())
            cv2.waitKey(300)


def board_show():
    show_image(game_board.get_img())
    pass


if __name__ == "__main__":
    maze = Maze(10, 10)

    game_board.draw_cubes(maze.board)
    maze.print_board()
    root = Tk()
    btn = Button(root, text="START SEARCH", command=BFS)
    btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

    btn = Button(root, text="SHOW BOARD", command=board_show)
    btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

    root.mainloop()
