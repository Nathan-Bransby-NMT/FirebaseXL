import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class ToolTip:

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify="left", background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
        self.tooltip_window = None


class ImportTab(tk.Frame):

    _file: str

    def __init__(self, master):
        super().__init__(master)

        self._file = None
        self._fileImage = ImageTk.PhotoImage(Image.open('./assets/file.png'))
        self._nullImage = ImageTk.PhotoImage(Image.open('./assets/null.png'))

        self.file_button = tk.Button(
            self, image=self._nullImage,
            command=lambda:self.toggle_file(),
            background="#ffffff", relief=tk.RAISED,
            borderwidth=1
        )

        self.file_button.pack()

        ToolTip(self.file_button, "Upload an Excel file")


    def toggle_file(self) -> None:
        if self._file and messagebox.askyesno(
                "Close file", f"Do you want to close {self._file}?"):
            self._file = None
            return self.file_button.config(image=self._nullImage)
            ToolTip(self.file_button, "Upload an Excel file")
        self._file = filedialog.askopenfilename(
                filetypes=[("Excel files", "*.xlsx")])
        if self._file == "":
            return None
        ToolTip(self.file_button, "Clear file selected")
        return self.file_button.config(image=self._fileImage)


class GUI(tk.Tk):

    _maxsize: tuple[int, int]

    def __init__(self) -> None:
        super().__init__()
        self.title("FirebaseXL - GUI")
        self._maxsize = int(self.winfo_screenwidth()/2), int(self.winfo_screenheight()/2)
        self.geometry(f"{self.max_width}x{self.max_height}")
        self.wm_maxsize(*self._maxsize)
        self.resizable(False, False)

        self.notebook = ttk.Notebook(self)
        self.import_tab = ImportTab(self.notebook)
        self.export_tab = tk.Frame(self.notebook)
        self.notebook.add(self.import_tab, text="Import Excel to Firebase")
        self.notebook.add(self.export_tab, text="Export Firebase to Excel")
        self.notebook.pack(expand=True, fill=tk.BOTH)

    def launch(self) -> None:
        return self.mainloop()

    @property
    def max_width(self) -> int:
        return self._maxsize[0]

    @property
    def max_height(self) -> int:
        return self._maxsize[1]
