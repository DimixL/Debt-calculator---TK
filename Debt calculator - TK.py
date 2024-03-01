import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import datetime


def is_leap_year(year):
    """Проверка на високосный год."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


# Методика подсчёта из второго задания
def calculate_solved_from_ui():
    try:
        debt = float(debt_entry.get())
        currency = currency_combobox.get()
        start_date_str = start_date_entry.get()
        end_date_str = end_date_entry.get()

        exchange_rates = {'RUB': 1, 'USD': 90.42, 'EUR': 98.31}

        if currency not in exchange_rates:
            result_label.config(text="Неизвестная валюта.")
            return

        debt_in_rub = debt * exchange_rates[currency]

        start_date = datetime.datetime.strptime(start_date_str, '%d.%m.%Y')
        end_date = datetime.datetime.strptime(end_date_str, '%d.%m.%Y')

        if start_date < datetime.datetime(2016, 8, 1) or end_date < start_date:
            result_label.config(text="Проверьте введённые даты.")
            return

        interest_rates = {
            (datetime.datetime(2016, 8, 2), datetime.datetime(2016, 9, 18)): 10.50,
            (datetime.datetime(2016, 9, 19), datetime.datetime(2016, 12, 31)): 10.00,
            (datetime.datetime(2017, 1, 1), datetime.datetime(2017, 3, 26)): 10.00,
            (datetime.datetime(2017, 3, 27), datetime.datetime(2017, 5, 1)): 9.75,
            (datetime.datetime(2017, 5, 2), datetime.datetime(2017, 6, 18)): 9.25,
            (datetime.datetime(2017, 6, 19), datetime.datetime(2017, 9, 17)): 9.00,
            (datetime.datetime(2017, 9, 18), datetime.datetime(2017, 10, 29)): 8.50,
            (datetime.datetime(2017, 10, 30), datetime.datetime(2017, 12, 17)): 8.25,
            (datetime.datetime(2017, 12, 18), datetime.datetime(2018, 2, 11)): 7.75,
            (datetime.datetime(2018, 2, 12), datetime.datetime(2018, 3, 25)): 7.50,
            (datetime.datetime(2018, 3, 26), datetime.datetime(2018, 9, 16)): 7.25,
            (datetime.datetime(2018, 9, 17), datetime.datetime(2018, 12, 16)): 7.50,
            (datetime.datetime(2018, 12, 17), datetime.datetime(2019, 6, 16)): 7.75,
            (datetime.datetime(2019, 6, 17), datetime.datetime(2019, 7, 28)): 7.50,
            (datetime.datetime(2019, 7, 29), datetime.datetime(2019, 9, 8)): 7.25,
            (datetime.datetime(2019, 9, 9), datetime.datetime(2019, 10, 27)): 7.00,
            (datetime.datetime(2019, 10, 28), datetime.datetime(2019, 12, 15)): 6.50,
            (datetime.datetime(2019, 12, 16), datetime.datetime(2019, 12, 31)): 6.25,
            (datetime.datetime(2020, 1, 1), datetime.datetime(2020, 2, 9)): 6.25,
            (datetime.datetime(2020, 2, 10), datetime.datetime(2020, 4, 25)): 6.00,
            (datetime.datetime(2020, 4, 26), datetime.datetime(2020, 6, 21)): 5.50,
            (datetime.datetime(2020, 6, 22), datetime.datetime(2020, 7, 26)): 4.50,
            (datetime.datetime(2020, 7, 27), datetime.datetime(2020, 12, 31)): 4.25,
            (datetime.datetime(2021, 1, 1), datetime.datetime(2021, 3, 21)): 4.25,
            (datetime.datetime(2021, 3, 22), datetime.datetime(2021, 4, 25)): 4.50,
            (datetime.datetime(2021, 4, 26), datetime.datetime(2021, 6, 14)): 5.00,
            (datetime.datetime(2021, 6, 15), datetime.datetime(2021, 7, 25)): 5.50,
            (datetime.datetime(2021, 7, 26), datetime.datetime(2021, 9, 12)): 6.50,
            (datetime.datetime(2021, 9, 13), datetime.datetime(2021, 10, 24)): 6.75,
            (datetime.datetime(2021, 10, 25), datetime.datetime(2021, 12, 19)): 7.50,
            (datetime.datetime(2021, 12, 20), datetime.datetime(2022, 2, 13)): 8.50,
            (datetime.datetime(2022, 2, 14), datetime.datetime(2022, 2, 27)): 9.50,
            (datetime.datetime(2022, 2, 28), datetime.datetime(2022, 4, 10)): 20.00,
            (datetime.datetime(2022, 4, 11), datetime.datetime(2022, 5, 3)): 17.00,
            (datetime.datetime(2022, 5, 4), datetime.datetime(2022, 5, 26)): 14.00,
            (datetime.datetime(2022, 5, 27), datetime.datetime(2022, 6, 13)): 11.00,
            (datetime.datetime(2022, 6, 14), datetime.datetime(2022, 7, 24)): 9.50,
            (datetime.datetime(2022, 7, 25), datetime.datetime(2022, 9, 18)): 8.00,
            (datetime.datetime(2022, 9, 19), datetime.datetime(2023, 7, 23)): 7.50,
            (datetime.datetime(2023, 7, 24), datetime.datetime(2023, 8, 14)): 8.50,
            (datetime.datetime(2023, 8, 15), datetime.datetime(2023, 9, 17)): 12.00,
            (datetime.datetime(2023, 9, 18), datetime.datetime(2023, 10, 29)): 13.00,
            (datetime.datetime(2023, 10, 30), datetime.datetime(2023, 12, 17)): 15.00,
            (datetime.datetime(2023, 12, 18), datetime.datetime(2023, 12, 31)): 16.00,
            (datetime.datetime(2024, 1, 1), datetime.datetime(2024, 12, 31)): 16.00,
            (datetime.datetime(2025, 1, 1), datetime.datetime(2199, 12, 31)): 16.00,
        }

        days_count = 0
        total_interest = 0

        for interval, interval_rate in interest_rates.items():
            if end_date < interval[0] or start_date > interval[1]:
                continue

            interval_start = max(start_date, interval[0])
            interval_end = min(end_date, interval[1])
            days_in_interval = (interval_end - interval_start).days + 1

            days_count += days_in_interval
            days_in_year = 366 if is_leap_year(interval_start.year) else 365
            total_interest += (debt_in_rub * interval_rate / 100 * days_in_interval / days_in_year)

        result = f"Сумма процентов (в рублях): {total_interest:.2f}\nОбщее количество дней: {days_count}"
        result_label.config(text=result)
    except ValueError:
        result_label.config(text="Ошибка ввода. Проверьте введенные данные.")


# Создаем главное окно
root = tk.Tk()
root.title("Калькулятор процентов по задолженности")
root.geometry("500x300")

debt_label = tk.Label(root, text="Сумма долга:")
debt_label.pack()

debt_entry = tk.Entry(root)
debt_entry.pack()

currency_label = tk.Label(root, text="Валюта:")
currency_label.pack()

currency_combobox = ttk.Combobox(root, values=['RUB', 'USD', 'EUR'])
currency_combobox.pack()
currency_combobox.set('RUB')

start_date_label = tk.Label(root, text="Дата начала:")
start_date_label.pack()

start_date_entry = DateEntry(root, date_pattern='dd.mm.yyyy')
start_date_entry.pack()

end_date_label = tk.Label(root, text="Дата окончания:")
end_date_label.pack()

end_date_entry = DateEntry(root, date_pattern='dd.mm.yyyy')
end_date_entry.pack()

calculate_button = tk.Button(root, text="Рассчитать", command=calculate_solved_from_ui)
calculate_button.pack()

result_label = tk.Label(root, text="Результат будет отображен здесь")
result_label.pack()

root.mainloop()
