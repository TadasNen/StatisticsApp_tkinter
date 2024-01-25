"""
File contains functions that are responsible for:
- Uploading files and creating dataframe (file_read_df)
-
"""

import pandas as pd
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt


def file_read_df():
    """
    Reads a file user uploaded and returns a DataFrame. Supported files are in .csv, .ods, .xls, .xlsx formats

    Parameters:
    - None

    Returns:
    - pd.DataFrame: The DataFrame created from the file.
    - Message box with error message
    """
    try:
        # Prompts user to select file in file explorer
        file_path = filedialog.askopenfilename()
        # Conditions of file format acceptance
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
            return df.astype(str)
        elif file_path.endswith(".ods"):
            df = pd.read_excel(file_path, engine='odf')
            return df.astype(str)
        elif file_path.endswith(".xls"):
            df = pd.read_excel(file_path, engine='xlrd')
            return df.astype(str)
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
            return df.astype(str)
        else:
            raise ValueError("File is not supported by the program")
        # Exception handling messagebox
    except Exception as e:
        error_message = f"Error: {e}"
        messagebox.showerror("Error", error_message)
        return None


def df_save_to_excel(df, chunk_size=1000):
    """
    Saves and updated DataFrame to an Excel file in chunks and prompts the user for the save location.

    Parameters:
    - df (pd.DataFrame): The DataFrame to be saved.
    - chunk_size (int): The number of rows to save in each chunk. Default is 1000. Used to reduce time of saving files
    that have large quantity of rows.
    """
    try:
        # Prompt user for save location
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if save_path:
            # Create ExcelWriter
            with pd.ExcelWriter(save_path, engine='xlsxwriter') as writer:
                # Save the DataFrame to .xlsx file in chunks
                for i in range(0, len(df), chunk_size):
                    chunk = df.iloc[i:i + chunk_size]
                    # Check if it's the first chunk and make column names row
                    if i == 0:
                        chunk.to_excel(writer, index=False, sheet_name='Sheet1')
                    else:
                        chunk.to_excel(writer, index=False, sheet_name='Sheet1', header=False, startrow=i)

            messagebox.showinfo("Info", "Dataframe saved as .xlsx successfully.")
    except Exception as e:
        raise e


def save_as_png():
    """
    Prompts user to save image file.

    Parameters:
    - None

    Returns:
    - None
    """
    # Function called in GUI when button to save graph is pressed
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        plt.savefig(file_path, format="png")
        messagebox.showinfo("Info", "Pie chart saved as .png")
