import tkinter as tk
from tkinter import filedialog
from typing import IO
from PIL import Image, ImageTk


class ContextLoader:

    _path: str
    _stream: IO | None

    def __init__(self) -> None:
        self._path = filedialog.askopenfilename()
        self._stream = None

    def __enter__(self) -> IO:
        self._stream = open(self._path, "r")
        return self._stream
    
    def __exit__(self, exc_val, exc_type, traceback) -> None:
        self._stream.close()
