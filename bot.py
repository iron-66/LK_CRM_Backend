import os
import psycopg2
import re
from dotenv import load_dotenv
from telebot import TeleBot
from telebot.apihelper import ApiException
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = TeleBot(TOKEN)
user_data = {}


def save_to_database(user_data, user_id):
    try:
        connection = psycopg2.connect(
            user="uztawibl",
            password="HralYemzEzC9p7go8wLzWpmDvfgY0Zga",
            host="cornelius.db.elephantsql.com",
            port="5432",
            database="uztawibl"
        )
        cursor = connection.cursor()
        sql_query = """
            INSERT INTO public."API_student" (full_name, course, university, speciality, degree, telegram, phone, vk, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        data = (
            user_data['full_name'],
            user_data['course'],
            user_data['university'],
            user_data['speciality'],
            user_data['degree'],
            user_id,
            user_data['phone'],
            user_data['vk'],
            user_data['email']
        )

        cursor.execute(sql_query, data)
        connection.commit()

        print("Данные успешно добавлены в базу данных!")

    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с базой данных:", error)

    finally:
        if connection:
            cursor.close()
            connection.close()


def check_student_exists(full_name):
    try:
        connection = psycopg2.connect(
            user="uztawibl",
            password="HralYemzEzC9p7go8wLzWpmDvfgY0Zga",
            host="cornelius.db.elephantsql.com",
            port="5432",
            database="uztawibl"
        )

        cursor = connection.cursor()
        sql_query = "SELECT 1 FROM public.\"API_student\" WHERE full_name = %s"
        cursor.execute(sql_query, (full_name,))
        return cursor.fetchone() is not None

    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с базой данных:", error)
        return False

    finally:
        if connection:
            cursor.close()
            connection.close()


class States:
    START = "start"
    ASK_NAME = "ask_name"
    ASK_COURSE = "ask_course"
    ASK_UNIVERSITY = "ask_university"
    ASK_SPECIALITY = "ask_speciality"
    ASK_DEGREE = "ask_degree"
    ASK_PHONE = "ask_phone"
    ASK_VK = "ask_vk"
    ASK_EMAIL = "ask_email"
    FINISHED = "finished"


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_data[user_id] = {}
    banner = open('Banner.png', 'rb')
    bot.send_photo(user_id, banner, caption='Здравствуйте!\n\n'
                            'Вы перешли к анкетированию для записи на стажировку в Uralintern. Для сбора персональных данных с Вами будет проведено анкетирование по следующим пунктам:\n\n'
                            '1. ФИО\n'
                            '2. Курс\n'
                            '3. Учебное заведение\n'
                            '4. Специальность / направление\n'
                            '5. Академическая степень\n'
                            '6. Номер телефона\n'
                            '7. Ссылка на VK\n'
                            '8. Адрес электронной почты')
    ask_name(message)


@bot.callback_query_handler(func=lambda message: message.data == "reenter_data")
def reenter_data(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Пожалуйста, введите ваше ФИО:')
    bot.register_next_step_handler_by_chat_id(user_id, ask_course)


def ask_name(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Представьтесь, пожалуйста. Напишите Ваше ФИО')
    bot.register_next_step_handler(message, ask_course)


def ask_course(message):
    user_id = message.from_user.id
    user_data[user_id]['full_name'] = message.text
    name = message.text.split()

    if len(name) < 3 or not all(word.isalpha() for word in name) or not all(2 <= len(part) <= 20 for part in name):
        bot.send_message(user_id, 'Пожалуйста, укажите ФИО в корректном формате\n(пример: Иванов Иван Иванович)')
        bot.register_next_step_handler(message, ask_course)
        return

    if check_student_exists(message.text):
        markup = InlineKeyboardMarkup()
        button = InlineKeyboardButton("Ввести другие данные", callback_data="reenter_data")
        markup.add(button)
        bot.send_message(user_id, 'Такой студент уже подавал заявку. Нажмите на кнопку ниже, если хотите указать другие данные', reply_markup=markup)
        return

    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    buttons = [KeyboardButton(str(i)) for i in range(1, 6)]
    markup.add(*buttons)

    bot.send_message(user_id, f'Отлично, {name[1]}, теперь укажите, на каком курсе Вы учитесь', reply_markup=markup)
    bot.register_next_step_handler(message, ask_university)


def ask_university(message):
    user_id = message.from_user.id
    user_data[user_id]['course'] = message.text

    if not message.text.isdigit() or not (1 <= int(message.text) <= 5):
        bot.send_message(user_id, 'Пожалуйста, укажите курс в диапазоне от 1 до 5')
        bot.register_next_step_handler(message, ask_university)
        return

    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [KeyboardButton("УрФУ"), KeyboardButton("Указать другой университет")]
    markup.add(*buttons)

    bot.send_message(user_id, 'Теперь укажите своё учебное заведение', reply_markup=markup)
    bot.register_next_step_handler(message, check_university)


def check_university(message):
    user_id = message.from_user.id
    if message.text == "Указать другой университет":
        markup = ReplyKeyboardRemove()
        bot.send_message(user_id, 'Напишите название своего учебного заведения', reply_markup=markup)
        bot.register_next_step_handler(message, ask_speciality)
    else:
        ask_speciality(message)


def ask_speciality(message):
    user_id = message.from_user.id
    user_data[user_id]['university'] = message.text

    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    buttons = [KeyboardButton("Программная инженерия"), KeyboardButton("Информатика и вычислительная техника"),
               KeyboardButton("Прикладная информатика"), KeyboardButton("Указать другую специальность")]
    markup.add(*buttons)

    bot.send_message(user_id, 'Укажите свою специальность / направление', reply_markup=markup)
    bot.register_next_step_handler(message, check_speciality)


def check_speciality(message):
    user_id = message.from_user.id
    if message.text == "Указать другую специальность":
        markup = ReplyKeyboardRemove()
        bot.send_message(user_id, 'Напишите название своей специальности', reply_markup=markup)
        bot.register_next_step_handler(message, ask_degree)
    else:
        ask_degree(message)


def ask_degree(message):
    user_id = message.from_user.id
    user_data[user_id]['speciality'] = message.text

    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    buttons = [KeyboardButton("Бакалавриат"), KeyboardButton("Специалитет"), KeyboardButton("Магистратура")]
    markup.add(*buttons)

    bot.send_message(user_id, 'Укажите свою академическую степень', reply_markup=markup)
    bot.register_next_step_handler(message, ask_phone)


def ask_phone(message):
    user_id = message.from_user.id
    user_data[user_id]['degree'] = message.text
    markup = ReplyKeyboardRemove()
    bot.send_message(user_id, 'Укажите номер своего телефона (В формате 89XXXXXXXXX)', reply_markup=markup)
    bot.register_next_step_handler(message, ask_vk)


def ask_vk(message):
    user_id = message.from_user.id
    user_data[user_id]['phone'] = message.text
    if len(message.text) != 11 or not message.text.isdigit():
        bot.send_message(user_id,
                         'Пожалуйста, укажите корректный номер телефона, состоящий из 11 цифр (например, 89123456789)')
        bot.register_next_step_handler(message, ask_vk)
        return
    bot.send_message(user_id, 'Укажите ссылку на свой VK (резервный способ оперативной связи с Вами)')
    bot.register_next_step_handler(message, ask_email)


def ask_email(message):
    user_id = message.from_user.id
    user_data[user_id]['vk'] = message.text
    bot.send_message(user_id, 'Укажите адрес своей электронной почты')
    bot.register_next_step_handler(message, save_to_db)


def save_to_db(message):
    user_id = message.from_user.id
    user_data[user_id]['email'] = message.text

    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if not re.match(email_regex, message.text):
        bot.send_message(user_id,
                         'Пожалуйста, укажите корректный адрес электронной почты (например, example@mail.ru)')
        bot.register_next_step_handler(message, save_to_db)
        return

    bot.send_message(user_id, f'Отлично. Вы завершили анкетирование! Ваша персональная ссылка для прохождения вступительного тестирования: http://crm.studprzi.beget.tech/{user_id}')

    save_to_database(user_data[user_id], user_id)

    full_name = user_data[user_id]['full_name']
    course = user_data[user_id]['course']
    university = user_data[user_id]['university']
    speciality = user_data[user_id]['speciality']
    degree = user_data[user_id]['degree']
    telegram = user_id
    phone = user_data[user_id]['phone']
    vk = user_data[user_id]['vk']
    email = user_data[user_id]['email']


if __name__ == "__main__":
    try:
        bot.polling(none_stop=True, interval=0)
    except ApiException as e:
        print(e)
