def actions(message):
    global count, current_word, meaning_word, count_for_victory
    if message.text != 'СТОП' and count == 1:
        current_word = message.text[0]
        count = 0
    if message.text != 'СТОП' and count_for_victory != 0:
        for k in range(len(message.text) - 1):
            if not message.text[k].isalpha() and message.text[k] != ' ':
                message.text = message.text[0:k] + message.text[k + 1:len(message.text)]
                bot.send_message(message.chat.id,
                                 'Ваше слово содержит странные символы. Мы их обрежем и получим "' + message.text + '"')
                return 'input_error_weird_chars'
        for j in range(len(message.text) - 1, 0, -1):
            if message.text[j] == ' ':
                bot.send_message(message.chat.id,
                                 'Вы ввели больше одного слова. В игру принимается первое, то есть "' + message.text[0:j] + '"')
                message.text = message.text[0:j]
                # break
                return 'input_error_too_many_words'
        if (message.text[len(message.text) - 1]).lower() == 'ь':
            bot.send_message(message.chat.id,
                             'Вы ввели слово, которое оканчивается на мягкий знак. Я возьму предыдущую букву, то есть "' +
                             message.text[len(message.text) - 2] + '"')
            letter = (message.text[len(message.text) - 2]).lower()
            return 'input_error_ь'
        elif (message.text[len(message.text) - 1]).lower() == 'ы':
            bot.send_message(message.chat.id,
                             'Вы ввели слово, которое оканчивается на "ы". Я возьму предыдущую букву, то есть "' +
                             message.text[len(message.text) - 2] + '"')
            letter = (message.text[len(message.text) - 2]).lower()
            return 'input_error_ы'
        elif (message.text[len(message.text) - 1]).lower() == 'ъ':
            bot.send_message(message.chat.id,
                             'Вы ввели слово, которое оканчивается на твердый знак. Я возьму предыдущую букву, то есть "' +
                             message.text[len(message.text) - 2] + '"')
            letter = (message.text[len(message.text) - 2]).lower()
        else:
            letter = (message.text[len(message.text) - 1]).lower()
        if message.text[0].lower() == current_word[len(current_word) - 1].lower() and count_for_victory != 0:
            mas_with_words = []
            count_for_victory -= 1
            url = 'https://ru.wiktionary.org/wiki/' + message.text.lower()
            request = requests.get(url)
            if (request.status_code == 200) and (not used_words.__contains__(str(message.text.lower()))):
                for i in range(len(words)):
                    word_from_list = words[i]
                    if letter.lower() == word_from_list[0].lower() and word_from_list[
                        len(word_from_list) - 1] != 'ь' and word_from_list[
                        len(word_from_list) - 1] != 'ы' and not used_words.__contains__(str(word_from_list.lower())):
                        mas_with_words.append(word_from_list)
                current_word = mas_with_words[random.randint(0, len(mas_with_words))]
                meaning_word = current_word[0].upper() + current_word[1:len(current_word)]
                markup_meaning = telebot.types.InlineKeyboardMarkup()
                markup_meaning.add(telebot.types.InlineKeyboardButton(text='Значение',
                                                                      url='https://ru.wikipedia.org/wiki/' + meaning_word))
                bot.send_message(message.chat.id, meaning_word, reply_markup=markup_meaning)
                used_words.append(str(message.text.lower()))
                used_words.append(str(current_word.lower()))
            elif request.status_code != 200:
                bot.send_message(message.chat.id,
                                 'Кажется, слова "' + message.text + '" нет в русском языке.\nПопробуйте другое слово)')

                return 'input_error_word_does_not_exist'

            elif used_words.__contains__(str(message.text.lower())):
                bot.send_message(message.chat.id, 'Слово "' + message.text + '" уже было.\nПопробуйте еще раз)')

                return 'input_error'

        elif message.text[0].lower() != current_word[len(current_word) - 1].lower():
            bot.send_message(message.chat.id,
                             'Вы ввели слово, которое начинается с буквы "' + message.text[0] + '", а нужно с буквы "' +
                             current_word[len(current_word) - 1] + '".\nПопробуйте еще раз)')

            return 'input_error'

        return 'iteration_played'

    elif count_for_victory == 0:
        bot.send_message(message.chat.id, 'Поздравляю! Вы победили.')
        keyboard1 = telebot.types.InlineKeyboardMarkup()
        keyboard1.add(telebot.types.InlineKeyboardButton(text='Да, давай!', callback_data='yes'))
        keyboard1.add(telebot.types.InlineKeyboardButton(text='В другой раз', callback_data='no'))
        bot.send_message(message.from_user.id, 'Cыграем еще раз?', reply_markup=keyboard1)
        count = 0

        return "victory"

    elif message.text == 'СТОП':
        keyboard1 = telebot.types.InlineKeyboardMarkup()
        keyboard1.add(telebot.types.InlineKeyboardButton(text='Да, давай!', callback_data='yes'))
        keyboard1.add(telebot.types.InlineKeyboardButton(text='В другой раз', callback_data='no'))
        bot.send_message(message.from_user.id, 'Победила дружба :)\nCыграем еще раз?', reply_markup=keyboard1)
        count = 0
        count_for_victory = 0
        used_words.clear()

        return 'stopped'
