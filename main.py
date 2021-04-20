from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
import time
from telegram import ReplyKeyboardMarkup
from telegram import Update
from bs4 import BeautifulSoup
import requests
from telegram.ext.callbackcontext import CallbackContext

TOKEN = '1796047189:AAHjg-N-h51PdSM3np0YnPDdRCYrhgBNjek'


# стартовая функция
def start(update, context):
    update.message.reply_text('Вас приветствует TaskManagerBot. '
                              'Введите /help, чтобы узнать, что я умею')


# команда, которая отправляет пользователю текущий курс доллара
def command_get_dollar(update: Update, context: CallbackContext):
    DOLLAR_RUB = 'https://www.google.com/search?safe=active&sxsrf=ALeKk003OV_fO84nnGD7PNqKct-tE445WA%3A1585668817809&ei=0WKDXsHaMIWJrwSnga_IAQ&q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80&gs_lcp=CgZwc3ktYWIQAzIJCCMQJxBGEIICMgUIABCDATIFCAAQgwEyBQgAEIMBMgIIADICCAAyBQgAEIMBMgUIABCDATIECAAQQzICCAA6BAgAEEc6BAgjECc6CggAEIMBEBQQhwJQ-68CWOm7AmCUvwJoAHACeACAAXiIAZgGkgEDNi4ymAEAoAEBqgEHZ3dzLXdpeg&sclient=psy-ab&ved=0ahUKEwiBh_fUhMXoAhWFxIsKHafACxkQ4dUDCAs&uact=5'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    full_page = requests.get(DOLLAR_RUB, headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    convert = soup.findAll("span", {"class": "DFlfde SwHCTb", "data-precision": 2})
    update.message.reply_text(
        f'На данный момент один доллар стоит ' + str(convert[0].text) + ' рублей')


# команда, которая отправляет пользователю текущий курс евро
def command_get_euro(update: Update, context: CallbackContext):
    EURO_RUB = 'https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B5%D0%B2%D1%80%D0%BE&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%B5%D0%B2%D1%80%D0%BE&aqs=chrome..69i57j0i131i433j0j0i433j0i131i433l2j0i457j0j0i131i433j0.3528j1j4&sourceid=chrome&ie=UTF-8'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    full_page = requests.get(EURO_RUB, headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    convert = soup.findAll("span", {"class": "DFlfde SwHCTb", "data-precision": 2})
    update.message.reply_text(
        f'На данный момент один евро стоит ' + str(convert[0].text) + ' рублей')


# команда, отправляет пользователю, что умеет данный бот
def command_help(update: Update, context: CallbackContext):
    print(update.message.chat)


# команда, которая в ответ присылает текущее время
def command_time(update, context):
    update.message.reply_text(time.asctime().split()[-2])


# команда, которая в ответ присылает текущую дату
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
    #text_handler = MessageHandler(Filters.text, echo)

    # Регистрируем обработчик и команды в диспетчере.
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", command_help))
    dp.add_handler(CommandHandler("time", command_time))
    dp.add_handler(CommandHandler("date", command_date))
    dp.add_handler(CommandHandler("dollar", command_get_dollar))
    dp.add_handler(CommandHandler("euro", command_get_euro))
    #dp.add_handler(text_handler)

    # Магические строчки, которые запускают и останавливают цикл программы
    updater.start_polling()
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
