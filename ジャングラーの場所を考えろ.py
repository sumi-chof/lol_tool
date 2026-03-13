import tkinter as tk
import ctypes
import os
import sys
import signal

# Windows API
user32 = ctypes.windll.user32

SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
SWP_NOACTIVATE = 0x0010
HWND_TOPMOST = -1

GWL_EXSTYLE = -20
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_NOACTIVATE = 0x08000000


def keep_topmost():
    user32.SetWindowPos(
        hwnd,
        HWND_TOPMOST,
        0, 0, 0, 0,
        SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE
    )
    root.after(1000, keep_topmost)


def set_extended_style(hwnd):
    style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    style = style | WS_EX_TOOLWINDOW | WS_EX_NOACTIVATE
    user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)


# 再起動
def restart_app():
    python = sys.executable
    os.execl(python, python, *sys.argv)


# 終了
def close_app():
    root.destroy()


# メッセージ表示
def show_message():

    root.geometry("220x90+0+0")

    label.pack(expand=True)

    root.after(5000, hide_message)


# メッセージ非表示
def hide_message():

    label.pack_forget()

    root.update_idletasks()

    w = btn_frame.winfo_reqwidth() + 6
    h = btn_frame.winfo_reqheight() + 6

    root.geometry(f"{w}x{h}+0+0")

    root.after(60000, show_message)


def signal_handler(sig, frame):
    root.destroy()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

# ----------------

root = tk.Tk()

root.overrideredirect(True)
root.attributes("-alpha", 0.85)
root.attributes("-topmost", True)

frame = tk.Frame(root, bg="white")
frame.pack(fill="both", expand=True)

# ボタンフレーム
btn_frame = tk.Frame(frame, bg="white")
btn_frame.pack(anchor="nw")

reload_btn = tk.Button(
    btn_frame,
    text="🔄",
    command=restart_app,
    bd=0,
    font=("Arial", 10)
)
reload_btn.pack(side="left", padx=2)

stop_btn = tk.Button(
    btn_frame,
    text="⏹",
    command=close_app,
    bd=0,
    font=("Arial", 10)
)
stop_btn.pack(side="left", padx=2)

# メッセージ
label = tk.Label(
    frame,
    text="ジャングラーは？",
    font=("MS Gothic", 12),
    bg="white"
)

root.update_idletasks()

hwnd = root.winfo_id()

set_extended_style(hwnd)

# 初期状態：ボタンのみ
label.pack_forget()

root.update_idletasks()

w = btn_frame.winfo_reqwidth() + 6
h = btn_frame.winfo_reqheight() + 6
root.geometry(f"{w}x{h}+0+0")

# 1分後表示
root.after(60000, show_message)

# 最前面維持
keep_topmost()

root.mainloop()