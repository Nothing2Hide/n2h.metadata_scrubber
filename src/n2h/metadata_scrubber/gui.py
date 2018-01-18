import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror, showinfo

from n2h.metadata_scrubber.scrubber import (remove_metadata,
                                            default_output_filename,
                                            )


class ScrubberGui:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title = "Metadata scrubber"
        self.window.attributes('-type', 'dialog')
        self.lbl_savesas = ""
        self.lbl_default = "No file selected"
        self.saveas_file = None
        self.browsed_file = None

        self.saveas_label = tk.Label(self.window,
                                     text=self.lbl_savesas, width=50)
        self.file_label = tk.Label(self.window,
                                   text=self.lbl_default, width=50)
        self.browse_btn = tk.Button(self.window, text="Browse",
                                    command=self.browse)
        self.rm_btn = tk.Button(self.window, text="Remove",
                                command=self.remove_meta, state=tk.DISABLED)
        self.saveas_btn = tk.Button(self.window, text="Save as",
                                    command=self.saveas, state=tk.DISABLED)

        self.file_label.grid(sticky=tk.E, padx=5, pady=5)
        self.saveas_label.grid(sticky=tk.E, padx=5, pady=5)
        self.browse_btn.grid(row=0, column=1, padx=5, pady=5)
        self.rm_btn.grid(row=0, column=2, padx=5, pady=5)
        self.saveas_btn.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

    def display(self):
        self.window.mainloop()

    def remove_meta(self):
        if self.browsed_file != self.lbl_default:
            try:
                remove_metadata(self.browsed_file, outfile=self.saveas_file)
            except Exception as error:
                showerror(title="Error", message=str(error))
            else:
                showinfo(title="Sucess", message="File scrubbed")
        else:
            showerror(title="Error", message="No such file selected")

    def browse(self):
        # TODO define better filetypes
        filetypes = [('all files', '.*')]
        self.browsed_file = askopenfilename(
            title="Open a file to scrubber",
            filetypes=filetypes
        )
        self.update_file_label(self.browsed_file)
        self.enable_rm_btn()
        self.enable_saveas_btn()
        self.fill_default_output_filename()

    def saveas(self):
        # TODO define better filetypes
        filetypes = [('all files', '.*')]
        self.saveas_file = asksaveasfilename(
            title="Select where to save opened file",
            filetypes=filetypes
        )
        self.update_saveas_label(self.saveas_file)

    def enable_rm_btn(self):
        if self.browsed_file:
            self.rm_btn['state'] = tk.NORMAL

    def enable_saveas_btn(self):
        if self.browsed_file:
            self.saveas_btn['state'] = tk.NORMAL

    def update_file_label(self, text):
        if text:
            self.file_label['text'] = text

    def update_saveas_label(self, text):
        if text:
            self.saveas_label['text'] = text

    def fill_default_output_filename(self):
        if self.browsed_file:
            self.update_saveas_label(
                default_output_filename(self.browsed_file)
            )


def main():
    gui = ScrubberGui()
    gui.display()


if __name__ == "__main__":
    main()
