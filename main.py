import config, dbRequests, keybords as kb
import telebot
from telebot import types


bot = telebot.TeleBot(config.BOT_TOKEN)


userInfo = {}

USER_STATUS = {}
# choosing_category
# choosing_ingredient
# choosing_recipe
# del_ingredient
# add_ingredient_for_recipe

# 342234:{
#     'recipes':[{'id':1, 'title':'жульен'}, {2:'паста'}]
#     'page': 1,
#     'maxpage': 3
# }

newRecipe = {}



def addDescForNewRecipe(message):
    if (message.text != '◀️ Назад'):
        newRecipe['Desc'] = message.text
        newRecipe['Id'] = dbRequests.addNewRecipe(newRecipe['Title'], newRecipe['Desc'], newRecipe['CTime'], newRecipe['VideoLink'])
        ingredients = dbRequests.getAllIngredients()
        keyboardTEMP = types.InlineKeyboardMarkup(row_width=3)
        for ingredient in ingredients:
            keyboardTEMP.row(types.InlineKeyboardButton(text=ingredient[1], callback_data=ingredient[0]))
        USER_STATUS[message.from_user.id] = 'add_ingredient_for_recipe'
        keyboardTEMP.row(kb.done)
        bot.send_message(chat_id=message.from_user.id, text='Выберите продукты, которые необходимы для этого блюда и затем нажмите ГОТОВО:', reply_markup=keyboardTEMP)
    else:
        if message.from_user.id in USER_STATUS:
            del USER_STATUS[message.from_user.id]
        bot.send_message(chat_id=message.chat.id, text="Вы в меню", reply_markup=kb.keyboardMain)
def addRecipe(message):
    if(message.text != '◀️ Назад'):
        global newRecipe
        try:
            # message.text = message.text.replace(' ', '')
            recipe = message.text.split(';')
            if len(recipe) == 3:
                recipe = [x.strip() for x in recipe]
                newRecipe = {
                    'Title': recipe[0],
                    'Desc': None,
                    'CTime': recipe[1],
                    'VideoLink': recipe[2],
                    'Id': None
                }
                if newRecipe != 0:
                    msg = bot.send_message(message.from_user.id, f"Введите описание:")
                    bot.register_next_step_handler(msg, addDescForNewRecipe)
                else:
                    bot.send_message(message.from_user.id, f"Такое навзание уже существует!",reply_markup=kb.keyboardUser)
            else: bot.send_message(message.from_user.id, f"Неправильный формат записи, попробуйте ещё раз! ", reply_markup=kb.keyboardUser)
        except:
            bot.send_message(message.from_user.id, f"Неправильный формат записи, попробуйте ещё раз! ", reply_markup=kb.keyboardUser)
    else:
        if message.from_user.id in USER_STATUS:
            del USER_STATUS[message.from_user.id]
        bot.send_message(chat_id=message.chat.id, text="Вы в меню", reply_markup=kb.keyboardMain)

def delRecipe(message):
    if (message.text != '◀️ Назад'):
        r = dbRequests.delRecipe(message.text)
        if r:
            bot.send_message(chat_id=message.chat.id, text=f"Рецепт *{message.text}* успешно удален!", parse_mode='Markdown', reply_markup=kb.keyboardMain)
        else:
            bot.send_message(chat_id=message.chat.id, text=f"*{message.text}* такого рецепта не существует!", parse_mode='Markdown', reply_markup=kb.keyboardMain)
    else:
        if message.from_user.id in USER_STATUS:
            del USER_STATUS[message.from_user.id]
        bot.send_message(chat_id=message.chat.id, text="Вы в главном меню", reply_markup=kb.keyboardMain)


@bot.message_handler(commands=['addrecipe'])
def addRecipe_handler(message):
    msg = bot.send_message(message.from_user.id, f"Введите блюдо в формате - Название; Время приготовления; Ссылка на видео")
    bot.register_next_step_handler(msg, addRecipe)

@bot.message_handler(commands=['delrecipe'])
def delRecipe_handler(message):
    msg = bot.send_message(message.from_user.id, f"Введите название блюда, которое хотите удалить")
    bot.register_next_step_handler(msg, delRecipe)

@bot.message_handler(commands=['start'])
def start_handler(message):
    userInfo = message.from_user
    r = dbRequests.addUserDB(userInfo.id, userInfo.first_name)
    if(r):
        bot.send_message(message.chat.id, f"""*Привет {message.from_user.first_name}!* Добавь продукты, чтобы я смог подобрать для тебя рецепт. 
Для этого нажми _«Добавить продукт»_ ниже и выбери ингредиенты из списка, а затем нажми _«Подобрать рецепт»_👇🏻

п.с. Для супер быстрого поиска можешь просто нажать «СЛУЧАЙНЫЙ РЕЦЕПТ» и я пришлю тебе что-нибудь на свой вкус😋""",  parse_mode= "Markdown", reply_markup=kb.keyboardMain)

        bot.send_message(
            chat_id=config.ADMIN_CHAT_ID,
            text=f"Присоеденился новый пользователь {userInfo.first_name} | {userInfo.id}.",
        )
    else:
        bot.send_message(chat_id = message.chat.id, text="Вы в главном меню!", reply_markup=kb.keyboardMain)

