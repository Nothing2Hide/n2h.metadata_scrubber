import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

from n2h.metadata_scrubber.scrubber import remove_metadata


class ScrubberGui:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title = "Metadata scrubber"
        self.lbl_default = "No file selected"
        self.file_label = tk.Label(self.window,
                                   text=self.lbl_default, width=50)
        self.file_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.browse_btn = tk.Button(self.window, text="Browse",
                                    command=self.browse)
        self.browse_btn.pack(side=tk.LEFT, padx=5, pady=5)
        self.rm_btn = tk.Button(self.window, text="Remove",
                                command=self.remove_meta, state=tk.DISABLED)
        self.rm_btn.pack(side=tk.RIGHT, padx=5, pady=5)

    def display(self):
        self.window.mainloop()

    def remove_meta(self):
        if self.browsed_file != self.lbl_default:
            try:
                remove_metadata(self.browsed_file)
            except Exception as e:
                showerror(e.message)
        else:
            showerror("No such file selected")

    def browse(self):
        # tk.Tk().withdraw()
        # TODO define better filetypes
        filetypes = [('all files', '.*')]
        self.browsed_file = askopenfilename(
            title="Open a file to scrubber",
            filetypes=filetypes
        )
        self.update_file_label(self.browsed_file)
        self.enable_rm_btn()

    def enable_rm_btn(self):
        if self.browsed_file:
            self.rm_btn['state'] = tk.NORMAL

    def update_file_label(self, text):
        if text:
            self.file_label['text'] = text


def main():
    gui = ScrubberGui()
    gui.display()
