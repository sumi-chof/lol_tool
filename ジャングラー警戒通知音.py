import tkinter as tk
import threading
import time
import keyboard
import simpleaudio as sa
import numpy as np
import sys
import os

# -----------------------------
# 設定
# -----------------------------

INTERVAL = 60
MAX_TIME = 20 * 60
volume = 0.4

running = False
start_time = None

# -----------------------------
# 音生成
# -----------------------------

def generate_tone(freq, duration):
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = np.sin(freq * t * 2 * np.pi)

    envelope = np.exp(-5 * t)
    tone = tone * envelope

    audio = tone * volume
    audio = (audio * 32767).astype(np.int16)

    return audio


def play_sound():

    pre = generate_tone(700, 0.08)
    main = generate_tone(520, 0.25)

    audio = np.concatenate((pre, np.zeros(2000), main))

    sa.play_buffer(audio, 1, 2, 44100)

# -----------------------------
# ランプ制御
# -----------------------------

def lamp_idle():
    canvas.itemconfig(lamp, fill="gray")

def lamp_running():
    canvas.itemconfig(lamp, fill="green")

def lamp_finished():
    canvas.itemconfig(lamp, fill="red")

def lamp_flash():
    canvas.itemconfig(lamp, fill="white")
    root.after(200, lamp_running)

# -----------------------------
# タイマー処理
# -----------------------------

def timer_loop():
    global running

    while running:

        elapsed = time.time() - start_time

        if elapsed >= MAX_TIME:
            running = False
            root.after(0, lamp_finished)
            break

        time.sleep(INTERVAL)

        if running:
            play_sound()
            root.after(0, lamp_flash)

# -----------------------------
# キー入力
# -----------------------------

def start_reset():
    global running, start_time

    start_time = time.time()

    if not running:
        running = True
        root.after(0, lamp_running)
        threading.Thread(target=timer_loop, daemon=True).start()
    else:
        root.after(0, lamp_running)

def key_listener():
    keyboard.add_hotkey('0', start_reset)
    keyboard.wait()

# -----------------------------
# UI操作
# -----------------------------

def restart():
    os.execv(sys.executable, ['python'] + sys.argv)

def quit_app():
    os._exit(0)

def volume_up():
    global volume
    volume = min(1.0, volume + 0.1)
    print("Volume:", int(volume * 100), "%")

def volume_down():
    global volume
    volume = max(0.0, volume - 0.1)
    print("Volume:", int(volume * 100), "%")

# -----------------------------
# UI作成
# -----------------------------

root = tk.Tk()

root.overrideredirect(True)
root.attributes("-topmost", True)

root.geometry("180x35+0+0")

frame = tk.Frame(root)
frame.pack()

canvas = tk.Canvas(frame, width=20, height=20, highlightthickness=0)
canvas.pack(side="left", padx=4)

lamp = canvas.create_oval(5,5,15,15, fill="gray")

btn_restart = tk.Button(frame, text="🔄", command=restart, width=3)
btn_restart.pack(side="left")

btn_quit = tk.Button(frame, text="⏹", command=quit_app, width=3)
btn_quit.pack(side="left")

btn_down = tk.Button(frame, text="▽", command=volume_down, width=3)
btn_down.pack(side="left")

btn_up = tk.Button(frame, text="△", command=volume_up, width=3)
btn_up.pack(side="left")

# -----------------------------
# キー入力スレッド
# -----------------------------

threading.Thread(target=key_listener, daemon=True).start()

# -----------------------------
# 起動
# -----------------------------

lamp_idle()

root.mainloop()