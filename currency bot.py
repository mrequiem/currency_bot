import telebot
from config import currencies, TOKEN
from extensions import ConvertionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Введите команду в следующем формате:\n<Название валюты на продажу> \
<Название валюты к покупке> <Количество валюты на продажу>\nНапример: "Рубль Доллар 1000"\n\
Таким образом вы узнаете сколько долларов можно получить за 1000 рублей\nЧтобы просмотреть список валют, введите /values'
    bot.reply_to(message, text)

@bot.message_handler(commands = ['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\n🇷🇺рубль\n🇺🇸доллар\n🇪🇺евро\n🇬🇧фунт\n🇵🇱злотый\n🇺🇦гривна\n🇬🇪лари\n🇰🇿тенге\n🇯🇵иена\n🇨🇳юань'

    bot.reply_to(message, text)

@bot.message_handler(content_types = ["text", ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров')

        quote, base, amount = values
        total_base = CurrencyConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Валюта {quote} в количестве {amount} в валюте {base} составит {round(total_base, 2)}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop = True)