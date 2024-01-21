import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from methods import file_read_df
from tkinter import messagebox
from tkinter import ttk


class MainApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.title('Excel viewer')
        self.title_font = ctk.CTkFont(family='Arial', size=18, weight="bold", slant="italic")
        self.geometry("500x800")
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for FrameClass in (MainMenuFrame, UploadFileFrame, InfoFrame):
            page_name = FrameClass.__name__
            frame = FrameClass(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenuFrame")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class MainMenuFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="MAIN MENU", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button_upload = ctk.CTkButton(self, text="Start program",
                                      font=('Arial', 18),
                                      width=200, height=40,
                                      command=lambda: controller.show_frame("UploadFileFrame"))
        button_info = ctk.CTkButton(self, text="Information",
                                    command=lambda: controller.show_frame("InfoFrame"))
        button_quit = ctk.CTkButton(self, text="Quit",
                                    command=self.quit_program)
        button_upload.pack(padx=10, pady=20)
        button_info.pack(padx=10, pady=20)
        button_quit.pack(padx=10, pady=20)

    def quit_program(self):
        self.controller.destroy()


class UploadFileFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.df = None

        self.tree = ttk.Treeview(self)

        button_upload = ctk.CTkButton(self, text="Upload your file",
                                      font=('Arial', 18),
                                      width=200, height=40,
                                      command=self.upload_file)
        button_upload.pack(padx=10, pady=5)

        button_view_data = ctk.CTkButton(self, text="View general data",
                                         font=('Arial', 18),
                                         width=200, height=40,
                                         command=self.view_general_data)
        button_view_data.pack(padx=10, pady=5)

        button_placeholder_3 = ctk.CTkButton(self, text="Placeholder Button 3",
                                             font=('Arial', 18),
                                             width=200, height=40,
                                             command=self.placeholder_method_3)
        button_placeholder_3.pack(padx=10, pady=5)

        button_back = ctk.CTkButton(self, text="Back",
                                    font=('Arial', 18),
                                    width=200, height=40,
                                    command=lambda: controller.show_frame("MainMenuFrame"))
        button_back.pack(padx=10, pady=20)

        self.infobox = ctk.CTkTextbox(self)

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        try:
            self.df = file_read_df(file_path)
            self.show_data_structure()
        except Exception as e:
            error_message = f"Error: {e}"
            messagebox.showerror("Error", error_message)

    def show_data_structure(self):
        if self.df is not None:
            for item in self.tree.get_children():
                self.tree.delete(item)
            headers = self.df.columns.tolist()
            self.tree["columns"] = headers
            for header in headers:
                self.tree.heading(header, text=header)
                self.tree.column(header, width=100)
            for _, row in self.df.head().iterrows():
                row_values = [str(value) for value in row]
                self.tree.insert("", tk.END, values=row_values)
        else:
            messagebox.showinfo("Info", "Dataframe is not available. Please upload a file first.")

    def view_general_data(self):
        try:
            if self.df is not None:
                general_data_window = GeneralDataWindow(self.controller, self.df)
                general_data_window.show_general_data_info()
            else:
                messagebox.showinfo("Info", "Dataframe is not available. Please upload a file first.")
        except Exception as e:
            error_message = f"Error: {e}"
            messagebox.showerror("Error", error_message)

    def placeholder_method_3(self):
        pass


class GeneralDataWindow(ctk.CTkToplevel):
    def __init__(self, parent, df):
        super().__init__()
        self.parent = parent
        self.df = df
        self.title("General Data")
        self.geometry("800x800")

        self.tree = ttk.Treeview(self)
        self.tree["columns"] = ("Index", "Column Names", "Unique Values", "Null Values")
        self.tree.heading("Index", text="Index")
        self.tree.heading("Column Names", text="Column Names")
        self.tree.heading("Unique Values", text="Unique Values")
        self.tree.heading("Null Values", text="Null Values")
        self.tree.column("Index", width=50)
        self.tree.column("Column Names", width=200)
        self.tree.column("Unique Values", width=200)
        self.tree.column("Null Values", width=200)

    def show_general_data_info(self):
        if self.df is not None:
            for item in self.tree.get_children():
                self.tree.delete(item)
            for idx, col in enumerate(self.df.columns):
                unique_values_count = self.df[col].nunique()
                null_values_count = self.df[col].isnull().sum()
                self.tree.insert("", idx, values=(idx, col, unique_values_count, null_values_count))
            self.tree.pack(expand=True, fill="both")
        else:
            messagebox.showinfo("Info", "Dataframe is not available. Please upload a file first.")


class InfoFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.statistics_text = None

        button_back = ctk.CTkButton(self, text="Back",
                                    font=('Arial', 18),
                                    width=200, height=40,
                                    command=lambda: controller.show_frame("MainMenuFrame"))
        button_back.pack(padx=10, pady=20)

        self.stats_label = ctk.CTkLabel(self, text="", font=('Arial', 14))
        self.stats_label.pack(padx=10, pady=5)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
