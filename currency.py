import requests
import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

API_KEY = "fca_live_BMBawMhIIrPafUIAEAEJ4BCjpfG7vaJxbP3zUC9c"
BASE_URL = "https://api.currencyapi.com/v3/latest"
CURRENCIES = ["USD", "CAD", "EUR", "AUD", "TRY"]

def convert_currency(base):
    currencies = ",".join(CURRENCIES)
    url = f"{BASE_URL}?apikey={API_KEY}&base_currency={base}&currencies={currencies}"
    print(f"Request URL: {url}")  # Hata ayıklama için URL'yi yazdır
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["data"]
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"HTTP Request failed: {e}")
        return None

def get_user_input():
    base_currency = base_currency_entry.get().upper()
    if not base_currency:  # Kullanıcı boş giriş yapmışsa
        messagebox.showerror("Error", "Base currency cannot be empty.")
        return
    if base_currency == "Q":
        root.quit()
    else:
        print(f"Base currency: {base_currency}")  # Hata ayıklama için girdiyi yazdır
        data = convert_currency(base_currency)
        if data:
            # Clear previous results
            for widget in result_frame.winfo_children():
                widget.destroy()
                
            df = pd.DataFrame.from_dict(data, orient='index')
            df = df[['value']]  # Only get the value column
            df.columns = ['Exchange Rate']

            # Create and display table
            table_label = tk.Label(result_frame, text=df.to_string())
            table_label.pack()

            # Create and display plot
            figure = Figure(figsize=(6, 4), dpi=100)
            ax = figure.add_subplot(111)
            df.plot(kind='bar', ax=ax)
            ax.set_title(f'Exchange Rates for {base_currency}')
            ax.set_ylabel('Exchange Rate')
            canvas = FigureCanvasTkAgg(figure, result_frame)
            canvas.get_tk_widget().pack()

root = tk.Tk()
root.title("Currency Converter")

tk.Label(root, text="Please enter the base currency (e.g. USD):").pack()
base_currency_entry = tk.Entry(root)
base_currency_entry.pack()

submit_button = tk.Button(root, text="Submit", command=get_user_input)
submit_button.pack()

result_frame = tk.Frame(root)
result_frame.pack()

root.mainloop()
