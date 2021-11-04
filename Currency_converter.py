# Pratiksha Ashok Naik
# Title: Currency Converter


import datetime
import requests
import tkinter as tk
from tkinter import *
from tkinter import ttk


class CurrencyConverter:
    def __init__(self, url):
        self.response_data = requests.get(url).json()
        self.list_currencies = self.response_data['rates']

    def convert_rate(self, from_currency, to_currency, amount):
        if from_currency != 'USD':
            amount = amount / self.list_currencies[from_currency]
        amount = round(amount * self.list_currencies[to_currency], 2)
        return amount


class Application(tk.Tk):
    def __init__(self, converter):
        tk.Tk.__init__(self)
        self.winfo_toplevel().title('Pratiksha Ashok Naik')
        self.geometry("600x350")
        self.configure(bg="#b3cccc")
        # Label
        self.intro_label = Label(self, text=f"Welcome to Currency Convertor \n "
                                            f"{datetime.date.today().strftime('%m-%d-%Y')}",
                                 fg='white', width=50, bg="#5c8a8a",
                                 justify=tk.CENTER, borderwidth=3)
        self.intro_label.config(font=('Manrope', 14, 'bold'))
        self.intro_label.place(x=0, y=5)

        # Entry box
        valid = (self.register(self.restrict_number_only), '%d', '%P')
        self.amount_field = Entry(self, bd=3, width=25, relief=tk.RIDGE, justify=tk.CENTER, validate='key',
                                  bg="#f0f5f5",
                                  validatecommand=valid)
        self.converted_amount_field_label = Label(self, text='', fg='black', relief=tk.RIDGE,
                                                  justify=tk.CENTER, width=23, bg="#f0f5f5", borderwidth=3)

        # dropdown combobox
        self.from_currency_variable = StringVar(self)
        self.from_currency_variable.set("USD")  # default value
        self.to_currency_variable = StringVar(self)
        self.to_currency_variable.set("INR")  # default value

        self.currency_converter = converter
        font = ("Manrope", 12, "bold")
        background = "#f0f5f5"
        selected_item_color = "#5c8a8a"
        self.option_add('*TCombobox*Listbox.font', font)
        self.option_add('*TCombobox*Listbox.background', background)
        self.option_add('*TCombobox*Listbox.selectBackground', selected_item_color)
        self.from_currency_dropdown = ttk.Combobox(self, textvariable=self.from_currency_variable,
                                                   values=list(self.currency_converter.list_currencies.keys()),
                                                   font=font,
                                                   state='readonly', width=15, justify=tk.CENTER)
        self.to_currency_dropdown = ttk.Combobox(self, textvariable=self.to_currency_variable,
                                                 values=list(self.currency_converter.list_currencies.keys()), font=font,
                                                 state='readonly', width=16, justify=tk.CENTER)

        # position
        self.from_currency_dropdown.place(x=40, y=120)
        self.amount_field.place(x=40, y=150)
        self.to_currency_dropdown.place(x=400, y=120)
        self.converted_amount_field_label.place(x=400, y=150)

        # Convert button
        self.convert_button = Button(self, text="Convert", bg="#5c8a8a", width=12, fg="white", command=self.perform)
        self.convert_button.config(font=('Manrope', 12, 'bold'))
        self.convert_button.place(x=235, y=190)

    def perform(self):
        enter_value = self.amount_field.get()
        if enter_value == '':
            # Label
            self.val_label = Label(self, text=f"Please enter the amount...",
                                   relief=tk.GROOVE, borderwidth=2, width=52, bg="#f0f5f5")
            self.val_label.place(x=40, y=250)
            self.val_label.config(font=('Manrope', 12, 'bold'))
            self.converted_amount_field_label.config(text=str(''))
        else:
            amount = float(self.amount_field.get())
            from_curr = self.from_currency_variable.get()
            to_curr = self.to_currency_variable.get()
            converted_amount = self.currency_converter.convert_rate(from_curr, to_curr, amount)
            self.converted_amount_field_label.config(text=str(converted_amount))
            # Label
            self.val_label = Label(self, text=f"{amount} {from_curr}  =  {converted_amount} {to_curr}",
                                   relief=tk.GROOVE, borderwidth=2, width=52, bg="#f0f5f5")
            self.val_label.place(x=40, y=250)
            self.val_label.config(font=('Manrope', 12, 'bold'))

    def restrict_number_only(self, action, string):
        number_only = re.compile(r"[0-9,]*?(\.)?[0-9,]*$")
        result = number_only.match(string)
        return string == "" or (string.count('.') <= 1 and result is not None)


def main():
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = CurrencyConverter(url)
    Application(converter)
    mainloop()


main()


def test_currency_converter_init():
    assert CurrencyConverter('https://api.exchangerate-api.com/v4/latest/USD').response_data['base'] == "USD"


def test_currency_converter_convert_rate():
    converter = CurrencyConverter('https://api.exchangerate-api.com/v4/latest/USD')
    assert converter.convert_rate('USD', 'USD', 10.0) == 10.0

