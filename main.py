#!/usr/bin/env python3
"""JyGet — anime-themed magnet/BitTorrent downloader."""

from gui import JyGetGUI
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    JyGetGUI(root)
    root.mainloop()
