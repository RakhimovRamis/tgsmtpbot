from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from aiosmtplib import SMTP
import asyncio
from email.mime.application import MIMEApplication
import aiohttp
import io
from dotenv import dotenv_values

config = dotenv_values(".env")

EMAIL = config['EMAIL']
PWD = config['PWD']

async def send_mail(subject, to, msg, url=None):
    message = MIMEMultipart()
    message["From"] = EMAIL
    message["To"] = to
    message["Subject"] = subject
    message.attach(MIMEText(f"<html><body>{msg}</body></html>", "html", "utf-8"))

    if url:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as responce:
                buffer = io.BytesIO(await responce.read())
                part = MIMEApplication(buffer.read(), Name=url.split('/')[-1])
                part['Content-Disposition'] = f'attachment; filename={url.split("/")[-1]}'
        message.attach(part)

    smtp_client = SMTP(hostname="smtp.yandex.ru", port=465, use_tls=True)
    async with smtp_client:
        await smtp_client.login(EMAIL, PWD)
        await smtp_client.send_message(message)

if __name__ == '__main__':
    asyncio.run(send_mail('Тема письма', 'example@yandex.ru', '<h1>Привет</h1>'))