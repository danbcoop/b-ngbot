import keyboard
import time
# pywin32
import win32gui

def focus_window(window_name: str):
    toplist = []
    winlist = []
    def enum_callback(hwnd, _):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))


    win32gui.EnumWindows(enum_callback, toplist)
    window = [(hwnd, title) for hwnd, title in winlist if window_name in title.lower()]
    # just grab the first window that matches
    window = window[0]
    # use the window handle to set focus
    win32gui.SetForegroundWindow(window[0])

if __name__ == '__main__':
    focus_window("editor")  
    DELAY  = 0.02
    keyboard.write("code")
    time.sleep(DELAY)
    keyboard.write('J')
    time.sleep(DELAY)
    keyboard.write('c')
    