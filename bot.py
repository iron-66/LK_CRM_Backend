from telebot import TeleBot
from telebot import types
from telebot.apihelper import ApiException
import psycopg2


TOKEN = '6730210777:AAErUqdTxdedDM31JFdGqN6DjxeiMFmwxQ0'
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

        # SQL-запрос для вставки данных в таблицу students
        sql_query = """
            INSERT INTO public."API_student" (full_name, course, university, speciality, degree, telegram, phone, vk, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Получаем данные из user_data
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

        # Выполняем SQL-запрос
        cursor.execute(sql_query, data)

        # Применяем изменения
        connection.commit()

        print("Данные успешно добавлены в базу данных!")

    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с базой данных:", error)

    finally:
        # Закрываем соединение с базой данных
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


def ask_name(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Представьтесь, пожалуйста. Напишите Ваше ФИО')
    bot.register_next_step_handler(message, ask_course)


def ask_course(message):
    user_id = message.from_user.id
    user_data[user_id]['full_name'] = message.text
    name = message.text.split()
    bot.send_message(user_id, f'Отлично, {name[1]}, теперь укажите, на каком курсе Вы учитесь')
    bot.register_next_step_handler(message, ask_university)


def ask_university(message):
    user_id = message.from_user.id
    user_data[user_id]['course'] = message.text
    bot.send_message(user_id, 'Теперь укажите своё учебное заведение (например, УрФУ)')
    bot.register_next_step_handler(message, ask_speciality)


def ask_speciality(message):
    user_id = message.from_user.id
    user_data[user_id]['university'] = message.text
    bot.send_message(user_id, 'Укажите свою специальность / направление (например, программная инженерия)')
    bot.register_next_step_handler(message, ask_degree)


def ask_degree(message):
    user_id = message.from_user.id
    user_data[user_id]['speciality'] = message.text
    bot.send_message(user_id, 'Укажите свою академическую степень (бакалавриат / специалитет)')
    bot.register_next_step_handler(message, ask_phone)


def ask_phone(message):
    user_id = message.from_user.id
    user_data[user_id]['degree'] = message.text
    bot.send_message(user_id, 'Укажите номер своего телефона (+7 9XX XXX XX XX)')
    bot.register_next_step_handler(message, ask_vk)


def ask_vk(message):
    user_id = message.from_user.id
    user_data[user_id]['phone'] = message.text
    bot.send_message(user_id, 'Укажите ссылку на свой VK')
    bot.register_next_step_handler(message, ask_email)


def ask_email(message):
    user_id = message.from_user.id
    user_data[user_id]['vk'] = message.text
    bot.send_message(user_id, 'Укажите адрес своей электронной почты')
    bot.register_next_step_handler(message, save_to_db)


def save_to_db(message):
    user_id = message.from_user.id
    user_data[user_id]['email'] = message.text
    bot.send_message(user_id, f'Отлично. Вы завершили анкетирование! Ваша персональная ссылка для прохождения вступительного тестирования: http://158.160.137.207:8000/{user_id}')

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
