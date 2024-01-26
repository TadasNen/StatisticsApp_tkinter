import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from methods_data_formatting import process_functions
from methods_file_handling import file_read_df, save_as_png, load_readme_content
from methods_general_data import show_general_data_info, show_data_structure


class MainApp(ctk.CTk):
    """
    Initialization of the program, default GUI settings, and frame handling.

    This class represents the main application and is responsible for setting up
    the GUI, managing frames, and controlling frame transitions.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the MainApp.

        Parameters:
        - *args, **kwargs: Additional arguments and keyword arguments.
        """
        # Frame format template and variables to transfer information to specific frames
        ctk.CTk.__init__(self, *args, **kwargs)
        self.title('Excel viewer')
        self.title_font = ctk.CTkFont(family='Arial', size=18, weight="bold", slant="italic")
        self.geometry("500x600")

        # Container frame for holding other frames
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Frame list and their settings
        self.frames = {}
        for FrameClass in (MainMenuFrame, UploadFileFrame, InfoFrame):
            page_name = FrameClass.__name__
            frame = FrameClass(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Calls MainMenuFrame as a default view when the program is initialized from methods_GUI file
        self.show_frame("MainMenuFrame")

    def show_frame(self, page_name):
        """
        Switches to the specified frame.

        Parameters:
        - page_name: The name of the frame to switch to.
        """
        frame = self.frames[page_name]
        frame.tkraise()


class MainMenuFrame(ctk.CTkFrame):
    """
    Initial frame shown when the program is initiated.

    This frame displays the main menu with options to start the program,
    view information, and quit the application.
    """

    def __init__(self, parent, controller):
        """
        Initializes the MainMenuFrame.

        Parameters:
        - parent: The parent widget.
        - controller: The main controller for managing frames and navigation.
        """
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        # Title label
        label = ctk.CTkLabel(self, text="MAIN MENU", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        # Buttons for different options
        button_upload = ctk.CTkButton(self, text="Start program",
                                      font=('Arial', 18),
                                      width=200, height=40,
                                      command=lambda: controller.show_frame("UploadFileFrame"))
        button_info = ctk.CTkButton(self, text="Information",
                                    font=('Arial', 18),
                                    width=200, height=40,
                                    command=lambda: controller.show_frame("InfoFrame"))
        button_quit = ctk.CTkButton(self, text="Quit",
                                    command=self.quit_program)
        button_upload.pack(padx=10, pady=20)
        button_info.pack(padx=10, pady=20)
        button_quit.pack(padx=10, pady=20)

    def quit_program(self):
        """
        Quits the entire program when the "Quit" button is clicked.
        """
        self.controller.destroy()


class UploadFileFrame(ctk.CTkFrame):
    """
    Frame for uploading files and performing various operations on the data.

    This frame allows users to upload files, view general data, clean data,
    and open statistics based on the uploaded data.
    """

    def __init__(self, parent, controller):
        """
        Initializes the UploadFileFrame.

        Parameters:
        - parent: The parent widget.
        - controller: The main controller for managing frames and navigation.
        """
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.df = None

        # Title label
        label = ctk.CTkLabel(self, text="FILE HANDLING OPTIONS", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        # Treeview widget for displaying data structure
        self.tree = ttk.Treeview(self)

        # Buttons for different operations
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

        # Textbox for displaying information
        self.infobox = ctk.CTkTextbox(self)

    def upload_file(self):
        """
        Uploads a file and reads its contents into a DataFrame.
        """
        self.df = file_read_df()

    def show_data_structure(self):
        """
        Displays the data structure in the Treeview.
        """
        show_data_structure(self.tree, self.df)

    def view_general_data(self):
        """
        Opens a window to view general data.
        """
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
        """
        Opens a window to clean the data.
        """
        try:
            if self.df is not None:
                CleanDataWindow(self.controller, self.df)
            else:
                messagebox.showinfo("Info", "Dataframe is not available. Please upload a file first.")
        except Exception as e:
            error_message = f"Error: {e}"
            messagebox.showerror("Error", error_message)

    def open_statistics(self):
        """
        Opens a window to view statistics based on the data.
        """
        try:
            if self.df is not None:
                StatisticsWindow(self.controller, self.df)
            else:
                messagebox.showinfo("Info", "Dataframe is not available. Please upload a file first.")
        except Exception as e:
            error_message = f"Error: {e}"
            messagebox.showerror("Error", error_message)


class GeneralDataWindow(ctk.CTkToplevel):
    """
    Window for displaying general information about a DataFrame.

    This window includes a Treeview widget to show information such as index,
    column names, unique values, and null values for each column.
    """

    def __init__(self, parent, df):
        """
        Initializes the GeneralDataWindow.

        Parameters:
        - parent: The parent widget.
        - df: The DataFrame for which general data is displayed.
        """
        super().__init__()
        self.parent = parent
        self.df = df
        self.title("General Data")
        self.geometry("800x800")

        # Treeview widget for displaying general data information
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
        """
        Displays general data information in the Treeview.
        """
        show_general_data_info(self.tree, self.df)


class CleanDataWindow(ctk.CTkToplevel):
    """
    Window for cleaning data based on user-selected options.

    This window allows users to choose options for cleaning the data, such as
    removing unnecessary columns, renaming columns, calculating distance based
    on coordinates, adjusting values, splitting date and time columns, and
    adding card type and industry columns.
    """

    def __init__(self, parent, df):
        """
        Initializes the CleanDataWindow.

        Parameters:
        - parent: The parent widget.
        - df: The DataFrame to be cleaned.
        """
        super().__init__()
        self.title('Clean data')
        self.geometry("600x800")
        self.df = df
        self.parent = parent

        # Label for instructions
        self.label = ctk.CTkLabel(self, text='Choose options according to which adjust the data')
        self.label.pack(padx=20, pady=20)

        # Start cleaning button
        self.button_start_clean = ctk.CTkButton(self, text='Start process',
                                                command=self.process_functions)

        # Checkboxes for various cleaning options
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
        self.cb_process_values = ctk.CTkCheckBox(self, text='Adjust values',
                                                 variable=self.cb_process_values_var)

        self.cb_split_datetime_var = ctk.BooleanVar()
        self.cb_split_datetime = ctk.CTkCheckBox(self, text='Split date and time column',
                                                 variable=self.cb_split_datetime_var)

        self.cb_card_info_expand_var = ctk.BooleanVar()
        self.cb_card_info_expand = ctk.CTkCheckBox(self, text='Add card type and industry columns',
                                                   variable=self.cb_card_info_expand_var)

        # Pack widgets
        self.cb_remove_columns.pack(padx=20, pady=20)
        self.cb_update_columns.pack(padx=20, pady=20)
        self.cb_distance.pack(padx=20, pady=20)
        self.cb_process_values.pack(padx=20, pady=20)
        self.cb_split_datetime.pack(padx=20, pady=20)
        self.cb_card_info_expand.pack(padx=20, pady=20)
        self.button_start_clean.pack(padx=20, pady=20)

    def process_functions(self):
        """
        Calls the process_functions method to clean the data based on user-selected options.
        """
        process_functions(
            df=self.df,
            cb_process_values=self.cb_process_values_var.get(),
            cb_remove_columns=self.cb_remove_columns_var.get(),
            cb_split_datetime=self.cb_split_datetime_var.get(),
            cb_distance=self.cb_distance_var.get(),
            cb_card_info_expand=self.cb_card_info_expand_var.get(),
            cb_update_columns=self.cb_update_columns_var.get()
        )


class StatisticsWindow(ctk.CTkToplevel):
    """
    Window for displaying statistics options and charts based on user selections.

    This window currently includes a button to open a Gender Pie Chart.
    """

    def __init__(self, parent, df):
        """
        Initializes the StatisticsWindow.

        Parameters:
        - parent: The parent widget.
        - df: The DataFrame for which statistics are displayed.
        """
        super().__init__()
        self.title('Statistics')
        self.geometry("500x300")
        self.df = df
        self.parent = parent

        # Label for statistics window
        self.label = ctk.CTkLabel(self, text='Select which chart should be opened')
        self.label.pack(padx=20, pady=20)

        # Button to open the Gender Pie Chart
        button_open_gender = ctk.CTkButton(self, text="Open Pie Chart", command=self.open_gender_pie_chart)
        button_open_gender.pack(pady=10)

    def open_gender_pie_chart(self):
        """
        Opens a Gender Pie Chart window.
        """
        pie_chart_window = GenderPieChartWindow(self, self.df)
        pie_chart_window.grab_set()
        self.wait_window(pie_chart_window)


class GenderPieChartWindow(ctk.CTkToplevel):
    """
    Window for displaying a Gender Pie Chart based on DataFrame values.
    """

    def __init__(self, parent, df):
        """
        Initializes the GenderPieChartWindow.

        Parameters:
        - parent: The parent widget.
        - df: The DataFrame for which the pie chart is generated.
        """
        super().__init__(parent)
        self.title("Gender Pie Chart")
        self.geometry("800x600")

        # Create Gender Pie Chart
        gender_counts = df['gender'].value_counts()
        labels = gender_counts.index
        sizes = gender_counts.values

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=1)
        ax.axis('equal')

        # Embed the chart in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Button to save the chart as PNG
        button_save = ctk.CTkButton(self, text="Save as PNG", command=save_as_png)
        button_save.pack(pady=10)


class InfoFrame(ctk.CTkFrame):
    """
    Frame for displaying information, including a README file content.
    """

    def __init__(self, parent, controller):
        """
        Initializes the InfoFrame.

        Parameters:
        - parent: The parent widget.
        - controller: The main controller for managing frames and navigation.
        """
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.statistics_text = None

        # Button to navigate back to the main menu
        button_back = ctk.CTkButton(self, text="Back",
                                    font=('Arial', 18),
                                    width=200, height=40,
                                    command=lambda: controller.show_frame("MainMenuFrame"))
        button_back.pack(padx=10, pady=20)

        # Label to display README content
        self.stats_label = ctk.CTkLabel(self, text="", font=('Arial', 14), anchor='w', justify="left")
        self.stats_label.pack(padx=10, pady=5)

        # Load README content from file
        readme_file_path = "README.txt"
        readme_content = self.display_readme_content(readme_file_path)
        self.stats_label.configure(text=readme_content)

    def display_readme_content(self, file_path):
        # Calls function to read readme.txt file and returns the content
        return load_readme_content(file_path)
