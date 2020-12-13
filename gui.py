import cv2
import numpy as np


class Field:
    def __init__(self):
        self.img = None
        self.box_size = 40
        self.width = 0
        self.height = 0
        self.line_color = (0, 255, 0)
        self.r_clicked = False
        self.x_clk = None
        self.y_clk = None
        self.cube_color = (int("0x17", 0), int("0xdd", 0), int("0x64", 0))
        self.background_color = (int("0x17", 0), int("0xDD", 0), int("0x64", 0))
        self.burnt_cube_color = (int("0x00", 0), int("0x00", 0), int("0x00", 0))
        self.path_cube_color = (int("0x00", 0), int("0x00", 0), int("0xFF", 0))
        self.poison_color = (int("0x00", 0), int("0x00", 0), int("0xcc", 0))
        self.text_color = (int("0x21", 0), int("0x21", 0), int("0x21", 0))

    def draw_cubes(self, board):
        self.width = len(board[0]) * self.box_size
        self.height = len(board) * self.box_size
        self.img = np.zeros((self.height, self.width, 3), np.uint8)
        cv2.rectangle(self.img, (0, 0), (self.width, self.height), self.background_color, -1)
        k = 0
        for i in range(0, self.width, self.box_size):
            z = 0
            for j in range(0, self.height, self.box_size):
                if board[z][k] == 0:
                    cv2.rectangle(self.img, (i + 4, j + 4), (i + self.box_size - 4, j + self.box_size - 4),
                                  self.cube_color,
                                  -1)
                else:
                    cv2.rectangle(self.img, (i + 4, j + 4), (i + self.box_size - 4, j + self.box_size - 4),
                                  self.burnt_cube_color,
                                  -1)
                z += 1
            k += 1

        cv2.line(self.img, (0, 0), (self.width, 0), (0, 255, 0), 2)
        cv2.line(self.img, (0, 0), (0, self.height), (0, 255, 0), 2)
        cv2.line(self.img, (self.width, self.height), (0, self.height), (0, 255, 0), 2)
        cv2.line(self.img, (self.width, self.height), (self.width, 0), (0, 255, 0), 2)
        print(f'H: {self.height} W: {self.width}')

    def write_result(self, text, offset):
        font = cv2.FONT_HERSHEY_PLAIN
        cv2.putText(self.img, text, (5, int(self.height / 2) + offset), font, 1,
                    self.text_color, 1, cv2.FONT_ITALIC)

    def get_img(self):
        return self.img

    def get_pos(self):
        return self.x_clk, self.y_clk

    def change_cube(self, pos, color=None):
        if color is None:
            color = self.path_cube_color

        cv2.rectangle(self.img, (pos[0] * self.box_size,
                                 pos[1] * self.box_size), ((pos[0] + 1) * self.box_size,
                                                           (pos[1] + 1) * self.box_size),
                      color, -1)

    def draw_path(self, result):
        for pixel in result:
            print(pixel)
            self.change_cube((pixel['column'], pixel['row']))
            cv2.imshow("AI Project", self.img)
            cv2.waitKey(300)

    def mouse_callback(self, e, x, y, flags, param):
        if e == cv2.EVENT_LBUTTONDOWN:
            cv2.rectangle(self.img, (int(x / self.box_size) * self.box_size,
                                     int(y / self.box_size) * self.box_size), (self.width - 2, self.height - 2),
                          self.burnt_cube_color, -1)
            self.r_clicked = True
            self.x_clk = int(x / self.box_size)
            self.y_clk = int(y / self.box_size)
