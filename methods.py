import pandas as pd
from tkinter import messagebox, filedialog


def file_read_df(file_path):
    """
    Reads a file user uploaded and returns a DataFrame.

    Parameters:
    - file_path (str): The path to the file.

    Returns:
    - pd.DataFrame: The DataFrame created from the file.
    """
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

def remove_columns(df):
    """
    Removes specified columns from a DataFrame and returns the updated DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame from which columns should be removed.

    Returns:
    - pd.DataFrame: The updated DataFrame.
    """
    columns_to_remove = ['street', 'city', 'state', 'zip', 'city_pop', 'unix_time']
    try:
        updated_df = df.drop(columns=columns_to_remove, errors='ignore')
        return updated_df
    except Exception as e:
        raise e

def update_column_names(df):
    """
    Update sepcific column names of a DataFrame that user uploaded. Works only with base design that was used to
    write a code and resembles financial institution extracted files.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.

    Returns:
    - pd.DataFrame: The DataFrame with updated column names.
    """
    updated_df = df.rename(columns=lambda x: x.lower().replace(' ', '_'))
    return updated_df

def save_dataframe_to_excel(df, chunk_size=1000):
    """
    Saves and updated DataFrame to an Excel file in chunks and prompts the user for the save location.

    Parameters:
    - df (pd.DataFrame): The DataFrame to be saved.
    - chunk_size (int): The number of rows to save in each chunk. Default is 1000. Used to reduce time of saving files
    that have large quantity of rows
    """
    try:
        # Prompt user for save location
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if save_path:
            # Save the DataFrame to .xlsx file in chunks
            for i in range(0, len(df), chunk_size):
                chunk = df.iloc[i:i + chunk_size]
                chunk.to_excel(save_path, index=False, engine='xlsxwriter')
            messagebox.showinfo("Info", "Dataframe saved as .xlsx successfully.")
    except Exception as e:
        raise e