import mysql.connector as mariadb
from config_sql import user, password, host, port, db_name
import re


def sql_connection():
    try:
        mariadb_connection = mariadb.connect(user=user, password=password, host=host, port=port, database=db_name)
        print('Connection is successful')
        print("=" * 64, '\n')
        return mariadb_connection

    except Exception as ex:
        print('Connection refused...\n', ex)


def sql_output_table(table_name):
    mariadb_connection = sql_connection()
    try:
        with mariadb_connection.cursor() as cursor:
            print_table = f"SELECT * FROM {table_name};"
            cursor.execute(print_table)
            rows = cursor.fetchall()
            return rows
    finally:
        mariadb_connection.close()


# def sql_output_code(desired_element, table_name, name_element, code_element):
#     mariadb_connection = sql_connection()
#     try:
#         with mariadb_connection.cursor() as cursor:
#             print_table = f"SELECT {desired_element} FROM {table_name} WHERE {name_element} = {code_element};"
#             cursor.execute(print_table)
#             answer = cursor.fetchall()
#             return answer[0]
#     finally:
#         mariadb_connection.close()


def sql_input_in_table_authors(value_name_author, value_birthday):
    mariadb_connection = sql_connection()
    try:
        with mariadb_connection.cursor(buffered=True) as cursor:
            add_new_string = f"SELECT AddInAuthors('{value_name_author}', '{value_birthday}');"
            cursor.execute(add_new_string)
            mariadb_connection.commit()
        with mariadb_connection.cursor() as cursor:
            counter_string = "SELECT COUNT(Code_author) FROM authors"
            cursor.execute(counter_string)
            answer = cursor.fetchall()
            return answer[0]
    finally:
        mariadb_connection.close()


def sql_input_in_table_books(value_title_book, value_code_author, value_pages, value_code_publish):
    mariadb_connection = sql_connection()
    try:
        with mariadb_connection.cursor(buffered=True) as cursor:
            add_new_string = f"SELECT AddInBooks('{value_title_book}', " \
                                               f"'{value_code_author}', " \
                                               f"'{value_pages}', " \
                                               f"'{value_code_publish}');"
            cursor.execute(add_new_string)
            mariadb_connection.commit()
        with mariadb_connection.cursor() as cursor:
            counter_string = "SELECT COUNT(Code_book) FROM books"
            cursor.execute(counter_string)
            answer = cursor.fetchall()
            return answer[0]
    finally:
        mariadb_connection.close()


def sql_input_in_table_deliveries(value_name_delivery, value_name_company, value_address, value_phone, value_ogrn):
    mariadb_connection = sql_connection()
    try:
        with mariadb_connection.cursor(buffered=True) as cursor:
            add_new_string = f"SELECT AddInDeliveries('{value_name_delivery}', " \
                                                    f"'{value_name_company}', " \
                                                    f"'{value_address}', " \
                                                    f"'{value_phone}', " \
                                                    f"'{value_ogrn}');"
            cursor.execute(add_new_string)
            mariadb_connection.commit()
        with mariadb_connection.cursor() as cursor:
            counter_string = "SELECT COUNT(Code_delivery) FROM deliveries"
            cursor.execute(counter_string)
            answer = cursor.fetchall()
            return answer[0]
    finally:
        mariadb_connection.close()


def sql_input_in_table_publishing_house(value_publish, value_city):
    mariadb_connection = sql_connection()
    try:
        with mariadb_connection.cursor(buffered=True) as cursor:
            add_new_string = f"SELECT AddInPublishingHouse('{value_publish}', '{value_city}');"
            cursor.execute(add_new_string)
            mariadb_connection.commit()
        with mariadb_connection.cursor() as cursor:
            counter_string = "SELECT COUNT(Code_publish) FROM publishing_house"
            cursor.execute(counter_string)
            answer = cursor.fetchall()
            return answer[0]
    finally:
        mariadb_connection.close()


def sql_input_in_table_purchases(value_code_book, value_date_order, value_code_delivery, value_type_purchase,
                                 value_cost, value_amount):
    mariadb_connection = sql_connection()
    try:
        with mariadb_connection.cursor(buffered=True) as cursor:
            add_new_string = f"SELECT AddInPurchases('{value_code_book}', " \
                                                   f"'{value_date_order}', " \
                                                   f"'{value_code_delivery}', " \
                                                   f"'{value_type_purchase}', " \
                                                   f"'{value_cost}', " \
                                                   f"'{value_amount}');"
            cursor.execute(add_new_string)
            mariadb_connection.commit()
        with mariadb_connection.cursor() as cursor:
            counter_string = "SELECT COUNT(Code_purchase) FROM purchases"
            cursor.execute(counter_string)
            answer = cursor.fetchall()
            return answer[0]
    finally:
        mariadb_connection.close()


def sql_output_function(name_function):
    mariadb_connection = sql_connection()
    try:
        with mariadb_connection.cursor() as cursor:
            func = f"SELECT {name_function};"
            cursor.execute(func)
            answer = cursor.fetchall()
            return answer[0]
    finally:
        mariadb_connection.close()


def work_with_string(telegram_string):
    mariadb_connection = sql_connection()
    try:
        with mariadb_connection.cursor() as cursor:
            procedure = f"CALL WorkWithText('{telegram_string}', @letter_a, @letter_v, @letter_i, @letter_p);"
            cursor.execute(procedure)

        with mariadb_connection.cursor() as cursor:
            cursor.execute("SELECT @letter_a")
            count_a_unprocessed = cursor.fetchall()
            count_a = re.sub(r'[(),]', "", str(count_a_unprocessed[0]))

            cursor.execute("SELECT @letter_v")
            count_v_unprocessed = cursor.fetchall()
            count_v = re.sub(r'[(),]', "", str(count_v_unprocessed[0]))

            cursor.execute("SELECT @letter_i")
            count_i_unprocessed = cursor.fetchall()
            count_i = re.sub(r'[(),]', "", str(count_i_unprocessed[0]))

            cursor.execute("SELECT @letter_p")
            count_p_unprocessed = cursor.fetchall()
            count_p = re.sub(r'[(),]', "", str(count_p_unprocessed[0]))

            all_counter = [count_a, count_v, count_i, count_p]
            return all_counter
    finally:
        mariadb_connection.close()


# print(sql_output_code("name_author", "authors", "code_author", 3)[0])
# print(sql_output_code("Name_delivery", "deliveries", "code_delivery", 2))
