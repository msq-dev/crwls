from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import math
import configparser

TABLE_COLS = ["Address", "Content Type", "Status Code", "Status", "Indexability", "Indexability Status", "Title 1", "Title 1 Length", "Title 1 Pixel Width", "Meta Description 1", "Meta Description 1 Length", "Meta Description 1 Pixel Width", "Meta Keywords 1", "Meta Keywords 1 Length", "H1-1", "H1-1 Length", "H1-2", "H1-2 Length", "H2-1", "H2-1 Length", "H2-2", "H2-2 Length", "Meta Robots 1", "X-Robots-Tag 1", "Meta Refresh 1", "Canonical Link Element 1", "rel=""next"" 1", "rel=""prev"" 1", "HTTP rel=""next"" 1", "HTTP rel=""prev"" 1",
              "amphtml Link Element", "Size (bytes)", "Word Count", "Text Ratio", "Crawl Depth", "Link Score", "Inlinks", "Unique Inlinks", "Unique JS Inlinks", "% of Total", "Outlinks", "Unique Outlinks", "Unique JS Outlinks", "External Outlinks", "Unique External Outlinks", "Unique External JS Outlinks", "Closest Similarity Match", "No. Near Duplicates", "Spelling Errors", "Grammar Errors", "Hash", "Response Time", "Last Modified", "Redirect URL", "Redirect Type", "Cookies", "HTTP Version", "URL Encoded Address", "Crawl Timestamp"]

# CONF_VARS
config = configparser.ConfigParser()
config.read("conf/config.ini")
conf = {
    "output_dir": config["DEV"]["outputpath"],
    "changes_dir": config["DEV"]["changespath"],
    "selected_cols": list(filter(None, config["DEFAULT"]["Columns"].split(",")))
}


class PathSelector():
    def __init__(self, row, parentframe, label, text_var, config_dir):
        self.parentframe = parentframe
        self.text_var = text_var
        self.config_dir = config_dir
        self.frame = ttk.Frame(parentframe, padding="0 0 0 5")
        self.frame.grid(row=row, sticky=(W))
        ttk.Label(self.frame, text=label,
                  style="Bold.TLabel").grid(column=0, row=0, sticky=(W))
        ttk.Label(self.frame, textvariable=self.text_var,
                  style="PathString.TLabel").grid(column=0, row=1, sticky=(W))
        ttk.Button(self.frame, text="Select",
                   command=self.select_dir).grid(column=1, row=1, sticky=(W))

    def select_dir(self):
        prev_val = conf[self.config_dir]
        dir_ = fd.askdirectory(parent=self.parentframe) or prev_val
        conf[self.config_dir] = dir_
        self.text_var.set(value=dir_)


class CheckBox(ttk.Checkbutton):
    def __init__(self, parent, text_value, text_var, **kwargs):
        self.text_value = text_value
        self.checked = IntVar(value=self.text_value in conf["selected_cols"])
        self.text_var = text_var
        kwargs["text"] = self.text_value
        kwargs["variable"] = self.checked
        kwargs["command"] = self.toggle_value
        kwargs["style"] = "CheckBox.TCheckbutton"
        if self.text_value == "Address":
            kwargs["state"] = "disabled"
        super().__init__(parent, **kwargs)

    def toggle_value(self):
        if self.text_value not in conf["selected_cols"]:
            conf["selected_cols"].append(self.text_value)
            self.text_var.set(
                value="\n".join(conf["selected_cols"]))
        else:
            conf["selected_cols"].remove(self.text_value)
            self.text_var.set(
                value="\n".join(conf["selected_cols"]))


class ConfigGUI():
    def __init__(self):
        self.root = Tk()
        self.root.title("CONFIG")

        # LAYOUT
        self.mainframe = ttk.Frame(self.root, padding="20")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.select_paths_frame = ttk.Frame(self.mainframe, padding="0 0 0 20")
        self.select_paths_frame.grid(column=0, row=0, sticky=(W))
        self.select_cols_frame = ttk.Frame(self.mainframe, padding="0 0 0 20")
        self.select_cols_frame.grid(column=0, row=1, sticky=(W))
        self.outputframe = ttk.Frame(self.mainframe)
        self.outputframe.grid(column=0, row=2, sticky=(W, E))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # STYLES
        self.style = ttk.Style()
        self.style.configure(
            "Bold.TLabel", font="-weight bold", padding="0 0 0 2")
        self.style.configure("PathString.TLabel", foreground="#112885", padding="0 0 20 0",
                             font=("Courier", 14))
        self.style.configure("CheckBox.TCheckbutton", padding="0 0 15 0")
        self.style.configure("SelectedCols.TLabel",
                             foreground="#112885", padding="10 0 0 30", font=("Courier", 14))
        self.style.configure("Save.TButton")
        self.style.map("TCheckbutton", foreground=[("disabled", "#888")])

        # TEXTVARIABLES
        self.var_output_dir = StringVar(value=conf["output_dir"])
        self.var_changes_dir = StringVar(value=conf["changes_dir"])
        self.var_selected_cols = StringVar(
            value="\n".join(conf["selected_cols"]))
        self.saved_msg = StringVar()

        # CONTENT
        PathSelector(0, self.select_paths_frame, "Output Directory",
                     self.var_output_dir, "output_dir")
        PathSelector(1, self.select_paths_frame, "Changes Directory",
                     self.var_changes_dir, "changes_dir")

        ttk.Label(self.select_cols_frame, text="Columns", style="Bold.TLabel").grid(
            column=0, row=0, sticky=(W))
        widget_row = 1
        for index, col in enumerate(TABLE_COLS):
            boxes_per_col = 10
            widget_col = math.floor(index / boxes_per_col)
            if index % boxes_per_col == 0:
                widget_row = 1
            widget_row += 1
            CheckBox(self.select_cols_frame, col, self.var_selected_cols).grid(
                column=widget_col, row=widget_row, sticky=(W))

        ttk.Label(self.outputframe, text="Selected Columns",
                  style="Bold.TLabel").grid(column=0, sticky=(W))
        ttk.Label(
            self.outputframe,
            textvariable=self.var_selected_cols,
            wraplength=700,
            justify="left",
            style="SelectedCols.TLabel"
        ).grid(row=1, sticky=(W, E))

        ttk.Button(self.outputframe, command=self.save_conf, text="Save",
                   style="Save.TButton").grid(row=2, sticky=(W))

        ttk.Label(self.outputframe, textvariable=self.saved_msg).grid(
            column=2, row=2, sticky=(W))

        ttk.Button(self.outputframe, command=self.quit, text="Quit",
                   style="Save.TButton").grid(row=3, sticky=(W))

        self.root.mainloop()

    def save_conf(self):
        config["DEV"]["outputpath"] = conf["output_dir"]
        config["DEV"]["changespath"] = conf["changes_dir"]
        config["DEFAULT"]["Columns"] = ",".join(conf["selected_cols"])
        with open("conf/config.ini", "w") as configfile:
            config.write(configfile)
        self.saved_msg.set("Saved!")

    def quit(self):
        self.root.destroy()


if __name__ == "__main__":
    ConfigGUI()
