# Telegram Web Scraper

This is a Telegram bot that can be used to scrape information from the web.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Python 3.10 or higher
* pip
* virtualenv

### Installing

1. Clone the repository:
```
git clone https://github.com/0xYur3i/telegram-web-scraper.git
```
2. Create a virtual environment:
```
python3 -m venv venv
```
3. Activate the virtual environment:
```
source venv/bin/activate
```
4. Install the dependencies:
```
pip install -r requirements.txt
```
5. Get your Telegram Bot Token from BotFather.
6. Set the `TELEGRAM_TOKEN` environment variable:
```
export TELEGRAM_TOKEN=<your_token>
```
7. Run the bot:
```
python src/main.py
```

## Usage

The bot has the following commands:

* `/start`: Starts the bot.
* `/scrape <url>`: Scrapes the given URL and returns the content.
* `/scrape_images <url>`: Scrapes the given URL and returns the images.
* `/scrape_posts <url>`: Scrapes the given URL and returns the title and the link of the posts.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.