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


def set_no_activate(hwnd):
    user32.SetWindowPos(
        hwnd,
        HWND_TOPMOST,
        0, 0, 0, 0,
        SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE
    )


# アプリ再起動
def restart_app():
    python = sys.executable
    os.execl(python, python, *sys.argv)


# アプリ終了
def close_app():
    root.destroy()


# 表示処理
def show_window():
    root.deiconify()
    root.after(5000, hide_window)  # 5秒後に消す


def hide_window():
    root.withdraw()
    root.after(60000, show_window)  # 1分後に表示


# Ctrl+C対応
def signal_handler(sig, frame):
    root.destroy()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

# ----------------

root = tk.Tk()

root.geometry("220x90+0+0")
root.attributes("-topmost", True)
root.attributes("-alpha", 0.7)
root.overrideredirect(True)

frame = tk.Frame(root, bg="white")
frame.pack(fill="both", expand=True)

# ボタン
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

# テキスト
label = tk.Label(
    frame,
    text="ジャングラーは？",
    font=("MS Gothic", 12),
    bg="white"
)
label.pack(expand=True)

# フォーカス奪わない設定
root.update_idletasks()
hwnd = root.winfo_id()
set_no_activate(hwnd)

# 最初は非表示
root.withdraw()

# 1分後に最初の表示
root.after(60000, show_window)

root.mainloop()