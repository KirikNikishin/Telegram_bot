import time
import datetime
import logging
import re
import random

import mysql

import aiogram
from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.utils.markdown import text, italic, code, hcode
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

from emoji import emojize
import tabulate

import keyboards as kb
from config_bot import TOKEN
import sql_queries as sq


funny_counter = 0

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


class UserState(StatesGroup):
    waiting_user_string = State()


class UserStringState(StatesGroup):
    user_string_for_count = State()


class Aggressive(StatesGroup):
    first_warning = State()


class Output(StatesGroup):
    check_flag_code = State()


def write_log(message, name_function):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} | {user_full_name=} | {name_function=} | {message.text=} | {time.asctime()}')
    return 0


def output_authors(rows):
    data = [['code', 'name_surname', 'birthday']]

    for row_unprocessed in rows:
        counter = row_unprocessed[0]
        name = row_unprocessed[1]
        birthday = str(row_unprocessed[2])
        list_for_insert = [counter, name, birthday]
        data.insert(counter, list_for_insert)
    rows_message = '<pre>' + tabulate.tabulate(data) + '</pre>'
    return rows_message


def output_books(rows):
    data = [['code', 'title', 'code_author', 'pages', 'code_publish']]

    for row_unprocessed in rows:
        counter = row_unprocessed[0]
        title = row_unprocessed[1]
        code_author = row_unprocessed[2]
        pages = row_unprocessed[3]
        code_publish = row_unprocessed[4]
        list_for_insert = [counter, title, code_author, pages, code_publish]
        data.insert(counter, list_for_insert)
    rows_message = '<pre>' + tabulate.tabulate(data) + '</pre>'
    return rows_message


def help_output_books(rows):
    data = [['code', 'title', 'name_author', 'pages', 'code_publish']]

    for row_unprocessed in rows:
        counter = row_unprocessed[0]
        title = row_unprocessed[1]
        code_author = row_unprocessed[2]
        name_author_unprocessed = sq.sql_output_code("name_author", "authors", "code_author", int(code_author))
        name_author = name_author_unprocessed[0]

        pages = row_unprocessed[3]
        code_publish = row_unprocessed[4]
        list_for_insert = [counter, title, name_author, pages, code_publish]
        data.insert(counter, list_for_insert)
    rows_message = '<pre>' + tabulate.tabulate(data) + '</pre>'
    return rows_message


def output_deliveries(rows):
    data = [['code', 'delivery', 'company', 'address', 'phone', 'OGRN']]

    for row_unprocessed in rows:
        counter = row_unprocessed[0]
        delivery = row_unprocessed[1]
        company = row_unprocessed[2]
        address = row_unprocessed[3]
        phone = row_unprocessed[4]
        ogrn = row_unprocessed[5]
        list_for_insert = [counter, delivery, company, address, phone, ogrn]
        data.insert(counter, list_for_insert)
    rows_message = '<pre>' + tabulate.tabulate(data) + '</pre>'
    return rows_message


def output_publishing_house(rows):
    data = [['code', 'publishing_house', 'city']]

    for row_unprocessed in rows:
        counter = row_unprocessed[0]
        publishing_house = row_unprocessed[1]
        city = row_unprocessed[2]

        list_for_insert = [counter, publishing_house, city]
        data.insert(counter, list_for_insert)
    rows_message = '<pre>' + tabulate.tabulate(data) + '</pre>'
    return rows_message


def output_purchases(rows):
    data = [['code', 'code_book', 'date_order', 'code_delivery', 'purchase', 'cost', 'amount']]

    for row_unprocessed in rows:
        counter = row_unprocessed[0]
        code_book = row_unprocessed[1]
        date_order = row_unprocessed[2]
        code_delivery = row_unprocessed[3]
        purchase = row_unprocessed[4]
        cost = row_unprocessed[5]
        amount = row_unprocessed[6]

        list_for_insert = [counter, code_book, date_order, code_delivery, purchase, cost, amount]
        data.insert(counter, list_for_insert)
    rows_message = '<pre>' + tabulate.tabulate(data) + '</pre>'
    return rows_message


