from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import math
from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path


def split_conf_str(string):
    """
    Turn string from config file into list with possible trailing comma in mind
    """
    return list(filter(None, string.split(",")))


# CONF_VARS
config = ConfigParser(interpolation=ExtendedInterpolation())
config.read("conf/config.ini")
conf = {
    "dir_app": config["DEV"]["app"],
    "dir_output": config["DEV"]["outputpath"],
    "dir_changes": config["DEV"]["changespath"],
    "urls": config["DEV"]["urlslist"],
    "cols_selected": split_conf_str(config["DEV"]["columns"]),
    "cols_all": split_conf_str(config["DEV"]["allcols"])
}

# STYLES
style = ttk.Style()
style.configure(
    "Bold.TLabel",
    font="-weight bold",
    padding="0 0 0 2"
)
style.configure(
    "PathString.TLabel",
    foreground="#112885",
    padding="0 0 20 0",
    font=("Courier", 14)
)
style.configure(
    "Modified.TLabel",
    foreground="#9b870c",
    font="-size 20"
)
style.configure(
    "Saved.TLabel",
    foreground="green",
    font="-size 20"
)
style.configure(
    "Delete.TButton",
    foreground="red",
)
style.configure("CheckBox.TCheckbutton", padding="0 0 15 0")
style.map("TCheckbutton", foreground=[("disabled", "#888")])
style.map("TButton", foreground=[("disabled", "#888")])


