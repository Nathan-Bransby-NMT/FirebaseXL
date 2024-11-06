import unittest
import tkinter as tk
from PIL import Image, ImageTk
from src.gui import ToolTip, ImportTab, GUI


class TestToolTip(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.button = tk.Button(self.root, text="Test Button")
        self.tooltip = ToolTip(self.button, "Test Tooltip")

    def test_tooltip_initialization(self):
        self.assertEqual(self.tooltip.widget, self.button)
        self.assertEqual(self.tooltip.text, "Test Tooltip")
        self.assertIsNone(self.tooltip.tooltip_window)

    def tearDown(self):
        self.root.destroy()

class TestImportTab(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.import_tab = ImportTab(self.root)

    def test_import_tab_initialization(self):
        self.assertIsNone(self.import_tab._file)
        self.assertIsInstance(self.import_tab._fileImage, ImageTk.PhotoImage)
        self.assertIsInstance(self.import_tab._nullImage, ImageTk.PhotoImage)
        self.assertIsInstance(self.import_tab.file_button, tk.Button)
        self.assertEqual(self.import_tab.file_button.cget("image"), str(self.import_tab._nullImage))

    def tearDown(self):
        self.root.destroy()

class TestGUI(unittest.TestCase):

    def setUp(self):
        self.gui = GUI()

    def test_gui_initialization(self):
        self.assertEqual(self.gui.title(), "FirebaseXL - GUI")
        self.assertFalse(self.gui.resizable()[0])
        self.assertFalse(self.gui.resizable()[1])
        self.assertIsInstance(self.gui.notebook, tk.ttk.Notebook)
        self.assertIsInstance(self.gui.import_tab, ImportTab)
        self.assertIsInstance(self.gui.export_tab, tk.Frame)

    def tearDown(self):
        self.gui.destroy()


if __name__ == '__main__':
    unittest.main()
