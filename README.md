


# Currency Converter

This is a simple currency converter application built with Python. It uses the `currencyapi` to fetch the latest exchange rates and displays the data using Tkinter for the GUI and Matplotlib for plotting the exchange rates.

## Features

- Fetches latest currency exchange rates.
- Supports multiple currencies (USD, CAD, EUR, AUD, TRY).
- Displays exchange rates in a table.
- Plots exchange rates using a bar chart.
- Simple and user-friendly GUI.

## Requirements

- Python 3.x
- `requests` library
- `tkinter` library (usually included with Python installations)
- `matplotlib` library
- `pandas` library

You can install the required libraries using the following command:

```sh
pip install requests matplotlib pandas
```

## Usage

1. Clone this repository:

```sh
git clone https://github.com/your-username/currency-converter.git
cd currency-converter
```

2. Run the application:

```sh
python currency.py
```

3. Enter the base currency (e.g., USD) in the input field and click "Submit". The application will display the exchange rates and plot them in a bar chart.

## Code Explanation

### Importing Libraries

The application imports several libraries for different functionalities:

```python
import requests
import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
```

### Constants

Some constants are defined to be used throughout the application:

```python
API_KEY = "your_api_key_here"
BASE_URL = "https://api.currencyapi.com/v3/latest"
CURRENCIES = ["USD", "CAD", "EUR", "AUD", "TRY"]
```

### `convert_currency` Function

This function takes a base currency as input and fetches the latest exchange rates for the defined currencies:

```python
def convert_currency(base):
    currencies = ",".join(CURRENCIES)
    url = f"{BASE_URL}?apikey={API_KEY}&base_currency={base}&currencies={currencies}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["data"]
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"HTTP Request failed: {e}")
        return None
```

### `get_user_input` Function

This function gets the user input from the Tkinter input field and processes it:

```python
def get_user_input():
    base_currency = base_currency_entry.get().upper()
    if not base_currency:
        messagebox.showerror("Error", "Base currency cannot be empty.")
        return
    if base_currency == "Q":
        root.quit()
    else:
        data = convert_currency(base_currency)
        if data:
            for widget in result_frame.winfo_children():
                widget.destroy()
                
            df = pd.DataFrame.from_dict(data, orient='index')
            df = df[['value']]
            df.columns = ['Exchange Rate']

            table_label = tk.Label(result_frame, text=df.to_string())
            table_label.pack()

            figure = Figure(figsize=(6, 4), dpi=100)
            ax = figure.add_subplot(111)
            df.plot(kind='bar', ax=ax)
            ax.set_title(f'Exchange Rates for {base_currency}')
            ax.set_ylabel('Exchange Rate')
            canvas = FigureCanvasTkAgg(figure, result_frame)
            canvas.get_tk_widget().pack()
```

### Tkinter GUI Setup

The Tkinter GUI is set up with labels, input fields, and buttons:

```python
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
```

## License

This project is licensed under the MIT License.

```

You can customize this README file further based on your specific needs and additional details of your project.
