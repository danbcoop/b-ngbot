import time

import keyboard
import win32gui


DELAY = 0.02


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
            window_handle = hwnd
            break
    if not window_handle:
        raise WindowFocusError(
            f"Es konnte kein Fenster mit dem Namen {
                window_name} gefunden werden!"
        )
    else:
        win32gui.SetForegroundWindow(window_handle)


def type_code(code: str):
    time.sleep(DELAY)
    keyboard.write(code)
    time.sleep(DELAY)
    keyboard.write("J")
    time.sleep(DELAY)
    keyboard.write("c")


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
