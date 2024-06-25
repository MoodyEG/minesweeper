""" Minesweeper game code """
from tkinter import *
from random import randint


class Minesweeper:
    """ Our game class """

    def __init__(self, tk):
        """ Initialize the game """

        # Create the frame
        self.tk = tk
        self.frame = Frame(self.tk)
        self.frame.pack()

        # Create time, mines,flags here later

        # Setup iamges
        self.images = {
            "tile": PhotoImage(file="images/unclicked_tile.png"),
            "mine": PhotoImage(file="images/unclicked_mine_tile.png"),
            "flag": PhotoImage(file="images/flag_tile.png"),
            "clicked_mine": PhotoImage(file="images/clicked_mine_tile.png"),
            "wrong_flag": PhotoImage(file="images/wrong_flag_tile.png"),
            "numbers": []
        }
        for i in range(0, 9):
            self.images["numbers"].append(
                PhotoImage(file="images/num{}_tile.png".format(str(i))))

        # Setup size & mines
        self.size = 10
        # Limit the mines so it doesn't glitch
        self.selected_mines = min(self.size ** 2 - 9, 10)
        self.start()

    def start(self):
        """ Start the game """
        self.is_armed = False
        self.clicks = 0
        self.stop = False

        # Create the grid
        self.grid = {}
        for x in range(0, self.size):
            for y in range(0, self.size):
                if y == 0:
                    self.grid[x] = {}
                tile = {
                    "button": Button(self.frame,
                                     image=self.images["tile"]),
                    "is_mine": False,
                    "surrounding_mines": 0,
                    "is_flagged": False,
                    "is_clicked": False,
                    "first": False,
                    "x": x,
                    "y": y
                }
                tile["button"].bind("<Button-1>",
                                    lambda Button, x=x, y=y:
                                    self.left_click(x, y))
                tile["button"].bind("<Button-3>",
                                    lambda Button, x=x, y=y:
                                    self.right_click(x, y))
                tile["button"].grid(row=x, column=y)
                self.tk.bind("r", lambda Res: self.restart())
                self.grid[x][y] = tile

    def restart(self):
        """ Restart the game """
        try:
            self.game_over_window.destroy()
        except Exception:
            pass
        self.start()

    def create_mine(self):
        """ Create mines """
        for x in self.grid:
            for y in self.grid[x]:
                # Check the place where the lpayer first click to avoid mines
                if self.grid[x][y]["first"] is True:
                    continue

                # If the mine already exists, continue
                if self.grid[x][y]["is_mine"] is True:
                    continue

                # Distributes the mines with max efficiency
                if randint(0, (self.size ** 2 + 1) //
                           (self.selected_mines) + 1) == 0:
                    self.grid[x][y]["is_mine"] = True
                    # self.grid[x][y]["button"].config(
                    # image=self.images["mine"])
                    self.mines += 1

                # If the amount of mines is met, return
                if self.mines == self.selected_mines:
                    return

    def check_mines(self):
        """ Check surrounding mines """
        for x in self.grid:
            for y in self.grid[x]:

                # If it was mine continue
                if self.grid[x][y]["is_mine"] is True:
                    continue

                # Check surrounding mines
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        # if out of boundries top and side
                        if x + i < 0 or y + j < 0:
                            continue

                        # if out of boundries bot and side
                        if x + i > self.size - 1 or y + j > self.size - 1:
                            continue

                        if self.grid[x + i][y + j]["is_mine"] is True:
                            self.grid[x][y]["surrounding_mines"] += 1
                # self.grid[x][y]["button"].config(
                    # image=self.images["numbers"]
                    # [self.grid[x][y]["surrounding_mines"]])

    def left_click(self, x, y):
        """ Left click """
        if self.stop:
            return
        if self.is_armed is False:
            # Create mines in the grid
            self.mines = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    # if out of boundries top and side
                    if x + i < 0 or y + j < 0:
                        continue

                    # if out of boundries bot and side
                    if x + i > self.size - 1 or y + j > self.size - 1:
                        continue

                    self.grid[x + i][y + j]["first"] = True
            while True:
                # forever loop until the number is met
                self.create_mine()
                if self.mines == self.selected_mines:
                    break
            self.is_armed = True

            # Check surrounding mines
            self.check_mines()

        if self.grid[x][y]["is_flagged"] is True:
            return

        if self.grid[x][y]["is_clicked"] is True:
            return

        elif self.grid[x][y]["is_mine"] is True:
            self.grid[x][y]["button"].config(
                image=self.images["clicked_mine"])
            self.grid[x][y]["is_clicked"] = True
            self.game_over(False)

        elif self.grid[x][y]["surrounding_mines"] == 0:
            self.grid[x][y]["button"].config(
                image=self.images["numbers"][0])
            self.grid[x][y]["is_clicked"] = True
            self.clicks += 1
            if self.clicks == (self.size ** 2 - self.mines):
                self.game_over(True)
            self.clear_surr(x, y)

        else:
            self.grid[x][y]["button"].config(
                image=self.images["numbers"]
                [self.grid[x][y]["surrounding_mines"]])
            self.grid[x][y]["is_clicked"] = True
            self.clicks += 1
            if self.clicks == (self.size ** 2 - self.mines):
                self.game_over(True)

    def clear_surr(self, x, y):
        """ Clear surrounding tiles """
        for i in range(-1, 2):
            for j in range(-1, 2):
                # if out of boundries top and side
                if x + i < 0 or y + j < 0:
                    continue

                # if out of boundries bot and side
                if x + i > self.size - 1 or y + j > self.size - 1:
                    continue

                # if self.grid[x + i][y + j]["surrounding_mines"] == 0:
                self.left_click(x + i, y + j)

    def right_click(self, x, y):
        """ Right click """
        if self.stop:
            return
        if self.grid[x][y]["is_clicked"] is True:
            return

        if self.grid[x][y]["is_flagged"] is False:
            self.grid[x][y]["button"].config(image=self.images["flag"])
            self.grid[x][y]["is_flagged"] = True

        else:
            self.grid[x][y]["button"].config(image=self.images["tile"])
            self.grid[x][y]["is_flagged"] = False

    def game_over(self, result):
        """ Game over """
        self.stop = True
        for x in self.grid:
            for y in self.grid[x]:

                # Show unflagged mines
                if self.grid[x][y]["is_mine"] is True\
                        and self.grid[x][y]["is_clicked"] is False:
                    if self.grid[x][y]["is_flagged"] is False:
                        self.grid[x][y]["button"].config(
                            image=self.images["mine"])

                # Show wrong flags
                if self.grid[x][y]["is_flagged"] is True:
                    if self.grid[x][y]["is_mine"] is False:
                        self.grid[x][y]["button"].config(
                            image=self.images["wrong_flag"])

        if result is True:
            title = "Game Over, You Win!"
        else:
            title = "Game Over, You Lose!"
        # Create a new window for the game over message
        self.game_over_window = Toplevel(self.tk)
        self.game_over_window.title("Game Over")

        # Create a label with the game over message
        message_label = Label(self.game_over_window, text=title)
        message_label.pack()

        # Create a frame for the buttons
        button_frame = Frame(self.game_over_window)
        button_frame.pack()

        # Create a button to restart the game
        restart_button = Button(button_frame,
                                text="Restart", command=self.restart)
        self.game_over_window.bind("r", lambda Res: self.restart())
        restart_button.pack(side=LEFT)

        # Create a button to quit the game
        quit_button = Button(button_frame,
                             text="Quit", command=self.tk.destroy)
        quit_button.pack(side=RIGHT)

        # Set the focus to the game over window
        self.game_over_window.focus_set()

    def reload(self):
        """ Reload the same game """
        pass


if __name__ == "__main__":
    window = Tk()
    window.title("Minesweeper")
    game = Minesweeper(window)
    window.mainloop()
