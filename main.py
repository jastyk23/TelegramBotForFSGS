import json
import os
import sys
from datetime import datetime
import apk_killer
import apk_status
import telebot
import threading
import time
from operator_changes import changes

# Chat APK -826999910
# APK bot 5400717778:AAElaDpGCslweXlFKJqecCbsb0wtjueI8iI

# Chat MY 1048052384
# MY bot 5788985434:AAEFIj5fY2HnZw35alMaDBOfCvsBq_xGVPs

operators = ("EFT", "ГКУ Ресурсы Ямала 2", "ГКУ Ресурсы Ямала 1", "Минцифры Чувашии", "ЦТИПК", "МОБТИ", "IGS",
             "Ростехинвентаризация", "Рощино", "Мосгоргеотрест", "Татнефть", "ЦИОГД", "КПФУ",
             "ГЕКСАГОН", "ЦГКиИПД", "ПРИН", "Липецкоблтехинвентаризация", "ТНЦ РБ", "ГСИ", "ИПГ", "ЦКОиМН")

non_mes = True
dis_noti = True
timelt = '17'
timegt = '9'

if __name__ == '__main__':
    API_TOKEN = '5400717778:AAElaDpGCslweXlFKJqecCbsb0wtjueI8iI'
    bot = telebot.TeleBot(API_TOKEN)
    chat_id = -826999910
    state = True
    bot.send_message(chat_id, 'Я начал работать')


    def timer():
        global dis_noti, timegt
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


    def check_stat_apk():
        status_arch = []
        while True:
            if non_mes:
                if len(status_arch) > 0:
                    bot.send_message(chat_id, '\n'.join(status_arch) + '\n#косякиапк', disable_notification=dis_noti)
                    status_arch = []
                status = apk_status.stat()
                if len(status) > 0:
                    bot.send_message(chat_id, '\n'.join(status) + '\n#косякапк', disable_notification=dis_noti)
                    print('Статус отправлен')
                    time.sleep(900)
                else:
                    print('Проблем нет')
                    time.sleep(360)
            else:
                stat_l = apk_status.stat()
                if len(stat_l) > 0:
                    print('Записал в архив')
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    status_arch.append(str(current_time) + ':\n' + '\n'.join(stat_l))
                else:
                    print('Проблем нет')
                    time.sleep(60)


    def check_message():

        @bot.message_handler(commands=['mute'])
        def mute(message):
            global non_mes
            non_mes = False
            bot.send_message(message.chat.id, 'Молчу 🤫', disable_notification=dis_noti)

        @bot.message_handler(commands=['unmute'])
        def unmute(message):
            global non_mes
            non_mes = True
            bot.send_message(message.chat.id, 'Щас всё расскажу', disable_notification=dis_noti)

        @bot.message_handler(commands=['killapk'])
        def kill_apk(message):
            bot.send_message(message.chat.id, 'Убит через: 3', disable_notification=dis_noti)
            time.sleep(1)

            bot.send_message(message.chat.id, 'Убит через: 2', disable_notification=dis_noti)
            time.sleep(1)
            bot.send_message(message.chat.id, 'Убит через: 1', disable_notification=dis_noti)
            time.sleep(1)
            bot.send_message(message.chat.id, 'Пиу-Пау', disable_notification=dis_noti)
            apk_killer.kill()

        @bot.message_handler(commands=['restart'])
        def restart(message):
            bot.send_message(message.chat.id, 'Перезапускаю', disable_notification=dis_noti)
            os.execv(sys.executable, [sys.executable] + sys.argv)

        @bot.message_handler(commands=['end'])
        def kill_apk(message):
            bot.send_message(message.chat.id, 'Ну всё ухожу, чё бухтеть то', disable_notification=dis_noti)
            thread1.join(timeout=1)
            condition = False
            bot.stop_polling()

        @bot.message_handler(commands=['checkop'])
        def checkop(message):
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
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

        @bot.message_handler(commands=['help'])
        def helper(message):
            bot.send_message(message.chat.id,
                             '/restart - перезапуск бота\n/end - отрубить бота\n/checkop- изменения оперторов\n/status - состояние АПК\n/killapk - судный день АПК\n/mute - пусть умолкнет\n/unmute - будет болтать',
                             disable_notification=dis_noti)

        @bot.message_handler(commands=['status'])
        def kill_apk(message):
            print(dis_noti)
            status = apk_status.stat()
            if len(status) > 0:
                bot.send_message(message.chat.id, '\n'.join(status) + '\n#косякапк', disable_notification=dis_noti)
                print('Статус отправлен')
            else:
                bot.send_message(message.chat.id, 'Всё круто', disable_notification=dis_noti)
                print('Проблем нет')

        @bot.message_handler(content_types=['text'])
        def find_changes(message):
            hide = telebot.types.ReplyKeyboardRemove()
            if message.text == "Убрать кнопки":
                bot.send_message(message.chat.id, 'Прячу клавиатуру', reply_markup=hide, disable_notification=dis_noti)
            elif message.text in operators:
                ch_list = changes(message.text)
                if len(ch_list) < 5:
                    for index, el in enumerate(ch_list):
                        bot.send_message(message.chat.id, '{\n' + ',\n'.join(
                            [f'{key.capitalize()}: {value}' for key, value in el.items()]) + '\n}', reply_markup=hide,
                                         disable_notification=dis_noti)
                        time.sleep(1)
                else:
                    with open(f'Change_files/{message.text}_change.json', 'w') as file:
                        json.dump(ch_list, file, indent=4, ensure_ascii=False)
                        file.close()
                    with open(f'Change_files/{message.text}_change.json') as file:
                        bot.send_document(message.chat.id, document=file, reply_markup=hide,
                                          disable_notification=dis_noti)
                        file.close()


    thread3 = threading.Thread(target=timer, daemon=True, name='Time_thread')
    thread1 = threading.Thread(target=check_stat_apk, daemon=True, name='Status_thread')
    thread2 = threading.Thread(target=check_message, daemon=True, name='Check_thread')

    thread1.start()
    thread2.start()
    thread3.start()
    try:
        bot.polling(non_stop=state)
    except:
        print(datetime.now())
    thread2.join(timeout=1)
    thread3.join(timeout=1)
    exit()
