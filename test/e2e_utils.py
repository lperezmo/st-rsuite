"""Helpers for the CCv2 e2e tests: run a Streamlit script in a subprocess and
wait until its health endpoint is live. Adapted from the streamlit-aggrid e2e
harness.
"""

import contextlib
import logging
import os
import socket
import subprocess
import sys
import time
import typing
from contextlib import closing
from tempfile import TemporaryFile


LOGGER = logging.getLogger(__file__)


def _find_free_port() -> int:
    """Return a free TCP port chosen by the OS."""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return int(s.getsockname()[1])


class AsyncSubprocess:
    """Wraps subprocess.Popen, capturing output to a temp file to avoid
    deadlocks on large output."""

    def __init__(self, args: typing.List[str]):
        self.args = args
        self._proc: typing.Optional[subprocess.Popen] = None
        self._stdout_file: typing.Optional[typing.IO[str]] = None

    def start(self) -> None:
        self._stdout_file = TemporaryFile("w+")
        LOGGER.info("Running: %s", " ".join(self.args))
        self._proc = subprocess.Popen(
            self.args,
            stdout=self._stdout_file,
            stderr=subprocess.STDOUT,
            text=True,
        )

    def stop(self) -> typing.Optional[str]:
        stdout = None
        if self._stdout_file is not None:
            with contextlib.suppress(Exception):
                self._stdout_file.seek(0)
                stdout = self._stdout_file.read()
            self._stdout_file.close()
            self._stdout_file = None
        if self._proc is not None:
            self._proc.terminate()
            with contextlib.suppress(Exception):
                self._proc.wait(timeout=10)
            self._proc = None
        return stdout


class StreamlitRunner:
    """Context manager that runs a Streamlit script and exposes its URL."""

    def __init__(self, script_path: os.PathLike, server_port: typing.Optional[int] = None):
        self.script_path = script_path
        self.server_port = server_port
        self._process: typing.Optional[AsyncSubprocess] = None

    def __enter__(self) -> "StreamlitRunner":
        self.server_port = self.server_port or _find_free_port()
        self._process = AsyncSubprocess(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                str(self.script_path),
                f"--server.port={self.server_port}",
                "--server.headless=true",
                "--server.fileWatcherType=none",
                "--browser.gatherUsageStats=false",
                "--global.developmentMode=false",
            ]
        )
        self._process.start()
        if not self._wait_for_server():
            out = self._process.stop()
            raise RuntimeError(f"Streamlit failed to start.\n{out}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._process is not None:
            self._process.stop()

    def _wait_for_server(self, timeout: int = 60) -> bool:
        import requests

        deadline = time.time() + timeout
        health = self.server_url + "/_stcore/health"
        while time.time() < deadline:
            with contextlib.suppress(requests.RequestException):
                if requests.get(health, timeout=2).text == "ok":
                    return True
            time.sleep(1)
        return False

    @property
    def server_url(self) -> str:
        if not self.server_port:
            raise RuntimeError("Unknown server port")
        return f"http://localhost:{self.server_port}"
