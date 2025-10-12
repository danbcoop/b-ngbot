import tkinter as tk


class GUI:
    """A GUI to interface the bot"""

    def __init__(self):
        self.root = tk.Tk()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    GUI().run()
