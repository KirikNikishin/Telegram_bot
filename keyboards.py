from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_table_output = KeyboardButton('Вывод данных из таблицы')
button_table_input = KeyboardButton('Ввод данных в таблицу')
button_choice_function = KeyboardButton('Выбор функции')
button_help = KeyboardButton('/help')

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_table_output,
                                                                                 button_table_input,
                                                                                 button_choice_function,
                                                                                 button_help)

button_with_code = KeyboardButton('С кодами')
button_without_code = KeyboardButton('Без кодов')

check_output_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_with_code,
                                                                button_without_code)

button_table_authors = KeyboardButton('authors')
button_table_books = KeyboardButton('books')
button_table_deliveries = KeyboardButton('deliveries')
button_table_publishing_house = KeyboardButton('publishing_house')
button_table_purchases = KeyboardButton('purchases')

output_table_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_table_authors,
                                                                button_table_books,
                                                                button_table_deliveries,
                                                                button_table_publishing_house,
                                                                button_table_purchases)

button_func_FindAvg = KeyboardButton('max_purchases()')
button_func_FindSum = KeyboardButton('Suum_cost()')

functions_table_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_func_FindAvg,
                                                                   button_func_FindSum)
