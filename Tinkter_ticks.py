import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import time
import requests
import csv
from datetime import datetime


BTC_URL = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
ETH_URL = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"

ticks = []
running = False


def collect_ticks():
    global running
    while running:
        try:
            btc = float(requests.get(BTC_URL, timeout=5).json()["price"])
            eth = float(requests.get(ETH_URL, timeout=5).json()["price"])

            ticks.append([
                datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                btc,
                eth
            ])

            status_label.config(text=f"Ticks collected: {len(ticks)}")

            time.sleep(1)  # 1-second polling
        except Exception as e:
            print("Error:", e)


def start_collection():
    global running
    if running:
        messagebox.showinfo("Info", "Already running")
        return

    running = True
    threading.Thread(target=collect_ticks, daemon=True).start()
    status_label.config(text="Collecting ticks...")

def stop_collection():
    global running
    running = False
    status_label.config(text="Stopped")

def save_csv():
    if not ticks:
        messagebox.showwarning("Warning", "No ticks to save")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")]
    )

    if not file_path:
        return

    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "btc_price", "eth_price"])
        writer.writerows(ticks)

    messagebox.showinfo("Saved", f"Ticks saved to:\n{file_path}")


root = tk.Tk()
root.title("BTC–ETH Tick Collector")
root.geometry("400x250")

tk.Label(root, text="BTC–ETH Tick Collector", font=("Arial", 14)).pack(pady=10)

tk.Button(root, text="Start", width=15, command=start_collection).pack(pady=5)
tk.Button(root, text="Stop", width=15, command=stop_collection).pack(pady=5)
tk.Button(root, text="Download Ticks (CSV)", width=20, command=save_csv).pack(pady=10)

status_label = tk.Label(root, text="Idle")
status_label.pack(pady=10)

root.mainloop()
