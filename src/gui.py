import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class GUI(tk.Tk):

    _maxsize: tuple[int, int]
    _file: str

    def __init__(self):
        super().__init__()
        self.title("Fire XL - GUI")
        self._maxsize = int(self.winfo_screenwidth()/2), int(self.winfo_screenheight()/2)
        self.geometry(f"{int(self.winfo_screenwidth()/2)}x{int(self.winfo_screenheight()/2)}")
        self.file_button = tk.Button(self, image=self.file_image, command=self.toggle_file)
        self.file_button.pack()

    def toggle_file(self) -> None:
        if self.file_opened and messagebox.askyesno("Close file", f"Do you want to close {self._file}?"):
            self._file = None
            return self.file_button.config(image=self.file_image)
        self._file = filedialog.askopenfilename()
        self.file_button.config(image=self.file_image)

    def launch(self) -> None:
        return self.mainloop()
    
    @property
    def max_width(self) -> int:
        return self._maxsize[0]
    
    @property
    def max_height(self) -> int:
        return self._maxsize[1]
    
    @property
    def file_opened(self) -> bool:
        return self._file != None
    
    @property
    def file_image(self) -> ImageTk.PhotoImage:
        image_file = "file.png" if self.file_opened else "null.png"
        image = Image.open(f"/assets/{image_file}")
        return ImageTk.PhotoImage(image)
