import pkg_resources  # NOQA  # pragma: no cover
import os  # pragma: no cover
import tkinter as tk  # pragma: no cover
from tkinter.filedialog import (askopenfilename, asksaveasfilename, askdirectory,
                                askopenfilenames)  # pragma: no cover
from tkinter.messagebox import showerror, showinfo  # pragma: no cover

from n2h.metadata_scrubber.scrubber import (remove_metadata,
                                            directory_scrubber,
                                            default_output_filename,
                                            default_output_directory,
                                            )  # pragma: no cover

here = os.path.abspath(os.path.dirname(__file__))  # pragma: no cover


class ScrubberGui:  # pragma: no cover

    def __init__(self):
        self.window = tk.Tk()
        self.window.title = "Metadata scrubber"
        self.window.minsize(width=300, height=300)
        self.display_menu()
        self.window_reset()

    def display(self):
        self.window.mainloop()

    def window_clean(self):
        for grid in self.window.grid_slaves():
            grid.destroy()
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

    def display_default(self):
        tk.Label(self.window, text="No file selected ...") \
            .grid(row=0, column=0, padx=5, pady=5)

    def window_reset(self):
        self.browsed_file = None
        self.browsed_directory = None
        self.window_clean()
        self.display_default()

    def display_menu(self):
        def alert():
            showinfo("Help", "Find documentation on GitHub"
                     "(https://github.com/Nothing2Hide/n2h.metadata_scrubber)")

        menubar = tk.Menu(self.window)

        menu1 = tk.Menu(menubar, tearoff=0)
        menu1.add_command(label="Open file", command=self.command_open_file)
        menu1.add_command(label="Open files", command=self.command_open_files)
        menu1.add_command(label="Open directory",
                          command=self.command_open_directory)
        menubar.add_cascade(label="Files", menu=menu1)

        menu3 = tk.Menu(menubar, tearoff=0)
        menu3.add_command(label="About", command=alert)
        menubar.add_cascade(label="Help", menu=menu3)

        self.window.config(menu=menubar)

    def command_open_directory(self):
        self.browsed_directory = askdirectory(
            title="Open a directory to clean",
        )
        if self.browsed_directory:
            self.display_directory()

    def command_open_files(self):
        # TODO define better filetypes
        filetypes = [('all files', '.*')]
        self.browsed_files = askopenfilenames(
            title="Open a file(s) to clean",
            filetypes=filetypes
        )
        if self.browsed_files:
            self.display_files()

    def command_open_file(self):
        # TODO define better filetypes
        filetypes = [('all files', '.*')]
        self.browsed_file = askopenfilename(
            title="Open a file to clean",
            filetypes=filetypes
        )
        if self.browsed_file:
            self.display_file()

    def display_directory(self):
        self.window_clean()
        self.savein_directory = default_output_directory(self.browsed_directory)

        self.savein_variable = tk.StringVar(self.window, value=self.savein_directory)
        self.savein_entry = tk.Entry(self.window,
                                     textvariable=self.savein_variable)
        self.directory_entry = tk.Entry(
            self.window, state='readonly',
            textvariable=tk.StringVar(self.window,
                                      value=self.browsed_directory)
        )
        self.rm_btn = tk.Button(self.window, text="Clean directory", width=0,
                                command=self.remove_metadata_directory)
        self.savein_btn = tk.Button(self.window, text="Save in",
                                    command=self.savein)

        self.directory_entry.grid(sticky='nwe', padx=5, pady=5)
        self.savein_entry.grid(sticky='nwe', padx=5, pady=5)
        self.savein_btn.grid(sticky='ne', row=1, column=1, padx=5, pady=5)
        self.rm_btn.grid(sticky='sw', row=2, column=0, columnspan=2, padx=5,
                         pady=5)

    def display_file(self):
        self.window_clean()
        self.saveas_file = default_output_filename(self.browsed_file)

        self.saveas_variable = tk.StringVar(self.window, value=self.saveas_file)
        self.saveas_entry = tk.Entry(self.window,
                                     textvariable=self.saveas_variable)
        self.file_entry = tk.Entry(
            self.window, state='readonly',
            textvariable=tk.StringVar(self.window, value=self.browsed_file)
        )
        self.rm_btn = tk.Button(self.window, text="Clean file", width=0,
                                command=self.remove_metadata_file)
        self.saveas_btn = tk.Button(self.window, text="Save as",
                                    command=self.saveas)

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.file_entry.grid(sticky='nwe', padx=5, pady=5)
        self.saveas_entry.grid(sticky='nwe', padx=5, pady=5)
        self.saveas_btn.grid(sticky='ne', row=1, column=1, padx=5, pady=5)
        self.rm_btn.grid(sticky='sw', row=2, column=0, columnspan=2, padx=5,
                         pady=5)

    def display_files(self):
        self.window_clean()
        self.savein_directory = os.path.join(here, 'clean')

        self.savein_variable = tk.StringVar(self.window, value=self.savein_directory)
        self.savein_entry = tk.Entry(self.window,
                                     textvariable=self.savein_variable)
        self.files_list = tk.Listbox(self.window)
        for i, file_ in enumerate(self.browsed_files):
            self.files_list.insert(i, file_)
        self.rm_btn = tk.Button(self.window, text="Clean directory", width=0,
                                command=self.remove_metadata_files)
        self.savein_btn = tk.Button(self.window, text="Save in",
                                    command=self.savein)

        self.files_list.grid(sticky='nwe', padx=5, pady=5)
        self.savein_entry.grid(sticky='nwe', padx=5, pady=5)
        self.savein_btn.grid(sticky='ne', row=1, column=1, padx=5, pady=5)
        self.rm_btn.grid(sticky='sw', row=2, column=0, columnspan=2, padx=5,
                         pady=5)

    def remove_metadata_file(self):
        try:
            remove_metadata(self.browsed_file, self.saveas_variable.get())
        except Exception as error:
            showerror(title="Error", message=str(error))
        else:
            showinfo(title="Success", message="File scrubbed")
            self.window_reset()

    def remove_metadata_files(self):
        for file_ in self.browsed_files:
            path, filename = os.path.split(file_)
            try:
                remove_metadata(file_, os.path.join(self.savein_variable.get(),
                                                    filename))
            except Exception as error:
                showerror(title="Error with %s" % file_, message=str(error))
        showinfo(title="Success", message="Files scrubbed")
        self.window_reset()

    def remove_metadata_directory(self):
        try:
            directory_scrubber(self.browsed_directory,
                               self.savein_variable.get())
        except Exception as error:
            showerror(title="Error", message=str(error))
        else:
            showinfo(title="Success", message="Directory is clean")
            self.window_reset()

    def saveas(self):
        # TODO define better filetypes
        filetypes = [('all files', '.*')]
        self.saveas_file = asksaveasfilename(
            title="Select where to save opened file",
            filetypes=filetypes
        )
        self.saveas_variable.set(self.saveas_file)

    def savein(self):
        self.savein_directory = askdirectory(
            title="Select directory to save clean files",
        )
        self.savein_variable.set(self.savein_directory)


def main():  # pragma: no cover
    gui = ScrubberGui()
    gui.display()


if __name__ == "__main__":  # pragma: no cover
    main()
