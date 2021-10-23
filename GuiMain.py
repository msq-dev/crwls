from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import math


class CrwlsApp():
    def __init__(self):
        self.root = Tk()
        self.root.title("CRWLS")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.mainframe = ttk.Frame(self.root, padding="20")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.controls_frame = ttk.Frame(self.mainframe)
        self.controls_frame.grid(column=0, sticky=(N, E, S, W))
        self.controls_frame.columnconfigure(0, weight=1)
        self.controls_frame.columnconfigure(1, weight=1)

        self.settings_btn = ttk.Button(self.controls_frame,
                                       text="Settings", command=self.open_config)
        self.settings_btn.grid(column=0, row=0, sticky=(W))
        self.quit_btn = ttk.Button(self.controls_frame,
                                   text="Quit", command=self.quit_app)
        self.quit_btn.grid(column=1, row=0, sticky=(E))

        # CENTER WINDOW
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = math.floor(ws * 0.2)
        y = math.floor(hs * 0.2)
        self.root.geometry(f"+{x}+{y}")

        self.root.mainloop()

    def open_config(self):
        from GuiSettings import ConfigGUI
        ConfigGUI(self.mainframe)

    def quit_app(self):
        wanna_quit = mb.askyesno(
            "Warning",
            "Do you want to quit CRWLS?",
            icon="warning"
        )
        if wanna_quit:
            self.root.destroy()
        else:
            self.mainframe.focus_set()


if __name__ == "__main__":
    CrwlsApp()
