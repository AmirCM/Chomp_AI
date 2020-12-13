from gui import *
from utils import *
from tkinter import *
from PIL import Image
from PIL import ImageTk

panelA = None


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


def BFS():
    start = {'row': 1, 'column': 1}
    end = {'row': 1, 'column': 5}
    game_board.change_cube((1, 1))
    show_image(game_board.get_img())
    cv2.waitKey(500)
    game_board.change_cube((1, 3))
    show_image(game_board.get_img())
    """result = breadth_first_search(maze.board, start, end)
    if result['result'] is True:
        for pixel in result['solution']:
            print(pixel)
            game_board.change_cube((pixel['column'], pixel['row']))
            show_image(game_board.get_img())
            cv2.waitKey(300)"""


if __name__ == "__main__":
    game_board = Field()
    maze = Maze(10, 10)
    game_board.draw_cubes(maze.board)

    root = Tk()
    btn = Button(root, text="BFS Search", command=BFS)
    btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
    root.mainloop()
