#!/usr/bin/env python3
"""JyGet — magnet/torrent download engine. Wraps aria2c with JSON-RPC."""

import os
import subprocess
import threading
import time
from pathlib import Path

import aria2p


class JyGetEngine:
    """Manages aria2c process and provides download control."""

    def __init__(self, download_dir=None):
        self.download_dir = download_dir or str(Path.home() / "Downloads" / "JyGet")
        self._process = None
        self._api = None
        self._client = None
        self._running = False
        self._rpc_port = 6800
        self._rpc_secret = "jyget_secret"

        Path(self.download_dir).mkdir(parents=True, exist_ok=True)

    def start(self):
        if self._running:
            return True

        aria2c = self._find_aria2c()
        if not aria2c:
            return False

        args = [
            aria2c,
            "--enable-rpc",
            f"--rpc-listen-port={self._rpc_port}",
            f"--rpc-secret={self._rpc_secret}",
            "--rpc-allow-origin-all",
            "--rpc-listen-all",
            f"--dir={self.download_dir}",
            "--max-concurrent-downloads=10",
            "--max-connection-per-server=16",
            "--split=16",
            "--min-split-size=1M",
            "--bt-enable-lpd=true",
            "--bt-max-peers=200",
            "--bt-request-peer-speed-limit=50M",
            "--enable-dht=true",
            "--dht-listen-port=6881-6999",
            "--seed-time=0",
            "--file-allocation=trunc",
            "--disk-cache=128M",
            "--quiet=true",
            "--log-level=error",
        ]

        self._process = subprocess.Popen(
            args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(1.0)

        self._api = aria2p.API(
            aria2p.Client(
                host="http://127.0.0.1",
                port=self._rpc_port,
                secret=self._rpc_secret,
            )
        )
        self._running = True
        return True

    def stop(self):
        if self._api:
            try:
                self._api.shutdown()
            except Exception:
                pass
        if self._process:
            self._process.terminate()
            self._process.wait(timeout=5)
        self._running = False

    def _find_aria2c(self):
        bundle = Path(__file__).parent / "aria2c.exe"
        if bundle.is_file():
            return str(bundle)
        for name in ["aria2c", "aria2c.exe"]:
            for base in os.environ.get("PATH", "").split(os.pathsep):
                p = Path(base) / name
                if p.is_file():
                    return str(p)
        return None

    @property
    def api(self):
        return self._api

    @property
    def running(self):
        return self._running

    # ── Download actions ────────────────────────────────────

    def add_magnet(self, uri):
        """Add a magnet link download. Returns gid."""
        if not self._api:
            return None
        try:
            gid = self._api.add_magnet(uri)
            return gid
        except Exception:
            return None

    def add_torrent(self, file_path):
        """Add a .torrent file. Returns gid."""
        if not self._api:
            return None
        try:
            gid = self._api.add_torrent(str(file_path))
            return gid
        except Exception:
            return None

    def add_url(self, url, out_name=None):
        """Add a direct URL download."""
        if not self._api:
            return None
        try:
            opts = {}
            if out_name:
                opts["out"] = out_name
            gid = self._api.add_uris([url], options=opts)
            return gid
        except Exception:
            return None

    def pause(self, gid):
        try:
            self._api.pause(gid)
        except Exception:
            pass

    def resume(self, gid):
        try:
            self._api.unpause(gid)
        except Exception:
            pass

    def remove(self, gid, delete_files=False):
        try:
            self._api.remove(gid)
            if delete_files:
                self._api.remove_download_result(gid)
        except Exception:
            pass

    def get_downloads(self):
        try:
            return self._api.get_downloads()
        except Exception:
            return []

    def get_stats(self):
        try:
            return self._api.get_global_stat()
        except Exception:
            return {"download_speed": 0, "upload_speed": 0,
                    "num_active": 0, "num_waiting": 0, "num_stopped": 0}

    def set_global_speed_limit(self, download_limit=0, upload_limit=0):
        """0 = unlimited. In bytes/sec."""
        try:
            opts = {}
            if download_limit:
                opts["max-overall-download-limit"] = str(download_limit)
            if upload_limit:
                opts["max-overall-upload-limit"] = str(upload_limit)
            if opts:
                self._api.change_global_option(opts)
        except Exception:
            pass

    def set_download_dir(self, path):
        try:
            self._api.change_global_option({"dir": str(path)})
            self.download_dir = path
        except Exception:
            pass


def human_size(n):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def human_speed(n):
    if n == 0:
        return "0 B/s"
    for unit in ("B/s", "KB/s", "MB/s", "GB/s"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB/s"


def parse_magnet(uri):
    """Extract info from magnet link."""
    info = {"name": "", "hash": "", "trackers": []}
    if not uri.startswith("magnet:?"):
        return info
    parts = uri[8:].split("&")
    for p in parts:
        if "=" not in p:
            continue
        k, _, v = p.partition("=")
        if k == "dn":
            from urllib.parse import unquote
            info["name"] = unquote(v)
        elif k == "xt" and "btih" in v.lower():
            info["hash"] = v.split(":")[-1]
        elif k == "tr":
            from urllib.parse import unquote
            info["trackers"].append(unquote(v))
    return info
