from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
import time
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater
from bs4 import BeautifulSoup
import requests
from telegram.ext.callbackcontext import CallbackContext

TOKEN = '1796047189:AAHjg-N-h51PdSM3np0YnPDdRCYrhgBNjek'


def echo(update, context):
    update.message.reply_text('Я получил сообщение: ' + str(update.message.text) + 'МАКС ЧЕМПИОН')


def start(update, context):
    update.message.reply_text(
        "Привет! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!\n"
        "Используйте /set <количество секунд> для установки таймера")


def command_get_dollar(update, context):
    print(context)
    DOLLAR_RUB = 'https://www.google.com/search?safe=active&sxsrf=ALeKk003OV_fO84nnGD7PNqKct-tE445WA%3A1585668817809&ei=0WKDXsHaMIWJrwSnga_IAQ&q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80&gs_lcp=CgZwc3ktYWIQAzIJCCMQJxBGEIICMgUIABCDATIFCAAQgwEyBQgAEIMBMgIIADICCAAyBQgAEIMBMgUIABCDATIECAAQQzICCAA6BAgAEEc6BAgjECc6CggAEIMBEBQQhwJQ-68CWOm7AmCUvwJoAHACeACAAXiIAZgGkgEDNi4ymAEAoAEBqgEHZ3dzLXdpeg&sclient=psy-ab&ved=0ahUKEwiBh_fUhMXoAhWFxIsKHafACxkQ4dUDCAs&uact=5'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    full_page = requests.get(DOLLAR_RUB, headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    convert = soup.findAll("span", {"class": "DFlfde SwHCTb", "data-precision": 2})
    update.message.reply_text(
        f'На данный момент один доллар стоит ' + str(convert[0].text) + ' рублей')


def send_alarm(context):
    job = context.job
    context.bot.send_message(job.context, text='Время истекло!!!')


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def command_set_timer(update, context):
    chat_id = update.message.chat_id
    try:
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('Мы не можем перемещаться назад в будущее((')
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(send_alarm, due, context=chat_id, name=str(chat_id))

        text = 'Таймер успешно установлен'
        if job_removed:
            text += 'Старый таймер был удалён'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Используйте: /set <количество секунд>')


def command_help(update, context):
    update.message.reply_text(
        "Я пока не умею помогать... Я только ваше эхо. Но могу поставить таймер.")


def command_time(update, context):
    update.message.reply_text(time.asctime().split()[-2])


def command_date(update, context):
    sp = time.asctime().split()
    ans = [sp[2], sp[1], sp[4]]
    update.message.reply_text((' ').join(ans))


def main():
    updater = Updater(TOKEN, use_context=True)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    # Создаём обработчик сообщений типа Filters.text
    # из описанной выше функции echo()
    # После регистрации обработчика в диспетчере
    # эта функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    text_handler = MessageHandler(Filters.text, echo)

    # Регистрируем обработчик и команды в диспетчере.
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", command_help))
    dp.add_handler(CommandHandler("time", command_time))
    dp.add_handler(CommandHandler("date", command_date))
    dp.add_handler(CommandHandler("set", command_set_timer))
    dp.add_handler(CommandHandler("dollar", command_get_dollar))
    dp.add_handler(text_handler)

    # Магические строчки, которые запускают и останавливают цикл программы
    updater.start_polling()
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
