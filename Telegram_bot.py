from telebot import TeleBot, types
import OP_Spoilers


class MyBot(TeleBot):
    last_written_user = None
    repeat = 0
    add_last_user = None
    del_last_user = None
    addition = False

    def check_repeats(self, message):
        if message.content_type == 'text':
            if self.repeat == 10:
                self.send_message(message.chat.id,
                                  f'Эй, {message.from_user.username}, успокойся. Хватит долбить сообщения в этот чат')
                self.repeat = 0
            else:
                if self.last_written_user == message.from_user.id:
                    self.repeat += 1
                else:
                    self.repeat = 1
                    self.last_written_user = message.from_user.id


token = '5586816905:AAFTDyaK__0E87K1tP9U8varS2xk7TixkEQ'
bot = MyBot(token)
bad_words = (
    'семпа', '2D девоч', 'гарем', 'кун', 'сан', 'чан', 'kun', 'chan', 'san', 'sama', 'сумимасен', 'гоменнасай',
    'гоменне', 'аригато')
one_piece = OP_Spoilers.make_list()
add_op = 'Add_One_Piece_Spoilers'
add_jp = 'Add_Deprecated_Japanese_Words'


@bot.message_handler(commands=['add'])
def add(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    op_button = types.KeyboardButton(f'/{add_op}')
    jap_words_button = types.KeyboardButton(f'/{add_jp}')
    markup.add(op_button, jap_words_button)
    bot.send_message(message.chat.id, 'Выбирай, куда добавишь слово', reply_markup=markup)
    bot.add_last_user = message.from_user.id


@bot.message_handler(commands=['help'])
def help_com(message):
    bot.send_message(message.chat.id, 'Автор еще не придумал как легко и быстро написать все функции')


@bot.message_handler(commands=['place'])
def place(message):
    bot.send_message(message.chat.id, f'Дружище, я на месте')


@bot.message_handler(commands=['poll'])
def poll(message):
    bot.send_message(message.chat.id, 'Выясняйте, чады')
    bot.send_poll(message.chat.id, 'Он сейчас насрал?', ['Да', 'Нет'], is_anonymous=False)


@bot.message_handler(commands=[add_op])
def op_button_com(message):
    if bot.add_last_user == message.from_user.id:
        bot.send_message(message.chat.id, 'Напиши термин, который будет являться спойлером для Ван Писа')
        bot.addition = True


@bot.message_handler(content_types=['text'])
def correction(message):
    """
    :param Message message:
    """
    try:
        if r'\\' in message.text:
            return
        bot.check_repeats(message)

        if bot.addition:
            added = OP_Spoilers.addition(message.text.lower(), one_piece)
            bot.send_message(message.chat.id, 'Добавил' if added else 'Дружище, такой термин уже в списке')
            bot.addition = False
            return

        if any(map(lambda x: x in message.text.lower(), bad_words)):
            bot.send_message(message.chat.id,
                             f'Этот {message.from_user.first_name} насрал что-то на японском. В общем Диме нельзя такое читать\n<tg-spoiler>{message.text}</tg-spoiler>',
                             parse_mode='HTML')
            bot.delete_message(message.chat.id, message.message_id)

        if any(map(lambda x: x in message.text.lower(), one_piece)):
            bot.send_message(message.chat.id,
                             f'Этот {message.from_user.first_name} насрал! В этом сообщении спойлеры к Ван Пису!\n<tg-spoiler>{message.text}</tg-spoiler>',
                             parse_mode='HTML')
            bot.delete_message(message.chat.id, message.message_id)

        if 'прости' in message.text.lower():
            bot.send_message(message.chat.id, 'Друг, я прощаю тебя. Но больше не повторяй свою ошибку')

    except:
        print('Не смог обработать сообщение')
    print(message.from_user.id, message.from_user.first_name, message.text, sep=' - ')


print('I am ready')
bot.infinity_polling()
