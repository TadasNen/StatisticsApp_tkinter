import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from methods import (file_read_df, save_dataframe_to_excel, remove_columns, distance, process_values, split_datetime,
                     card_type_assign, update_column_names)


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

        button_clean_data = ctk.CTkButton(self, text="Clean data",
                                          font=('Arial', 18),
                                          width=200, height=40,
                                          command=self.clean_data)
        button_clean_data.pack(padx=10, pady=5)

        button_statistics_view = ctk.CTkButton(self, text='Statistics',
                                               font=('Arial', 18),
                                               width=200, height=40,
                                               command=self.open_statistics)
        button_statistics_view.pack(padx=10, pady=5)

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

    def clean_data(self):
        try:
            if self.df is not None:
                CleanDataWindow(self.controller, self.df)
            else:
                messagebox.showinfo("Info", "Dataframe is not available. Please upload a file first.")
        except Exception as e:
            error_message = f"Error: {e}"
            messagebox.showerror("Error", error_message)

    def open_statistics(self):
        try:
            if self.df is not None:
                StatisticsWindow(self.controller, self.df)
            else:
                messagebox.showinfo("Info", "Dataframe is not available. Please upload a file first.")
        except Exception as e:
            error_message = f"Error: {e}"
            messagebox.showerror("Error", error_message)


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


class CleanDataWindow(ctk.CTkToplevel):
    def __init__(self, parent, df):
        super().__init__()
        self.title('Clean data')
        self.geometry("600x800")
        self.df = df
        self.parent = parent

        self.label = ctk.CTkLabel(self, text='Choose options according to which adjust the data')
        self.label.pack(padx=20, pady=20)

        self.button_start_clean = ctk.CTkButton(self, text='Start process',
                                                command=self.process_functions)

        self.cb_remove_columns_var = ctk.BooleanVar()
        self.cb_remove_columns = ctk.CTkCheckBox(self, text='Remove unnecessary columns',
                                                 variable=self.cb_remove_columns_var)

        self.cb_update_columns_var = ctk.BooleanVar()
        self.cb_update_columns = ctk.CTkCheckBox(self, text='Rename columns',
                                                 variable=self.cb_update_columns_var)

        self.cb_distance_var = ctk.BooleanVar()
        self.cb_distance = ctk.CTkCheckBox(self, text='Calculate distance based on coordinates',
                                           variable=self.cb_distance_var)

        self.cb_process_values_var = ctk.BooleanVar()
        self.cb_process_values = ctk.CTkCheckBox(self, text='Adjust value of merchants',
                                                 variable=self.cb_process_values_var)

        self.cb_split_datetime_var = ctk.BooleanVar()
        self.cb_split_datetime = ctk.CTkCheckBox(self, text='Split date and time column',
                                                 variable=self.cb_split_datetime_var)

        self.cb_card_info_expand_var = ctk.BooleanVar()
        self.cb_card_info_expand = ctk.CTkCheckBox(self, text='Add card type and industry columns',
                                                   variable=self.cb_card_info_expand_var)

        self.cb_remove_columns.pack(padx=20, pady=20)
        self.label2 = ctk.CTkLabel(self, text='Removes columns not relevant for data')
        self.label2.pack(padx=20, pady=5)
        self.cb_update_columns.pack(padx=20, pady=20)
        self.cb_distance.pack(padx=20, pady=20)
        self.cb_process_values.pack(padx=20, pady=20)
        self.cb_split_datetime.pack(padx=20, pady=20)
        self.cb_card_info_expand.pack(padx=20, pady=20)
        self.button_start_clean.pack(padx=20, pady=20)

    def process_functions(self):
        """
        Carries out relevant function based on choices user made in CleanDataWindow.

        Parameters:
        -self: calls stored dataframe user provided

        :return: None - prompts user to save updated file
        """
        try:
            if self.df is None:
                raise ValueError("DataFrame not uploaded. Please upload a file first.")
            else:
                df = self.df
                if self.cb_process_values_var.get():
                    df = process_values(df)
                if self.cb_remove_columns_var.get():
                    df = remove_columns(df)
                if self.cb_split_datetime_var.get():
                    df = split_datetime(df)
                if self.cb_distance_var.get():
                    df = distance(df)
                if self.cb_card_info_expand_var.get():
                    df = card_type_assign(df)
                if self.cb_update_columns_var.get():
                    df = update_column_names(df)
                save_dataframe_to_excel(df)
        except Exception as e:
            error_message = f'Error: {e}'
            messagebox.showerror(error_message)


class StatisticsWindow(ctk.CTkToplevel):
    def __init__(self, parent, df):
        super().__init__()
        self.title('Statistics')
        self.geometry("600x800")
        self.df = df
        self.parent = parent

        button_open_gender = ctk.CTkButton(self, text="Open Pie Chart", command=self.open_gender_pie_chart)
        button_open_gender.pack(pady=10)

    def open_gender_pie_chart(self):
        pie_chart_window = GenderPieChartWindow(self, self.df)
        pie_chart_window.mainloop()


class GenderPieChartWindow(ctk.CTkToplevel):
    def __init__(self, parent, df):
        super().__init__(parent)
        self.title("Gender Pie Chart")
        self.geometry("800x600")

        gender_counts = df['gender'].value_counts()
        labels = gender_counts.index
        sizes = gender_counts.values

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=1)
        ax.axis('equal')
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        button_save = ctk.CTkButton(self, text="Save as PNG", command=self.save_as_png)
        button_save.pack(pady=10)

    def save_as_png(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            plt.savefig(file_path, format="png")
            messagebox.showinfo("Info", "Pie chart saved as .png")


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

    # def clean_data(self):
    #     try:
    #         if self.df is not None:
    #             updated_df = remove_columns(self.df)
    #             updated_df = distance(updated_df)
    #             updated_df = process_values(updated_df)
    #             updated_df = split_datetime(updated_df)
    #             updated_df = card_type_assign(updated_df)
    #             updated_df = update_column_names(updated_df)
    #             save_dataframe_to_excel(updated_df)
    #         else:
    #             messagebox.showinfo("Info", "Dataframe is not available. Please upload a file first.")
    #
    #     except Exception as e:
    #         error_message = f"Error: {e}"
    #         messagebox.showerror("Error", error_message)