@bot.message_handler(content_types=['text'])
def get_text_message(message):
    userId = message.from_user.id
    if(message.text == 'Мои продукты'):
        ingredients = dbRequests.getUserIngredients(userId);
        list = ""
        if len(ingredients) > 0:
            for row in ingredients:
                list += f"{row[1].title()}\n"
            bot.send_message(userId, f"*Ваш список продуктов:*\n{list}", parse_mode="Markdown", reply_markup=kb.keyboardUser)
        else:
            bot.send_message(userId, """Добавь продукты, чтобы я смог подобрать для тебя рецепт. 
Для этого нажми _«Добавить продукт»_ ниже и выбери ингредиенты из списка, а затем нажми _«Подобрать рецепт»_👇🏻

п.с. Для супер быстрого поиска можешь просто нажать _«Случайный рецепт»_ и я пришлю тебе что-нибудь на свой вкус😋""", parse_mode="Markdown",reply_markup=kb.keyboardUser)
    elif(message.text == 'Подобрать рецепты'):
        records = dbRequests.getUserIngredients(userId);
        listId = ''
        for i, row in enumerate(records):
            listId += str(row[0])
            if i != (len(records)-1):
                listId+=','
        print(listId)
        resultRecipesId = dbRequests.getRecipeForIngredients(listId)
        print("resultRecipesId = ")
        print(resultRecipesId)
        if(len(resultRecipesId) > 0):
            keyboardTEMP = types.InlineKeyboardMarkup(row_width=2)
            userInfo[userId] = {'recipes': []}
            userInfo[userId]['recipes'] = {'1': []}
            userInfo[userId]['page'] = 1
            print(userInfo)

            countOnpage = 10
            j=1

            for i, r in enumerate(resultRecipesId):
                if i == j*countOnpage:
                    j += 1
                    userInfo[userId]['recipes'][str(j)] = []

                userInfo[userId]['recipes'][str(j)].append({'id':r[0], 'title':r[1]})
                if i < countOnpage:
                    keyboardTEMP.add(types.InlineKeyboardButton(text=r[1], callback_data=r[0]))
            pages = round(len(resultRecipesId)/countOnpage)
            userInfo[userId]['maxPage'] = pages
            print(userInfo)
            if pages == 0: pages=1
            keyboardTEMP.row(kb.left, types.InlineKeyboardButton(text=f"1/{str(pages)}", callback_data='center'), kb.right)
            keyboardTEMP.row(kb.back)
            USER_STATUS[userId] = 'choosing_recipe'
            bot.send_message(userId, f"Вот, что я подобрал для тебя. Выбери любой рецепт из списка и я пришлю рецепт😋", parse_mode="Markdown", reply_markup=keyboardTEMP)
        else:
            bot.send_message(userId, f"""Извини, но кажется ты забыл добавить продукты или мне слишком мало информации😢

Повтори эти шаги и я попробую найти для тебя рецепт:
1) Нажми _«Мои продукты»_ ниже
2) Выбери _«Добавить продукт»_
3) Выбери ингредиенты из списка и нажми кнопку _«☑️Назад»_
4) Осталось выбрать _«Подобрать рецепт»_

п.с. Для супер быстрого поиска можешь просто нажать _«Случайный рецепт»_ и я пришлю тебе что-нибудь на свой вкус😋""", parse_mode="Markdown", reply_markup=kb.keyboardMain)
    elif (message.text == 'Случайный рецепт'):
        r = dbRequests.getRandomRecipe()
        bot.send_message(userId, f"*{r[1]} ({r[3]})*\n\n{r[2]}\n{r[4]}", parse_mode="Markdown",reply_markup=kb.keyboardMain)
    elif (message.text == 'Добавить продукт'):
        USER_STATUS[userId] = 'choosing_category'
        categories = dbRequests.getCategories();
        keyboardTEMP = types.InlineKeyboardMarkup(row_width=2)
        for category in categories:
            keyboardTEMP.row(types.InlineKeyboardButton(text=category[1], callback_data=category[0]))

        bot.send_message(userId, """Выберите категорию:""", parse_mode="Markdown", reply_markup=keyboardTEMP)
    elif (message.text == 'Удалить продукт'):
        # msg = bot.send_message(userId, f"Введите название продукта:", reply_markup=kb.keyboardUser)
        # bot.register_next_step_handler(msg, delIngForuser)
        USER_STATUS[userId] = 'del_ingredient'
        ingredients = dbRequests.getUserIngredients(userId);
        if len(ingredients) > 0 :
            keyboardTEMP = types.InlineKeyboardMarkup(row_width=2)
            for ingredient in ingredients:
                keyboardTEMP.row(types.InlineKeyboardButton(text=ingredient[1], callback_data=ingredient[0]))

            bot.send_message(userId, "Нажмите на продукт, чтобы удалить:", parse_mode="Markdown", reply_markup=keyboardTEMP)
        else:
            bot.send_message(userId, "У вас ещё нет продуктов, нажмите _«Добавить продукт»_, чтобы добавить!", parse_mode="Markdown",reply_markup=kb.keyboardUser)
    elif (message.text == '◀️ Назад'):
        bot.send_message(chat_id=message.chat.id, text="Вы в главном меню!", reply_markup=kb.keyboardMain)
        if (userId in userInfo):
            del userInfo[userId]
            print(userInfo)
    elif (message.text == 'Тех.Поддержка'): bot.send_message(userId, f"Если ты нашёл ошибки или у тебя есть вопросы/предложения, просто [напиши сюда](https://t.me/bloodymondayy) 😉", parse_mode="MarkdownV2", reply_markup=kb.keyboardMain, disable_web_page_preview=True)
    elif (message.text == 'Донаты'): bot.send_message(userId,"""Этот проект только запустился, и ты можешь поддержать авторов, чтобы в дальнейшем видеть крутые улучшения ✅

Если хочешь, поддержи проект рублем [здесь](https://yoomoney.ru/to/4100117581976152)👈🏼""", parse_mode="MarkdownV2", reply_markup=kb.keyboardMain, disable_web_page_preview=True)
    elif (message.text == 'Инструкция'): bot.send_message(userId, f"""Всё очень просто! Для поиска рецептов есть всего 3 кнопки внизу: _«Подобрать рецепт»_, _«Мои рецепты»_ и _«Случайный рецепт»_:

☑️_«Подобрать рецепт»_ - при помощи этой кнопки бот Easy menu пришлёт тебе рецепт на основе продуктов, которые хранятся у тебя в _«Мои рецепты»_
☑️_«Мои рецепты»_ - при помощи этой кнопки ты можешь добавить продукты из списка или удалить уже не актуальные ингредиенты. После того, как выберешь все нужные продукты и удалишь ненужные, просто нажми _«◀️ Назад»_ и _«Подобрать рецепт»_
☑️_«Случайный рецепт»_ - используй эту кнопку, чтобы быстро получить случайный рецепт от бота""", parse_mode="Markdown", reply_markup=kb.keyboardMain)
    print(USER_STATUS)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    userId = call.from_user.id
    if call.data == 'back':
        global newRecipe
        bot.send_message(chat_id=userId, text="Вы в главном меню!", reply_markup=kb.keyboardMain)
        if(userId in userInfo):
            del userInfo[userId]
        elif userId in USER_STATUS:
            del USER_STATUS[userId]
        elif newRecipe:
            newRecipe = None
            bot.send_message(chat_id=userId, text="Рецепт успешно добавлен!", reply_markup=kb.keyboardMain)
    elif call.data == 'backCat':
        USER_STATUS[userId] = 'choosing_category'
        categories = dbRequests.getCategories();
        keyboardTEMP = types.InlineKeyboardMarkup(row_width=2)
        for category in categories:
            keyboardTEMP.row(types.InlineKeyboardButton(text=category[1], callback_data=category[0]))
        bot.edit_message_text(chat_id=userId, message_id=call.message.message_id, text="""Выберите категорию:""", parse_mode="Markdown", reply_markup=keyboardTEMP)


    elif(userId in USER_STATUS and USER_STATUS[userId] == 'choosing_category'):
        ingredients = dbRequests.getIngredientsForCategory(call.data, userId)
        keyboardTEMP = types.InlineKeyboardMarkup(row_width=2)
        if len (ingredients)>0:
            for ingredient in ingredients:
                keyboardTEMP.row(types.InlineKeyboardButton(text=ingredient[1], callback_data=ingredient[0]))
            keyboardTEMP.row(kb.backCat)
            USER_STATUS[userId] = 'choosing_ingredient'
            bot.edit_message_text(chat_id=userId, message_id=call.message.message_id,text='Нажмите на продукт, чтобы добавить:', reply_markup=keyboardTEMP)
        else:
            keyboardTEMP.row(kb.backCat)
            bot.edit_message_text(chat_id=userId, message_id=call.message.message_id, text='Все ингредиенты из этой категории уже добавлены!', reply_markup=keyboardTEMP)


    elif (userId in USER_STATUS and USER_STATUS[userId] == 'choosing_ingredient'):
        # print(call.message.json['reply_markup']['inline_keyboard'])
        r = dbRequests.addInredientToUser(userId, call.data)
        if r:
            keyboardTEMP = types.InlineKeyboardMarkup(row_width=2)
            for btn in call.message.json['reply_markup']['inline_keyboard']:
                if btn[0]['callback_data'] != call.data:
                    keyboardTEMP.row(types.InlineKeyboardButton(text=btn[0]['text'], callback_data=btn[0]['callback_data']))

            bot.edit_message_text(chat_id=userId, message_id=call.message.message_id, text='Нажмите на продукт, чтобы добавить:',reply_markup=keyboardTEMP)
    elif (userId in USER_STATUS and USER_STATUS[userId] == 'del_ingredient'):
        r = dbRequests.delIngedientToUser(userId, call.data)
        if r:
            keyboardTEMP = types.InlineKeyboardMarkup(row_width=2)
            for btn in call.message.json['reply_markup']['inline_keyboard']:
                if btn[0]['callback_data'] != call.data:
                    keyboardTEMP.row(
                        types.InlineKeyboardButton(text=btn[0]['text'], callback_data=btn[0]['callback_data']))
            bot.edit_message_text(chat_id=userId, message_id=call.message.message_id,text='Нажмите на продукт, чтобы удалить:', reply_markup=keyboardTEMP)
        else:
            bot.send_message(userId, 'Произошла ошибка при удалении', reply_markup=kb.keyboardMain)
    elif (userId in USER_STATUS and USER_STATUS[userId] == 'add_ingredient_for_recipe'):
        r = dbRequests.addIngredintForRecipe(newRecipe['Id'], call.data)
        if r:
            keyboardTEMP = types.InlineKeyboardMarkup(row_width=2)
            for btn in call.message.json['reply_markup']['inline_keyboard']:
                if btn[0]['callback_data'] != call.data:
                    keyboardTEMP.row(
                        types.InlineKeyboardButton(text=btn[0]['text'], callback_data=btn[0]['callback_data']))
            bot.edit_message_text(chat_id=userId, message_id=call.message.message_id,
                                  text='Нажмите на продукт, чтобы удалить:', reply_markup=keyboardTEMP)
        else:
            bot.send_message(userId, 'Произошла ошибка при добавления', reply_markup=kb.keyboardMain)
    elif (len(call.data) > 0 and userId in userInfo):
        if (call.data == 'right'):
            if userInfo[userId]['page'] < userInfo[userId]['maxPage']:
                keyboardTEMP = types.InlineKeyboardMarkup(row_width=2)
                userInfo[userId]['page'] += 1
                for item in userInfo[userId]['recipes'][str(userInfo[userId]['page'])]:
                    keyboardTEMP.add(types.InlineKeyboardButton(text=item['title'], callback_data=item['id']))

                keyboardTEMP.row(kb.left, types.InlineKeyboardButton(
                    text=f"{userInfo[userId]['page']}/{userInfo[userId]['maxPage']}", callback_data='center'), kb.right)
                keyboardTEMP.row(kb.back)
                bot.edit_message_text(chat_id=userId, message_id=call.message.message_id, text='Доступные блюда:',
                                      reply_markup=keyboardTEMP)
        elif (call.data == 'left'):
            if userInfo[userId]['page'] > 1:
                keyboardTEMP = types.InlineKeyboardMarkup(row_width=2)
                userInfo[userId]['page'] -= 1
                for item in userInfo[userId]['recipes'][str(userInfo[userId]['page'])]:
                    keyboardTEMP.add(types.InlineKeyboardButton(text=item['title'], callback_data=item['id']))
                keyboardTEMP.row(kb.left, types.InlineKeyboardButton(
                    text=f"{userInfo[userId]['page']}/{userInfo[userId]['maxPage']}", callback_data='center'), kb.right)
                keyboardTEMP.row(kb.back)
                bot.edit_message_text(chat_id=userId, message_id=call.message.message_id, text='Доступные блюда:',
                                      reply_markup=keyboardTEMP)
        else:
            print(userInfo[userId]['recipes'][str(userInfo[userId]['page'])])
            for item in userInfo[userId]['recipes'][str(userInfo[userId]['page'])]:
                if (int(call.data) == item['id']):
                    r = dbRequests.getRecipe(int(item['id']))
                    title = r[1]
                    desc = r[2]
                    cTime = r[3]
                    videoLink = r[4]
                    bot.send_message(userId, f"*{title} ({cTime})*\n\n{desc}\n{videoLink}", parse_mode="Markdown",
                                     reply_markup=kb.keyboardMain)
    bot.answer_callback_query(call.id)





if __name__ == '__main__':
    print("TgBot started")
    bot.polling(none_stop=True, interval=1);
