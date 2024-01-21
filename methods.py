import pandas as pd
from tkinter import messagebox


def file_read_df(file_path):
    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".ods"):
            df = pd.read_excel(file_path, engine='odf')
        elif file_path.endswith(".xls"):
            df = pd.read_excel(file_path, engine='xlrd')
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("File is not supported by the program")
        df = df.astype(str)

        return df
    except Exception as e:
        error_message = f"Error: {e}"
        messagebox.showerror("Error", error_message)
        return None
