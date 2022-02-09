from telebot import types

keyboardMain = types.ReplyKeyboardMarkup(True)
keyboardMain.row("Подобрать рецепты",'Мои продукты','Случайный рецепт')
keyboardMain.row('Инструкция', 'Тех.Поддержка', 'Донаты')

keyboardUser = types.ReplyKeyboardMarkup(True)
keyboardUser.row("Добавить продукт", 'Мои продукты','Удалить продукт')
keyboardUser.row('◀️ Назад')


left= types.InlineKeyboardButton(text='<', callback_data='left');
right= types.InlineKeyboardButton(text='>', callback_data='right');
back= types.InlineKeyboardButton(text='◀️ Назад', callback_data='back');
done= types.InlineKeyboardButton(text='✅️ Готово', callback_data='back');


backCat = types.InlineKeyboardButton(text="◀️ Назад", callback_data='backCat')



# Мясные продукты - курица, индейка, свинина, говядина, мясной фарш, колбаса/сосиски
# Макароны/Крупы - макароны, спагетти,греча, рис
# Овощи - картофель, морковь, свекла, лук репчатый, чеснок, томаты, огурцы, блог.перец
# Молочные продукты - молоко, творог, твёрдый сыр, мягкий сыр
# Соус - томатная паста, кетчуп, майонез, сметана
# Другое - рыба, грибы, хлеб, куриные яйца

# {'game_short_name': None, 'chat_instance': '709525513141476307', 'id': '1984564824781569095',
#  'from_user': {'id': 462067505, 'is_bot': False, 'first_name': 'Artem', 'username': 'artmiptv', 'last_name': 'Ipatov', 'language_code': 'en', 'can_join_groups': None,
#                'can_read_all_group_messages': None, 'supports_inline_queries': None},
#  'message': {'content_type': 'text', 'message_id': 1607, 'from_user': <telebot.types.User object at 0x0000024C7583ED30>, 'date': 1643384926, 'chat': <telebot.types.Chat object at 0x0000024C75E0DF70>, 'forward_from': None, 'forward_from_chat': None, 'forward_from_message_id': None, 'forward_signature': None, 'forward_date': None, 'reply_to_message': None, 'edit_date': 1643384930, 'media_group_id': None, 'author_signature': None, 'text': 'Нажмите на продукт, чтобы добавить:', 'entities': None, 'caption_entities': None, 'audio': None, 'document': None, 'photo': None, 'sticker': None, 'video': None, 'video_note': None, 'voice': None, 'caption': None, 'contact': None, 'location': None, 'venue': None, 'animation': None, 'dice': None, 'new_chat_member': None, 'new_chat_members': None, 'left_chat_member': None, 'new_chat_title': None, 'new_chat_photo': None, 'delete_chat_photo': None, 'group_chat_created': None, 'supergroup_chat_created': None, 'channel_chat_created': None, 'migrate_to_chat_id': None, 'migrate_from_chat_id': None, 'pinned_message': None, 'invoice': None, 'successful_payment': None, 'connected_website': None, 'json': {'message_id': 1607, 'from': {'id': 2129987678, 'is_bot': True, 'first_name': 'Бот "Easy Menu"', 'username': 'easy_menu_bot'}, 'chat': {'id': 462067505, 'first_name': 'Artem', 'last_name': 'Ipatov', 'username': 'artmiptv', 'type': 'private'}, 'date': 1643384926, 'edit_date': 1643384930, 'text': 'Нажмите на продукт, чтобы добавить:', 'reply_markup': {'inline_keyboard': [[{'text': 'Курица', 'callback_data': '1'}], [{'text': 'Индейка', 'callback_data': '2'}], [{'text': 'Свинина', 'callback_data': '3'}], [{'text': 'Говядина', 'callback_data': '4'}], [{'text': 'Мясной фарш', 'callback_data': '5'}], [{'text': 'Колбаса/сосиски', 'callback_data': '6'}]]}}}, 'data': '1', 'inline_message_id': None}
