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

        label = tk.Label(
            tw, text=self.text, justify="left",
            background="#ffffe0", relief="solid", borderwidth=1
        )
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
        self.tooltip_window = None


class WrapWidgets(tk.Frame):

    def __init__(self, master, *widgets) -> None:
        super().__init__(master=master)
        self.widgets = widgets
        for widget in self.widgets:
            widget.pack(expand=False)
        self.pack(expand=False)


class ImportTab(tk.Frame):

    _file: str
    _destination: tk.StringVar

    def __init__(self, master):
        super().__init__(master, background="#00a1e4")

        self._file = None
        self._destination = tk.StringVar(self, "Enter Firebase Credentials:")
        self._fileImage = ImageTk.PhotoImage(Image.open('./assets/file.png'))
        self._nullImage = ImageTk.PhotoImage(Image.open('./assets/null.png'))

        self.title = tk.Label(
            self, justify=tk.CENTER,
            text="Import an Excel file to a Firebase database",
            font=("Arial", 24, "bold"),
            background="#00a1e4"
        )

        # Select a file label
        self.file_title = tk.Label(
            self, justify=tk.LEFT,
            text="Select an Excel file:",
            font=("Arial", 16),
            background="#00a1e4"
        )

        # Upload / clear file button
        self.file_button = tk.Button(
            self, image=self._nullImage,
            command=lambda:self.toggle_file(),
            background="#ffffff", relief=tk.RAISED,
            borderwidth=1
        )

        # Entry for the firebase url
        self.entry = tk.Entry(self, textvariable=self._destination, width=50)

        # Pack the widgets into the Frame
        self.title.pack(expand=True, fill=tk.X, padx=20, pady=20)
        WrapWidgets(self, self.file_title, self.file_button)
        # self.file_title.pack(expand=True, fill=tk.X, padx=20, pady=20)
        # self.file_button.pack(expand=False)
        self.entry.pack(expand=True, fill=tk.X, padx=20, pady=20)

        # Wrap the button to display the correct tool-tips for the given file state.
        ToolTip(self.file_button, "Upload an Excel file")

        # Event binding functions
        self.entry.bind("<FocusIn>", lambda e: self._enter_destination_entry(e))
        self.entry.bind("<FocusOut>", lambda e: self._exit_destination_entry(e))

    def _enter_destination_entry(self, event) -> None:
        if self._destination.get() == "Enter Firebase Credentials:":
            self._destination.set("")

    def _exit_destination_entry(self, event) -> None:
        if self._destination.get() == "":
            self._destination.set("Enter Firebase Credentials:")

    def toggle_file(self) -> None:
        if self._file and messagebox.askyesno(
                "Close file", f"Do you want to close {self._file}?"):
            self._file = None
            ToolTip(self.file_button, "Upload an Excel file")
            self.file_title.config(text=self._file)
            return self.file_button.config(image=self._nullImage)

        self._file = filedialog.askopenfilename(
                filetypes=[("Excel files", "*.xlsx")])

        self.file_title.config(text="Select an Excel file:")

        if self._file == "":
            return None
        ToolTip(self.file_button, "Clear file selected")
        return self.file_button.config(image=self._fileImage)


class ExportTab(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.title = tk.Label(self, text="Export Firebase table to Excel")

        self.title.pack(expand=True, fill=tk.X, padx=20, pady=20)


class GUI(tk.Tk):

    _maxsize: tuple[int, int]

    def __init__(self) -> None:
        super().__init__()
        self.title("FirebaseXL - GUI")
        self._maxsize = int(self.winfo_screenwidth()/5)*4, int(self.winfo_screenheight()/5)*4
        self.geometry(f"{self.max_width}x{self.max_height}")
        self.wm_maxsize(*self._maxsize)
        self.resizable(False, False)
        self.configure(background="#00a1e4")

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
