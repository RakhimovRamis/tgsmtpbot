from telebot.async_telebot import AsyncTeleBot
import asyncio
import smtp

TOKEN = smtp.config['TOKEN']

bot = AsyncTeleBot(TOKEN)

@bot.message_handler(commands=['start'])
async def send_welcome(message):
	await bot.send_message(message.chat.id, "Привет")

@bot.message_handler(func=lambda message: message.text.lower() == 'письмо')
async def send_email_text(message):
	await bot.send_message(message.chat.id, 'Письмо отправлено')
	cormail = smtp.send_mail('Новое сообщение','example@yandex.ru', f'<p>User ID {message.from_user.id}</p>')
	asyncio.gather(asyncio.create_task(cormail))

@bot.message_handler(content_types=['document'])
async def send_email_document(message):
	await bot.send_message(message.chat.id, 'Файл отправлен')
	document_id = message.document.file_id
	file_info = await bot.get_file(document_id)
	url_file = f'http://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}'
	cormail = smtp.send_mail('Новое сообщение',
                            'example@yandex.ru',
                            f'<p>Файл отправлен пользователем ID{message.from_user.id}</p>',
                            url_file)
	asyncio.gather(asyncio.create_task(cormail))

asyncio.run(bot.polling())