def help_output_purchases(rows):
    data = [['code', 'name_book', 'date_order', 'name_delivery', 'purchase', 'cost', 'amount']]

    for row_unprocessed in rows:
        counter = row_unprocessed[0]
        code_book = row_unprocessed[1]

        name_book_unprocessed = sq.sql_output_code("title_book", "books", "code_book", int(code_book))
        name_book = name_book_unprocessed[0]

        date_order = row_unprocessed[2]
        code_delivery = row_unprocessed[3]

        name_delivery_unprocessed = sq.sql_output_code("Name_delivery", "deliveries", "code_delivery", int(code_delivery))
        name_delivery = name_delivery_unprocessed[0]

        purchase = row_unprocessed[4]
        cost = row_unprocessed[5]
        amount = row_unprocessed[6]

        list_for_insert = [counter, code_book, date_order, name_delivery, purchase, cost, amount]
        data.insert(counter, list_for_insert)
    rows_message = '<pre>' + tabulate.tabulate(data) + '</pre>'
    return rows_message


flag = ''
flag_table = ''
name_table = ''
user_check = ''


@dp.message_handler(commands=['start'], state="*")
async def start_handler(message: types.Message, state: FSMContext):
    name_function = 'start'
    write_log(message, name_function)

    await state.finish()
    user_full_name = message.from_user.full_name

    await message.reply(f"Привет, {user_full_name}!"
                        f"\n Выберите желаемую функцию", reply_markup=kb.greet_kb)


@dp.message_handler(commands=['back'], state="*")
async def back_handler(message: types.Message, state: FSMContext):
    name_function = 'back'
    write_log(message, name_function)

    await state.finish()

    await message.reply("Выберите желаемую функцию", reply_markup=kb.greet_kb)


@dp.message_handler(commands=['help'], state="*")
async def process_help_command(message: types.Message, state: FSMContext):
    name_function = 'help'
    write_log(message, name_function)

    await state.finish()

    await message.reply("Удачи!",
                        reply_markup=kb.greet_kb)


@dp.message_handler(commands="cancel", state="*")
async def cancel_get_user_string(message: types.Message, state: FSMContext):
    name_function = 'cancel'
    write_log(message, name_function)

    await state.finish()

    await bot.send_message(message.chat.id, "Действие отменено")
    await message.answer("Выберите желаемую функцию", reply_markup=kb.greet_kb)


@dp.message_handler(filters.Text("Ввод данных в таблицу"), state="*")
async def process_input_table_db(message: types.Message, state: FSMContext):
    global flag
    name_function = 'input_table'
    write_log(message, name_function)

    await state.finish()
    flag = 'input'

    await message.reply("Выберите таблицу для ввода (для возврата используйте /back)",
                        reply_markup=kb.output_table_kb)


@dp.message_handler(filters.Text("Вывод данных из таблицы"), state="*")
async def process_output_table_db(message: types.Message, state: FSMContext):
    global flag
    name_function = 'output'
    write_log(message, name_function)

    await state.finish()
    flag = 'output'

    # await message.reply("Выберите формат вывода данных", reply_markup=kb.check_output_kb)
    await message.reply("Выберите таблицу для вывода (для возврата используйте /back)",
                        reply_markup=kb.output_table_kb)


