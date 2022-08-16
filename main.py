# попробовать реализовать игру "Быки и коровы". Бот загадывает слово из определенного количества букв.
# Допустим, четырех. Ваша задача - угадать слово, называя слова из того же количества букв (добавьте проверку).
# Если буква из вашего слова есть в загаданном - это корова.
# Если еще и позиция совпадает - это бык.
# Пример:
# загаданное слово: чаты.
# Игрок: тьма - 2 коровы
# Игрок : чума - 1 бык, 1 корова.
import random

from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler, updater, dispatcher
import os


MATCH = 0
word = ''

def game_bot(token):
    bot = Bot(token)
    updater = Updater(token)
    dispatcher = updater.dispatcher
    print('Бот работает...')


    def start(update, context):
        global word
        word = random.choice(list(open('Words.txt')))
        print(word)
        context.bot.send_message(update.effective_chat.id, "Привет! Правила игры просты. Я загадал слово из пяти неповторяющихся букв, сможешь отгадать?")
        return MATCH

    def game(update, context):
        bull = 0
        cow = 0
        global word
        word_new = update.message.text
        if len(word_new) == 5:
            for i,j in zip(word, word_new):
                if j in word:
                    if i == j:
                        context.bot.send_message(update.effective_chat.id, f'Вы отгадали букву {j}')
                        bull += 1
                    else:
                        context.bot.send_message(update.effective_chat.id, f'буква {j} есть в этом слове, но в другом месте')
                        cow +=1
            if bull == 5:
                context.bot.send_message(update.effective_chat.id, f'Поздравляю! Вы отгадали слово {word}!')
                return ConversationHandler.END
            else:
                context.bot.send_message(update.effective_chat.id, f'Вы не угадали, подумайте еще')
                return MATCH
        else:
            context.bot.send_message(update.effective_chat.id, f'Загаданное слово состоит из пяти букв')
            return MATCH

    def stop(update, context):
        context.bot.send_message(update.effective_chat.id, "Уже уходите? Хорошего дня!")

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('start'), start)],
        states={
            MATCH: [MessageHandler(Filters.text, game)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )


    dispatcher.add_handler(conv_handler)


    updater.start_polling()
    updater.idle()

def main():
    game_bot(os.getenv('TOKEN'))
    print('Бот остановлен!')


if __name__ == "__main__":
    main()