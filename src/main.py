
import os
import logging
import httpx
import urllib.parse
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def scrape(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a URL to scrape.")
        return

    url = context.args[0]
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            await context.bot.send_message(chat_id=update.effective_chat.id, text=response.text[:4096])
    except httpx.RequestError as exc:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"An error occurred while requesting {exc.request.url!r}.")
    except httpx.HTTPStatusError as exc:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")

async def scrape_images(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a URL to scrape.")
        return

    url = context.args[0]
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')

        for img_tag in img_tags:
            img_url = img_tag.get('src')
            if img_url:
                img_url = urllib.parse.urljoin(url, img_url)
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=img_url)

    except httpx.RequestError as exc:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"An error occurred while requesting {exc.request.url!r}.")
    except httpx.HTTPStatusError as exc:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")

async def scrape_posts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a URL to scrape.")
        return

    url = context.args[0]
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        posts = []
        for post in soup.find_all(['h1', 'h2', 'h3']):
            title = post.get_text()
            link = post.find('a')
            if link:
                link = urllib.parse.urljoin(url, link.get('href'))
                posts.append(f"{title} - {link}")

        if posts:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='\n'.join(posts))
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="No posts found.")

    except httpx.RequestError as exc:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"An error occurred while requesting {exc.request.url!r}.")
    except httpx.HTTPStatusError as exc:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")

def main():
    # Get the token from the environment variable
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    if not TOKEN:
        print("Please set the TELEGRAM_TOKEN environment variable.")
        return

    # Create the Application
    application = ApplicationBuilder().token(TOKEN).build()

    # Add the start command handler
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Add the scrape command handler
    scrape_handler = CommandHandler('scrape', scrape)
    application.add_handler(scrape_handler)

    # Add the scrape_images command handler
    scrape_images_handler = CommandHandler('scrape_images', scrape_images)
    application.add_handler(scrape_images_handler)

    # Add the scrape_posts command handler
    scrape_posts_handler = CommandHandler('scrape_posts', scrape_posts)
    application.add_handler(scrape_posts_handler)

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
