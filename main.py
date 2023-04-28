import json
import os
import sys
from datetime import datetime
import apk_status
import telebot
import threading
import time
from operator_changes import changes
from requests.exceptions import ReadTimeout



operators = ("EFT", "ГКУ Ресурсы Ямала 2", "ГКУ Ресурсы Ямала 1", "Минцифры Чувашии", "ЦТИПК", "МОБТИ", "IGS",
             "Ростехинвентаризация", "Рощино", "Мосгоргеотрест", "Татнефть", "ЦИОГД", "КПФУ",
             "ГЕКСАГОН", "ЦГКиИПД", "ПРИН", "Липецкоблтехинвентаризация", "ТНЦ РБ", "ГСИ", "ИПГ", "ЦКОиМН")

non_mes = True
dis_noti = True
timelt = '17' # Рабочее время
timegt = '9' # Рабочее время

if __name__ == '__main__':
    API_TOKEN = None
    bot = telebot.TeleBot(API_TOKEN)
    chat_id = None # id chata, можно прописать message.message_id и должен будет рабаотать в личный диалогах
    state = True


    def timer() -> None:
        """
        Проверяет закончился ли рабочй день, если да, то бот работает в беззвучном режиме.
        :return: None
        """
        global dis_noti, timegt, timelt
        while True:
            now = datetime.now()
            current_time = now.strftime("%H")
            w_day = now.strftime("%a")
            if w_day == 'Fri':
                timelt = '16'
            elif w_day == 'Sun' or w_day == 'Sat':
                dis_noti = True
                time.sleep(43200)
                continue
            if int(timegt) < int(current_time) < int(timelt):
                dis_noti = False
            time.sleep(3600)


    def check_stat_apk() -> None:
        """
        Проверяет состояние АПК ФСГС.
        Есть 2 режима:
            if non_mes is True:
                работает в обычном режиме
            else:
                записывает состояния в архив, который выдает после возвращения в обычный режим
        :return: None
        """
        status_arch = []
        while True:
            if non_mes:
                if len(status_arch) > 0: # Если архив не пустой выводит бользователю все данные
                    try:
                        bot.send_message(chat_id, '\n'.join(status_arch) + '\n#косякиапк', disable_notification=dis_noti)
                    except telebot.apihelper.ApiTelegramException: # Если данных слишком много отдает тектовый файл со всеми статусами
                        if not os.path.exists('Change_files'):
                            os.mkdir('Change_files')
                        text = '\n'.join(status_arch)
                        with open('Change_files/log.txt', 'w') as txt_f:
                            txt_f.write(text)
                            bot.send_message(message.chat.id, 'Видимо ошибок было слишком много, так что вот вам логи.')
                            bot.send_document(message.chat.id, document=file, disable_notification=dis_noti)
                    status_arch = [] # Обнуляем архив
                status = apk_status.stat() # Получает статус ФСГС
                if len(status) > 0: # Если есть ошибка выводит ее и слипается на 15 минут
                    bot.send_message(chat_id, '\n'.join(status) + '\n#косякапк', disable_notification=dis_noti)
                    print('Статус отправлен')
                    time.sleep(900)
                else: # Если ошибки нет уходит в слип 6 минут
                    time.sleep(360)
            else:
                stat_l = apk_status.stat()
                if len(stat_l) > 0:
                    print('Записал в архив')
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    status_arch.append(str(current_time) + ':\n' + '\n'.join(stat_l))
                else:
                    time.sleep(360)


    def check_message() -> None:
        """
        Функция для работы на отдлеьном потоке для проверки поступающих сообщений
        :return: None
        """
        @bot.message_handler(commands=['start'])
        def mute(message): # Запускает бота, включает сообщения

            global non_mes
            non_mes = False
            bot.send_message(message.chat.id, 'Я начал работать', disable_notification=dis_noti)
        @bot.message_handler(commands=['mute'])
        def mute(message): # Выключает увдомления бота о работе
            global non_mes
            non_mes = False
            bot.send_message(message.chat.id, 'Молчу 🤫', disable_notification=dis_noti)

        @bot.message_handler(commands=['unmute']) # Включает уведомления обратоно
        def unmute(message):
            global non_mes
            non_mes = True
            bot.send_message(message.chat.id, 'Щас всё расскажу', disable_notification=dis_noti)

        @bot.message_handler(commands=['restart']) # Перезапускает бота
        def restart(message):
            bot.send_message(message.chat.id, 'Перезапускаю', disable_notification=dis_noti)
            os.execv(sys.executable, [sys.executable] + sys.argv)

        @bot.message_handler(commands=['end']) # Выключает бота
        def kill_цapk(message):
            bot.send_message(message.chat.id, 'Ну всё ухожу, чё бухтеть то', disable_notification=dis_noti)
            thread1.join(timeout=1)
            bot.stop_polling()

        @bot.message_handler(commands=['changeop']) # Для проверки изменений бота выводит клавиатуру с операторами
        def changer(message):
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True) # selective показывает клавиатуру только пользователю который ее запросил
            for index, operator in enumerate(operators):
                if index != 0 and index % 2 != 0:
                    continue
                if index + 1 < len(operators):
                    op_button1 = telebot.types.KeyboardButton(operators[index])
                    op_button2 = telebot.types.KeyboardButton(operators[index + 1])
                    markup.add(op_button1, op_button2)
            hide_button = telebot.types.KeyboardButton("Убрать кнопки")
            markup.add(hide_button)
            bot.send_message(chat_id=message.chat.id, text='Выбери оператора', reply_to_message_id=message.message_id,
                             reply_markup=markup, disable_notification=dis_noti)



        @bot.message_handler(commands=['help']) # Выводит помощь
        def helper(message):
            bot.send_message(message.chat.id,
                             '/restart - перезапуск бота\n/end - отрубить бота\n/changeop- изменения оперторов\n/status - состояние АПК\n/killapk - судный день АПК\n/mute - пусть умолкнет\n/unmute - будет болтать',
                             disable_notification=dis_noti)

        @bot.message_handler(commands=['status'])
        def status_apk(message): # Выводит состояние АПК ФСГС на данный момент по запросу
            print(dis_noti)
            status = apk_status.stat()
            if len(status) > 0:
                bot.send_message(message.chat.id, '\n'.join(status) + '\n#косякапк', disable_notification=dis_noti)
                print('Статус отправлен')
            else:
                bot.send_message(message.chat.id, 'Всё круто', disable_notification=dis_noti)
                print('Проблем нет')

        @bot.message_handler(content_types=['text'])
        def find_changes(message): # Отарабатывает получаемые сообщение
            hide = telebot.types.ReplyKeyboardRemove()
            if message.text == "Убрать кнопки": # Убирает клавиатуру, к сожалению сообщение видят все пользователи если бот используетс в чате
                bot.send_message(message.chat.id, 'Прячу клавиатуру', reply_markup=hide, disable_notification=dis_noti)
            elif message.text in operators: # Проверяет оператора в списке
                ch_list = changes(message.text)
                if ch_list is None: # Если авторизация не прошла уведомляют пользователя что проблемы со входом
                    bot.send_message(message.chat.id, 'Пробелмы с авторизацией.', reply_markup=hide,
                                     disable_notification=dis_noti)
                elif len(ch_list) < 5: # Если списко изменения небольшой отправляетя данные списком
                    for index, el in enumerate(ch_list):
                        bot.send_message(message.chat.id, '{\n' + ',\n'.join(
                            [f'{key.capitalize()}: {value}' for key, value in el.items()]) + '\n}', reply_markup=hide,
                                         disable_notification=dis_noti)
                        time.sleep(1)
                else: # Если изменений много отправляет JSON с изменениями
                    if not os.path.exists('Change_files'):
                        os.mkdir('Change_files')
                    with open(f'Change_files/{message.text}_change.json', 'w') as file:
                        json.dump(ch_list, file, indent=4, ensure_ascii=False)
                        file.close()
                    with open(f'Change_files/{message.text}_change.json') as file:
                        bot.send_document(message.chat.id, document=file, reply_markup=hide,
                                          disable_notification=dis_noti)
                        file.close()


    thread1 = threading.Thread(target=check_stat_apk, daemon=True, name='Status_thread').start()
    thread2 = threading.Thread(target=check_message, daemon=True, name='Check_thread').start()
    thread3 = threading.Thread(target=timer, daemon=True, name='Time_thread').start()
    try:
        bot.polling(non_stop=state)
    except ReadTimeout as er:
        print(er, datetime.now())
    thread2.join(timeout=1)
    thread3.join(timeout=1)
    exit()