@dp.message_handler(filters.Text(["authors", "books", "deliveries", "publishing_house", "purchases"]), state="*")
async def process_select_table(message: types.Message, state: FSMContext):
    global name_table
    name_function = 'select_table'
    write_log(message, name_function)

    await state.finish()
    name_table = message.text

    if flag == 'input':
        if name_table == "authors":
            message_text = text('Введите данные для добавления в таблицу в формате\n',
                                hcode('name_surname date_birthday(YYYY-MM-DD)'), '\n\n',
                                'Для отмены действия - команда /cancel')
            await bot.send_message(message.from_user.id, message_text, parse_mode="HTML",
                                   reply_markup=types.ReplyKeyboardRemove())
            await UserState.waiting_user_string.set()

        if name_table == "books":
            rows_authors = sq.sql_output_table('authors')
            rows_message_authors = output_authors(rows_authors)

            rows_publish = sq.sql_output_table('publishing_house')
            rows_message_publish = output_publishing_house(rows_publish)

            await bot.send_message(message.from_user.id, "Вспомогательные таблицы\nAuthors\n" + rows_message_authors,
                                   parse_mode='HTML')
            await bot.send_message(message.from_user.id, "publishing_house\n" + rows_message_publish, parse_mode='HTML')

            message_text = text('Введите данные для добавления в таблицу в формате\n',
                                hcode('title_book code_author pages code_publish'), '\n\n',
                                hcode('code_author'), 'и',
                                hcode('code_publish'), '\n\n\n',
                                'Для отмены действия - команда /cancel')
            await bot.send_message(message.from_user.id, message_text, parse_mode="HTML",
                                   reply_markup=types.ReplyKeyboardRemove())
            await UserState.waiting_user_string.set()

        if name_table == "deliveries":
            message_text = text('Введите данные для добавления в таблицу в формате\n',
                                hcode('name_delivery name_company address phone OGRN'), '\n\n',
                                'Для отмены действия - команда /cancel')
            await bot.send_message(message.from_user.id, message_text, parse_mode="HTML",
                                   reply_markup=types.ReplyKeyboardRemove())
            await UserState.waiting_user_string.set()

        if name_table == "publishing_house":
            message_text = text('Введите данные для добавления в таблицу в формате\n',
                                hcode('publishing_house city'), '\n\n',
                                'Для отмены действия - команда /cancel')
            await bot.send_message(message.from_user.id, message_text, parse_mode="HTML",
                                   reply_markup=types.ReplyKeyboardRemove())
            await UserState.waiting_user_string.set()

        if name_table == "purchases":
            rows_books = sq.sql_output_table('books')
            rows_message_books = output_books(rows_books)

            rows_deliveries = sq.sql_output_table('deliveries')
            rows_message_deliveries = output_deliveries(rows_deliveries)

            await bot.send_message(message.from_user.id, "Вспомогательные таблицы\nBooks\n" + rows_message_books,
                                   parse_mode='HTML')
            await bot.send_message(message.from_user.id, "deliveries\n" + rows_message_deliveries, parse_mode='HTML')

            message_text = text('Введите данные для добавления в таблицу в формате\n',
                                hcode('code_book date_order(YYYY-MM-DD), code_delivery type_purchase, cost, amount\n'),
                                '\n\n',
                                hcode('code_book'), 'и',
                                hcode('code_delivery'), '\n\n\n',
                                'Для отмены действия - команда /cancel')
            await bot.send_message(message.from_user.id, message_text, parse_mode="HTML",
                                   reply_markup=types.ReplyKeyboardRemove())
            await UserState.waiting_user_string.set()

    if flag == 'output':
        rows = sq.sql_output_table(name_table)

        if name_table == "authors":
            rows_message = output_authors(rows)

        if name_table == "books":
            rows_message = output_books(rows)

        if name_table == "deliveries":
            rows_message = output_deliveries(rows)

        if name_table == "publishing_house":
            rows_message = output_publishing_house(rows)

        if name_table == "purchases":
            rows_message = output_purchases(rows)

        await state.finish()

        await bot.send_message(message.from_user.id, rows_message, parse_mode='HTML', reply_markup=kb.greet_kb)


