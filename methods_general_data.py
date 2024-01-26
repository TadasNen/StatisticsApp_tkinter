from tkinter import messagebox
import tkinter as tk


def show_general_data_info(tree, df):
    if df is not None:
        for item in tree.get_children():
            tree.delete(item)
        for idx, col in enumerate(df.columns):
            unique_values_count = df[col].nunique()
            null_values_count = df[col].isnull().sum()
            tree.insert("", idx, values=(idx, col, unique_values_count, null_values_count))
        tree.pack(expand=True, fill="both")
    else:
        messagebox.showinfo("Info", "Dataframe is not available. Please upload a file first.")


def show_data_structure(tree, df):
    if df is not None:
        for item in tree.get_children():
            tree.delete(item)
        headers = df.columns.tolist()
        tree["columns"] = headers
        for header in headers:
            tree.heading(header, text=header)
            tree.column(header, width=100)
        for _, row in df.head().iterrows():
            row_values = [str(value) for value in row]
            tree.insert("", tk.END, values=row_values)
    else:
        messagebox.showinfo("Info", "Dataframe is not available. Please upload a file first.")