class ConfigGUI(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("CONFIG")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.mainframe = ttk.Frame(self, padding="20")
        self.mainframe.grid(column=0, row=0, sticky=(N, E, S, W))

        # TEXTVARIABLES
        self.var_modified = IntVar(value=0)
        self.var_dir_app = StringVar(value=conf["dir_app"])
        self.var_dir_output = StringVar(value=conf["dir_output"])
        self.var_dir_changes = StringVar(value=conf["dir_changes"])
        self.var_urls_list = StringVar(value=conf["urls"])
        self.var_cols_selected = StringVar(
            value="\n".join(conf["cols_selected"]))

        # CONTENT
        self.select_paths_frame = ttk.Frame(self.mainframe, padding="0 0 0 20")
        self.select_paths_frame.grid(column=0, sticky=(W))

        PathSelector(self.select_paths_frame,
                     "App Directory", self.var_dir_app, "dir_app", self.handle_modified)
        PathSelector(self.select_paths_frame,
                     "Output Directory", self.var_dir_output, "dir_output", self.handle_modified)
        PathSelector(self.select_paths_frame,
                     "Changes Directory", self.var_dir_changes, "dir_changes", self.handle_modified)
        PathSelector(self.select_paths_frame,
                     "URLs List", self.var_urls_list, "urls", self.handle_modified)

        self.label_frame = ttk.Frame(self.mainframe)
        self.label_frame.grid(column=0, sticky=(N, E, S, W))
        self.label_frame.columnconfigure(0, weight=1)
        self.label_frame.columnconfigure(1, weight=20)

        ttk.Label(self.label_frame, text="Columns", style="Bold.TLabel").grid(
            column=0, sticky=(W))

        if config["DEV"]["allcols"] != config["DEFAULT"]["allcols"]:
            self.restore_cols_btn = ttk.Button(
                self.label_frame,
                text="Restore Columns",
                command=self.restore_columns
            )
            self.restore_cols_btn.grid(column=1, row=0, sticky=(W))

        self.checkboxes_frame = ttk.Frame(self.mainframe, padding="0 10 0 20")
        self.checkboxes_frame.grid(column=0, sticky=(W))
        self.checkboxes_frame.columnconfigure(0, weight=1)
        self.populate_checkboxes()

        self.controls_frame = ttk.Frame(self.mainframe, padding="0 40 20 20")
        self.controls_frame.grid(column=0, sticky=(N, E, S, W))
        self.controls_frame.columnconfigure(0, weight=1)
        self.controls_frame.columnconfigure(1, weight=1)
        self.controls_frame.columnconfigure(2, weight=1)

        self.save_btn = ttk.Button(
            self.controls_frame,
            command=self.save_conf,
            text="Save",
            state="disabled"
        )
        self.save_btn.grid(column=0, row=0, sticky=(W))

        self.label_of_change = ttk.Label(
            self.controls_frame,
            text=""
        )
        self.label_of_change.grid(column=1, row=0, sticky=(W, E))

        ttk.Button(
            self.controls_frame,
            command=self.quit_conf,
            text="Quit",
        ).grid(column=2, row=0, sticky=(E))

    def populate_checkboxes(self):
        """
        Make columns selectable
        """
        class GridInfo():
            def __init__(self, frame, col, row):
                self.frame = frame
                self.col = col
                self.row = row

        widget_row = 0
        for index, table_col in enumerate(conf["cols_all"]):
            boxes_per_col = 16
            widget_col = math.floor(index / boxes_per_col)
            if index % boxes_per_col == 0:
                widget_row = 0
            widget_row += 1
            CheckBox(GridInfo(self.checkboxes_frame, widget_col, widget_row),
                     table_col, self.var_cols_selected, self.handle_modified)

    def restore_columns(self):
        self.handle_modified()
        for box in self.checkboxes_frame.winfo_children():
            box.destroy()
        conf["cols_all"] = split_conf_str(config["DEFAULT"]["allcols"])
        self.populate_checkboxes()
        self.restore_cols_btn.destroy()

    def handle_modified(self):
        self.var_modified.set(value=1)
        self.label_of_change["style"] = "Modified.TLabel"
        self.label_of_change["text"] = "Modified ..."
        self.save_btn["state"] = "normal"

    def handle_saved(self):
        self.var_modified.set(value=0)
        self.label_of_change["style"] = "Saved.TLabel"
        self.label_of_change["text"] = "Saved!"
        self.save_btn["state"] = "disabled"

    def save_conf(self):
        config["DEV"]["app"] = self.var_dir_app.get()
        config["DEV"]["outputpath"] = self.var_dir_output.get()
        config["DEV"]["changespath"] = self.var_dir_changes.get()
        config["DEV"]["urlslist"] = self.var_urls_list.get()
        config["DEV"]["columns"] = ",".join(conf["cols_selected"])
        config["DEV"]["allcols"] = ",".join(conf["cols_all"])
        with open("conf/config.ini", "w") as configfile:
            config.write(configfile)
        self.handle_saved()

    def quit_conf(self):
        if self.var_modified.get():
            wanna_quit = mb.askyesno(
                "Warning",
                "Do you want to quit without saving?",
                icon="warning"
            )
            if wanna_quit:
                self.destroy()
            else:
                self.mainframe.focus_set()
        else:
            self.destroy()


class PathSelector():
    """
    Widget to select paths to certain folders or files
    """

    def __init__(self, parentframe, label, var_path, conf_dir, handle_modified):
        self.parentframe = parentframe
        self.label = label
        self.var_path = var_path
        self.conf_dir = conf_dir
        self.handle_modified = handle_modified

        self.selector_frame = ttk.Frame(self.parentframe, padding="0 0 0 10")
        self.selector_frame.grid(sticky=(N, E, S, W))
        self.selector_frame.columnconfigure(0, weight=1)
        self.selector_frame.columnconfigure(1, weight=1)

        ttk.Label(self.selector_frame, text=self.label,
                  style="Bold.TLabel").grid(column=0, row=0, sticky=(W))
        ttk.Label(self.selector_frame, textvariable=self.var_path,
                  style="PathString.TLabel").grid(column=0, row=1, sticky=(W))
        ttk.Button(self.selector_frame, text="Select",
                   command=self.select_dir).grid(column=1, row=1, sticky=(E))

    def select_dir(self):
        """
        Trigger filedialog to select a directory or file
        """
        prev_val = self.var_path.get()
        if self.conf_dir == "dir_app" or self.conf_dir == "urls":
            dir_ = fd.askopenfilename(parent=self.parentframe,
                                      initialdir=Path.home()) or prev_val
        else:
            dir_ = fd.askdirectory(parent=self.parentframe,
                                   initialdir=Path.home()) or prev_val

        self.var_path.set(value=dir_)
        if dir_ != prev_val:
            conf[self.conf_dir] = dir_
            self.handle_modified()


class CheckBox():
    """
    Widget to select the columns one wants to work with
    """

    def __init__(self, grid_info, text_value, var_selected, handle_modified):
        self.parent = grid_info.frame
        self.col = grid_info.col
        self.row = grid_info.row
        self.handle_modified = handle_modified

        self.text_value = text_value
        self.checked = IntVar(value=self.text_value in conf["cols_selected"])
        self.var_selected = var_selected

        self.box_frame = ttk.Frame(self.parent, padding="0 0 40 0")
        self.box_frame.grid(
            column=self.col, row=self.row, sticky=(N, E, S, W))
        self.box_frame.columnconfigure(0, weight=1)
        self.box_frame.columnconfigure(1, weight=1)

        self.checkbox = ttk.Checkbutton(
            self.box_frame,
            text=self.text_value,
            variable=self.checked,
            command=self.toggle_value,
            style="CheckBox.TCheckbutton"
        )

        if self.text_value == "Address":
            self.checkbox["state"] = "disabled"
        self.checkbox.grid(column=0, row=0, sticky=(W))

        if not self.text_value == "Address":
            self.delete_box_btn = ttk.Button(
                self.box_frame,
                text="Delete",
                style="Delete.TButton",
                command=self.delete_checkbox
            )
            self.delete_box_btn.grid(column=1, row=0, sticky=(E))

    def toggle_value(self):
        """
        Select or deselect columns
        """
        self.handle_modified()
        if self.text_value not in conf["cols_selected"]:
            conf["cols_selected"].append(self.text_value)
            self.var_selected.set(
                value="\n".join(conf["cols_selected"]))
        else:
            conf["cols_selected"].remove(self.text_value)
            self.var_selected.set(
                value="\n".join(conf["cols_selected"]))

    def delete_checkbox(self):
        """
        Get rid of rarely used columns
        """
        wanna_delete = mb.askyesno(
            "Warning",
            f'Delete checkbox for column "{self.text_value}"?',
            icon="warning"
        )
        if wanna_delete:
            self.handle_modified()
            conf["cols_all"].remove(self.text_value)
            try:
                conf["cols_selected"].remove(self.text_value)
            except ValueError:
                pass
            mb.showinfo("Info", "This checkbox will not bother you anymore")
            self.box_frame.grid_remove()
            self.parent.focus_set()
        else:
            self.parent.focus_set()