@dp.message_handler(state=UserState.waiting_user_string)
async def get_user_string(message: types.Message, state: FSMContext):
    name_function = 'string_for_table'
    write_log(message, name_function)

    if re.search('[а-яА-ЯЁё]', message.text):

        await message.answer("Пожалуйста, введите данные для добавления в таблицу на английском языке!"
                             "\n\nДля отмены действия - команда /cancel")
        return

    if name_table == "authors":  # name_surname YYYY-MM-DD
        try:
            list_string = message.text.split()
            date = datetime.datetime.strptime(list_string[1], '%Y-%m-%d')
            value_birthday = str(date.date())
        except ValueError:

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return
        except IndexError:

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return
        pattern = '[a-zA-Z]*_[a-zA-Z]*'
        if not re.fullmatch(pattern, list_string[0]):

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return
        value_name_author = list_string[0]
        try:
            answer_unprocessed = str(sq.sql_input_in_table_authors(value_name_author, value_birthday))
        except mysql.connector.errors.DataError:

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return

    if name_table == "books":  # title_book code_author pages code_publish
        try:
            list_string = message.text.split()
            title_book = list_string[0]
            code_author = int(list_string[1])
            pages = int(list_string[2])
            code_publish = int(list_string[3])
        except ValueError:

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return
        except IndexError:

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return
        try:
            answer_unprocessed = str(sq.sql_input_in_table_books(title_book, code_author, pages, code_publish))
        except mysql.connector.errors.DataError:

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return

    if name_table == "deliveries":  # name_delivery name_company address phone OGRN
        try:
            list_string = message.text.split()
            name_delivery = list_string[0]
            name_company = list_string[1]
            address = list_string[2]
            phone = int(list_string[3])
            ogrn = int(list_string[4])
        except ValueError:

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return
        except IndexError:

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return
        try:
            answer_unprocessed = str(sq.sql_input_in_table_deliveries(name_delivery, name_company,
                                                                      address, phone, ogrn))
        except mysql.connector.errors.DataError:

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return

    if name_table == "publishing_house":  # publishing_house city
        try:
            list_string = message.text.split()
            publishing_house = list_string[0]
            city = list_string[1]
        except IndexError:

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return
        try:
            answer_unprocessed = str(sq.sql_input_in_table_publishing_house(publishing_house, city))
        except mysql.connector.errors.DataError:

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return

    if name_table == "purchases":  # code_book date_order, code_delivery type_purchase, cost, amount
        try:
            list_string = message.text.split()
            code_book = int(list_string[0])
            date = datetime.datetime.strptime(list_string[1], '%Y-%m-%d')
            date_order = str(date.date())
            code_delivery = int(list_string[2])
            type_purchase = int(list_string[3])
            cost = float(list_string[4])
            amount = float(list_string[5])
        except ValueError:

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return
        except IndexError:

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return
        try:
            answer_unprocessed = str(sq.sql_input_in_table_purchases(code_book, date_order, code_delivery,
                                                                     type_purchase, cost, amount))
        except mysql.connector.errors.DataError:

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return

    await state.update_data(user_string=message.text)
    data = await state.get_data()
    answer = re.sub(r'[(),]', "", answer_unprocessed)

    await message.answer(f"Ваша строка \"{data['user_string']}\" успешна занесена в базу данных на {answer} позицию",
                         reply_markup=kb.greet_kb)

    rows = sq.sql_output_table(name_table)
    if name_table == "authors":
        await bot.send_message(message.from_user.id, output_authors(rows), parse_mode='HTML')
    if name_table == "books":
        await bot.send_message(message.from_user.id, help_output_books(rows), parse_mode='HTML')
    if name_table == "deliveries":
        await bot.send_message(message.from_user.id, output_deliveries(rows), parse_mode='HTML')
    if name_table == "publishing_house":
        await bot.send_message(message.from_user.id, output_publishing_house(rows), parse_mode='HTML')
    if name_table == "purchases":
        await bot.send_message(message.from_user.id, help_output_purchases(rows), parse_mode='HTML')

    await state.finish()


@dp.message_handler(filters.Text("Выбор функции"), state="*")
async def process_select_function(message: types.Message, state: FSMContext):
    name_function = 'select_function'
    write_log(message, name_function)

    await state.finish()

    await message.reply("Выберите функцию (для возврата используйте /back)", reply_markup=kb.functions_table_kb)


@dp.message_handler(filters.Text(["max_purchases()", "Suum_cost()"]), state="*")
async def process_function_execution(message: types.Message, state: FSMContext):
    name_function = 'execution_function'
    write_log(message, name_function)

    await state.finish()
    name_function = message.text
    answer_unprocessed = str(sq.sql_output_function(name_function))
    answer = re.sub(r'[(),]', "", answer_unprocessed)

    if name_function == "max_purchases()":
        answer_message = f"Функция: {name_function}" \
                         f"\nРезультат:" \
                         f"\n    Максимум = {answer}"

    elif name_function == "Suum_cost()":
        answer_message = f"Функция: {name_function}" \
                         f"\nРезультат:" \
                         f"\n    Cумма закупок = {answer}"

    await bot.send_message(message.from_user.id, answer_message, reply_markup=kb.greet_kb)


@dp.message_handler(content_types=types.ContentType.ANY)
async def unknown_message(message: types.Message):
    name_function = 'unknown_message'
    write_log(message, name_function)

    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    message_text = text(('\nНекорректный ввод'))
    logging.info(f'{user_id=} | {user_full_name=} | {message.text=} | {time.asctime()}')
    await message.reply(message_text, parse_mode=types.ParseMode.MARKDOWN, reply_markup=kb.greet_kb)

    await Aggressive.first_warning.set()


if __name__ == '__main__':
    executor.start_polling(dp)
