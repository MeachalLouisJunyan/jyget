#!/usr/bin/env python3
"""JyGet — anime-themed BitTorrent downloader GUI."""

import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

from engine import JyGetEngine, human_size, human_speed, parse_magnet


# ── Theme ──────────────────────────────────────────────────────────────
BG = "#fff0f5"
SURFACE = "#ffe4ec"
CARD = "#ffffff"
ACCENT = "#ff6b9d"
TEXT = "#4a2040"
TEXT_SEC = "#9c6b84"
ROW_EVEN = "#fff0f5"
ROW_ODD = "#ffe8ee"
SELECT_BG = "#ffb6d0"
SELECT_FG = "#4a2040"
HEADER_BG = "#ff6b9d"
HEADER_FG = "#ffffff"
GREEN = "#6bc46e"
YELLOW = "#f0c040"
BLUE = "#60b0f0"
GRAY = "#b0a0a8"
PROGRESS_BG = "#ffd0d8"
PROGRESS_FG = ACCENT

FONT = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_HEADING = ("Segoe UI", 11, "bold")
FONT_SMALL = ("Segoe UI", 9)
FONT_BTN = ("Segoe UI", 10, "bold")

PADDING = 8


class JyGetGUI:
    """Main GUI window for JyGet."""

    def __init__(self, root):
        self.root = root
        self.root.title("JyGet")
        self.root.geometry("900x620")
        self.root.minsize(700, 500)
        self.root.configure(bg=BG)

        self.engine = JyGetEngine()
        self._gid_map = {}  # gid -> iid (Treeview item id)
        self._iid_map = {}  # iid -> gid
        self._refresh_job = None

        # ── Styles ────────────────────────────────────────────
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview",
                        background=CARD, foreground=TEXT,
                        rowheight=36, fieldbackground=CARD,
                        font=FONT)
        style.map("Treeview",
                  background=[("selected", SELECT_BG)],
                  foreground=[("selected", SELECT_FG)])
        style.configure("Treeview.Heading",
                        background=HEADER_BG, foreground=HEADER_FG,
                        font=FONT_BOLD, relief="flat")
        style.map("Treeview.Heading",
                  background=[("active", "#ff8aad")])

        style.configure("TButton",
                        background=ACCENT, foreground="#ffffff",
                        font=FONT_BTN, borderwidth=0, focusthickness=0,
                        padding=(16, 6))
        style.map("TButton",
                  background=[("active", "#ff8aad"), ("pressed", "#e05a8a")])

        style.configure("TLabel", background=BG, foreground=TEXT, font=FONT)
        style.configure("Stats.TLabel", background=SURFACE, foreground=TEXT, font=FONT)

        style.configure("Card.TFrame", background=CARD)
        style.configure("Surface.TFrame", background=SURFACE)
        style.configure("Progress.Horizontal.TProgressbar",
                        background=PROGRESS_FG,
                        troughcolor=PROGRESS_BG,
                        borderwidth=0, thickness=14)

        # ── Layout ────────────────────────────────────────────
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Top bar
        self._build_topbar()

        # Task list
        self._build_tasklist()

        # Bottom stats bar
        self._build_bottombar()

        # Context menu
        self._build_context_menu()

        # Start engine in background
        self.root.after(100, self._start_engine)

        # Refresh loop
        self.schedule_refresh()

    # ── UI Builders ────────────────────────────────────────────────

    def _build_topbar(self):
        frame = tk.Frame(self.root, bg=BG, padx=PADDING, pady=(PADDING, 2))
        frame.grid(row=0, column=0, sticky="ew")
        frame.columnconfigure(1, weight=1)

        # Logo / title
        lbl = tk.Label(frame, text="🌸 JyGet", bg=BG, fg=ACCENT,
                       font=("Segoe UI", 14, "bold"))
        lbl.grid(row=0, column=0, padx=(0, 10))

        # Magnet entry
        self.magnet_var = tk.StringVar()
        entry = tk.Entry(frame, textvariable=self.magnet_var,
                         font=FONT, bg=CARD, fg=TEXT,
                         relief="flat", bd=8, highlightthickness=1,
                         highlightcolor=ACCENT, highlightbackground="#d0b0b8")
        entry.grid(row=0, column=1, sticky="ew", padx=(0, 8))

        # 下载 button
        add_btn = tk.Button(frame, text="⬇ 下载", font=FONT_BTN,
                            bg=ACCENT, fg="#ffffff",
                            activebackground="#ff8aad", activeforeground="#ffffff",
                            relief="flat", bd=0, padx=18, pady=6,
                            cursor="hand2", command=self._on_add_magnet)
        add_btn.grid(row=0, column=2, padx=(0, 6))

        # 打开种子文件 button
        tor_btn = tk.Button(frame, text="📂 打开种子文件", font=FONT_BTN,
                            bg="#d490b0", fg="#ffffff",
                            activebackground="#e0a0c0", activeforeground="#ffffff",
                            relief="flat", bd=0, padx=14, pady=6,
                            cursor="hand2", command=self._on_add_torrent)
        tor_btn.grid(row=0, column=3)

        # Bind Enter key
        entry.bind("<Return>", lambda e: self._on_add_magnet())

    def _build_tasklist(self):
        container = tk.Frame(self.root, bg=BG, padx=PADDING, pady=(4, 0))
        container.grid(row=1, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        columns = ("name", "status", "progress", "size", "speed", "eta", "seeds")
        self.tree = ttk.Treeview(container, columns=columns,
                                 show="headings", selectmode="browse",
                                 style="Treeview")

        headings = [
            ("name", "📄 Name", 260),
            ("status", "Status", 80),
            ("progress", "Progress", 120),
            ("size", "Size", 90),
            ("speed", "Speed", 100),
            ("eta", "ETA", 80),
            ("seeds", "S/P", 70),
        ]
        for col, text, width in headings:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, minwidth=50)

        # Scrollbar
        vsb = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky="ns")
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Tag row colors
        self.tree.tag_configure("even", background=ROW_EVEN)
        self.tree.tag_configure("odd", background=ROW_ODD)

        # Bind right-click
        self.tree.bind("<Button-3>", self._show_context_menu)

    def _build_bottombar(self):
        frame = tk.Frame(self.root, bg=SURFACE, padx=PADDING, pady=(4, PADDING))
        frame.grid(row=2, column=0, sticky="ew")
        frame.columnconfigure(5, weight=1)

        self.stats_vars = {}
        labels = [
            ("⬇ DL", "dl_speed", "0 B/s"),
            ("⬆ UL", "ul_speed", "0 B/s"),
            ("▶ Active", "active", "0"),
            ("⏳ Waiting", "waiting", "0"),
            ("⏹ Stopped", "stopped", "0"),
        ]
        for i, (icon_key, key, default) in enumerate(labels):
            lbl = tk.Label(frame, text=f"{icon_key}: ", bg=SURFACE,
                           fg=TEXT_SEC, font=FONT_SMALL)
            lbl.grid(row=0, column=i * 2, padx=(0, 2))
            val = tk.Label(frame, text=default, bg=SURFACE,
                           fg=TEXT, font=FONT_BOLD)
            val.grid(row=0, column=i * 2 + 1, padx=(0, 12))
            self.stats_vars[key] = val

        # Download dir label
        self.dir_label = tk.Label(frame,
                                  text=f"📁 {self.engine.download_dir}",
                                  bg=SURFACE, fg=TEXT_SEC,
                                  font=FONT_SMALL, anchor="e")
        self.dir_label.grid(row=0, column=len(labels) * 2, sticky="e")

    def _build_context_menu(self):
        self.ctx_menu = tk.Menu(self.root, tearoff=0,
                                bg=CARD, fg=TEXT,
                                activebackground=ACCENT,
                                activeforeground="#ffffff",
                                font=FONT)

        self.ctx_menu.add_command(label="▶ Resume", command=self._ctx_resume)
        self.ctx_menu.add_command(label="⏸ Pause", command=self._ctx_pause)
        self.ctx_menu.add_separator()
        self.ctx_menu.add_command(label="🗑 Remove", command=self._ctx_remove)
        self.ctx_menu.add_command(label="🗑 Remove + Delete Files",
                                  command=self._ctx_remove_delete)
        self.ctx_menu.add_separator()
        self.ctx_menu.add_command(label="📂 Open Folder", command=self._ctx_open_folder)

    # ── Engine ────────────────────────────────────────────────────

    def _start_engine(self):
        if not self.engine.start():
            messagebox.showwarning(
                "JyGet",
                "aria2c 未找到。请确保 aria2c 在 PATH 中或与 engine.py 同目录。\n\n"
                "您仍可使用界面，但下载功能不可用。"
            )

    # ── Actions ────────────────────────────────────────────────────

    def _on_add_magnet(self):
        uri = self.magnet_var.get().strip()
        if not uri:
            return
        if not uri.startswith("magnet:?"):
            messagebox.showwarning("JyGet", "请输入有效的 magnet 链接。")
            return

        def run():
            try:
                gid = self.engine.add_magnet(uri)
            except Exception:
                gid = None
            self.root.after(0, lambda: self._after_add(uri, gid))

        self.magnet_var.set("")
        threading.Thread(target=run, daemon=True).start()

    def _on_add_torrent(self):
        path = filedialog.askopenfilename(
            title="选择种子文件",
            filetypes=[("Torrent files", "*.torrent"), ("All files", "*.*")]
        )
        if not path:
            return

        def run():
            try:
                gid = self.engine.add_torrent(path)
            except Exception:
                gid = None
            name = os.path.basename(path)
            self.root.after(0, lambda: self._after_add(name, gid))

        threading.Thread(target=run, daemon=True).start()

    def _after_add(self, name, gid):
        if gid is None:
            messagebox.showerror("JyGet", "添加下载失败。\n请检查 aria2c 是否运行。")

    def pause_gid(self, gid):
        threading.Thread(target=self.engine.pause, args=(gid,), daemon=True).start()

    def resume_gid(self, gid):
        threading.Thread(target=self.engine.resume, args=(gid,), daemon=True).start()

    def remove_gid(self, gid, delete_files=False):
        threading.Thread(target=self.engine.remove, args=(gid, delete_files),
                         daemon=True).start()

    def open_folder(self, gid):
        """Open the download directory for a given gid."""
        d = self.engine.download_dir
        if Path(d).is_dir():
            import subprocess
            subprocess.Popen(["explorer", d], shell=True)

    # ── Context Menu ──────────────────────────────────────────────

    def _show_context_menu(self, event):
        iid = self.tree.identify_row(event.y)
        if iid:
            self.tree.selection_set(iid)
            self.ctx_menu.post(event.x_root, event.y_root)

    def _selected_gid(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return self._iid_map.get(sel[0])

    def _ctx_pause(self):
        gid = self._selected_gid()
        if gid:
            self.pause_gid(gid)

    def _ctx_resume(self):
        gid = self._selected_gid()
        if gid:
            self.resume_gid(gid)

    def _ctx_remove(self):
        gid = self._selected_gid()
        if gid:
            self.remove_gid(gid, delete_files=False)

    def _ctx_remove_delete(self):
        gid = self._selected_gid()
        if gid:
            if messagebox.askyesno("JyGet", "确定要删除下载并移除文件吗？"):
                self.remove_gid(gid, delete_files=True)

    def _ctx_open_folder(self):
        gid = self._selected_gid()
        if gid:
            self.open_folder(gid)

    # ── Refresh ───────────────────────────────────────────────────

    def schedule_refresh(self):
        self._refresh_job = self.root.after(1000, self.refresh)

    def refresh(self):
        try:
            self._refresh_tasklist()
            self._refresh_stats()
        except Exception:
            pass
        self.schedule_refresh()

    def _refresh_tasklist(self):
        try:
            downloads = self.engine.get_downloads()
        except Exception:
            return

        seen_gids = set()
        row_tags = ("even", "odd")

        for idx, d in enumerate(downloads):
            gid = d.gid
            seen_gids.add(gid)

            # Determine status icon
            status = d.status if hasattr(d, 'status') else ''
            status_icon = self._status_icon(status)

            # Progress bar text
            pct = getattr(d, 'progress', 0) or 0
            completed = getattr(d, 'completed_length', 0) or 0
            total = getattr(d, 'total_length', 0) or 0

            size_str = human_size(total) if total > 0 else "∞"
            speed_str = human_speed(getattr(d, 'download_speed', 0) or 0)

            # ETA
            speed_bps = getattr(d, 'download_speed', 0) or 0
            remaining = total - completed
            if speed_bps > 0 and remaining > 0:
                eta_sec = remaining // speed_bps
                eta_str = self._format_eta(eta_sec) if eta_sec < 86400 else ">1d"
            else:
                eta_str = "∞" if status in ("active", "waiting") else "—"

            # Seeds / Peers
            seeds = getattr(d, 'num_seeders', 0) or 0
            peers = getattr(d, 'connections', 0) or 0
            sp = f"{seeds}/{peers}"

            # Name fallback
            name = getattr(d, 'name', '') or getattr(d, 'gid', '') or 'Unknown'
            if not name or name == gid:
                parsed = parse_magnet(getattr(d, 'magnet_link', ''))
                name = parsed.get('name') or gid[:8]

            # Progress display: bar chars
            bar = self._progress_bar(pct)

            values = (name, status_icon, bar, size_str, speed_str, eta_str, sp)

            if gid in self._gid_map:
                # Update existing row
                iid = self._gid_map[gid]
                self.tree.item(iid, values=values)
            else:
                # Insert new row
                tag = row_tags[idx % 2]
                iid = self.tree.insert("", "end", values=values, tags=(tag,))
                self._gid_map[gid] = iid
                self._iid_map[iid] = gid

        # Remove stale rows
        stale = []
        for gid, iid in list(self._gid_map.items()):
            if gid not in seen_gids:
                stale.append((gid, iid))
        for gid, iid in stale:
            self.tree.delete(iid)
            del self._gid_map[gid]
            del self._iid_map[iid]

    def _refresh_stats(self):
        try:
            s = self.engine.get_stats()
        except Exception:
            return

        self.stats_vars["dl_speed"].config(text=human_speed(s.get("download_speed", 0)))
        self.stats_vars["ul_speed"].config(text=human_speed(s.get("upload_speed", 0)))
        self.stats_vars["active"].config(text=str(s.get("num_active", 0)))
        self.stats_vars["waiting"].config(text=str(s.get("num_waiting", 0)))
        self.stats_vars["stopped"].config(text=str(s.get("num_stopped", 0)))

    # ── Helpers ───────────────────────────────────────────────────

    @staticmethod
    def _status_icon(status):
        mapping = {
            "active": "▶",
            "waiting": "⏳",
            "paused": "⏸",
            "error": "❌",
            "complete": "✅",
            "removed": "🗑",
            "seeding": "🌱",
        }
        return mapping.get(status, "❓")

    @staticmethod
    def _format_eta(sec):
        sec = int(sec)
        h, m, s = sec // 3600, (sec % 3600) // 60, sec % 60
        if h:
            return f"{h}h{m:02d}m"
        if m:
            return f"{m}m{s:02d}s"
        return f"{s}s"

    @staticmethod
    def _progress_bar(pct):
        pct = max(0, min(100, pct or 0))
        filled = int(pct / 5)
        empty = 20 - filled
        blocks = "█" * filled + "░" * empty
        return f"{blocks} {pct:.1f}%"

    # ── Cleanup ───────────────────────────────────────────────────

    def on_close(self):
        if self._refresh_job:
            self.root.after_cancel(self._refresh_job)
        threading.Thread(target=self.engine.stop, daemon=True).start()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = JyGetGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
