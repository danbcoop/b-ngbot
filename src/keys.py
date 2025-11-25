import time

import keyboard
import win32gui

DELAY = 0.25
EINGABE = (500, 380)
CONFIRMJ = (565, 380)
CONFIRMC = (485, 380)


class WindowFocusError(LookupError):
    """Raise this, when the window you are looking for could not be found."""


def focus_window(window_name: str):
    toplist = []
    winlist = []

    def enum_callback(hwnd, _):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

    win32gui.EnumWindows(enum_callback, toplist)

    window_handle = 0
    for hwnd, title in winlist:
        if window_name in title.lower():
            print(title.lower())
            window_handle = hwnd
            break
    if not window_handle:
        raise WindowFocusError(
            f"Es konnte kein Fenster mit dem Namen {
                window_name} gefunden werden!"
        )
    else:
        x0, y0, x1, y1 = win32gui.GetWindowRect(window_handle)
        global EINGABE
        global CONFIRMJ
        EINGABE = (EINGABE[0] + x0, EINGABE[1] + y0)
        CONFIRMJ = (CONFIRMJ[0] + x0, CONFIRMJ[1] + y0)
        print(EINGABE)
        win32gui.SetForegroundWindow(window_handle)


def type_code(code: str):
    if check_pixel(*EINGABE):
        for letter in code:
            keyboard.press_and_release(letter)

    time.sleep(DELAY)
    if check_pixel(*CONFIRMJ):
        keyboard.press_and_release("J")
        keyboard.press_and_release("c")
    else:
        for i in range(9):
            keyboard.send("backspace")


def check_pixel(x, y):
    TARGET_COLOR = 11184810
    return (
        win32gui.GetPixel(win32gui.GetDC(win32gui.GetActiveWindow()), x, y)
        == TARGET_COLOR
    )


if __name__ == "__main__":
    try:
        focus_window("editor")
    except WindowFocusError as err:
        errortext = err.args[0]

    keyboard.write("code")
    time.sleep(DELAY)
    keyboard.write("J")
    time.sleep(DELAY)
    keyboard.write("c")
