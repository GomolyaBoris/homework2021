import telebot # загружаем библиотеки
import pb
import pytz
import json
import traceback



# передаём токен
bot = telebot.TeleBot('5051007404:AAHBx9VXFOu7FFI9CQKmRejW_eiSnhnJehs')

# пишем обработчик команды /start
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        'Прекрасно! Я могу показать Вам курсы обмена валют.\n' +
        'Чтобы узнать курсы обмена, нажмите /exchange.\n' +
        'Если что-то непонятно, то нажмите /help для инструкции и для того, чтобы написать разрабу.'
  )

# пишем обработчик команды /help
@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            'Написать разработчику', url='telegram.me/gorinich144'
  )
    )
    bot.send_message(
        message.chat.id,
        '1) Чтобы получить список доступных валют, нажмите /exchange.\n' +
        '2) Нажмите на интересующую Вас валюту.\n' +
        '3) Вы получите сообщение, содержащее информацию об источнике и валютах, ' +
        'курсы для покупки и продаж.\n',
        reply_markup=keyboard
    )


#Обработчик команды /exchange + создание кнопок USD, EUR, RUR
@bot.message_handler(commands=['exchange'])
def exchange_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('USD', callback_data='get-USD'),
        telebot.types.InlineKeyboardButton('BTC', callback_data='get-BTC')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('EUR', callback_data='get-EUR'),
        telebot.types.InlineKeyboardButton('RUB', callback_data='get-RUR')
    )

    bot.send_message(
        message.chat.id,
        'Выберите валюту:',
        reply_markup=keyboard
    )

# обработчик для кнопок встроенной клавиатуры
@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    data = query.data
    if data.startswith('get-'):
        get_ex_callback(query)

# реализуем query
# Метод answer_callback_query нужен, чтобы убрать состояние загрузки, к которому переходит бот после нажатия кнопки
def get_ex_callback(query):
    bot.answer_callback_query(query.id)
    send_exchange_result(query.message, query.data[4:])

# реализуем send_exchange_result Это нужно чтобы бот показывал индикатор «набора текста», пока API банка получает запрос
def send_exchange_result(message, ex_code):
    bot.send_chat_action(message.chat.id, 'typing')
    ex = pb.get_exchange(ex_code)
    bot.send_message(
        message.chat.id, serialize_ex(ex),
        reply_markup=get_update_keyboard(ex),
	parse_mode='HTML'
    )
# создадим кнопку Поделиться. У кнопки Share есть параметр switch_inline_query.
# После нажатия кнопки пользователю будет предложено выбрать один из чатов, открыть этот чат и ввести имя бота и определенный запрос в поле ввода.
def get_update_keyboard(ex):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton('Share', switch_inline_query=ex['ccy']))
    return keyboard


def serialize_ex(ex_json, diff=None):
    result = '<b>' + ex_json['base_ccy'] + ' -> ' + ex_json['ccy'] + ':</b>\n\n' + \
             'Buy: ' + ex_json['buy']
    return result

# реализовать встроенный режим
@bot.inline_handler(func=lambda query: True)
def query_text(inline_query):
    bot.answer_inline_query(
        inline_query.id,
        get_iq_articles(pb.get_exchanges(inline_query.query))
    )
# Используем get_exchanges для поиска нескольких валют, подходящих под запрос.
def get_iq_articles(exchanges):
    result = []
    for exc in exchanges:
        result.append(
            telebot.types.InlineQueryResultArticle(
                id=exc['ccy'],
	        title=exc['ccy'],
	        input_message_content=telebot.types.InputTextMessageContent(
                    serialize_ex(exc),
		    parse_mode='HTML'
		),
	        reply_markup=get_update_keyboard(exc),
	        description='Convert ' + exc['base_ccy'] + ' -> ' + exc['ccy'],
	        thumb_height=1
	    )
        )
    return result


bot.polling(none_stop=True)

