from pyrogram import Client, filters
from pyrogram.types import Message
import requests
from bs4 import BeautifulSoup

@Client.on_message(filters.command(["poster"]))
async def landscape_poster(client, message):
    query = message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else "landscape"
    url = f"https://www.bing.com/images/search?q={query}&qft=+filterui:aspect-w4h3+filterui:license-public"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.text, 'html.parser')

        image_elements = soup.find_all("img", class_="mimg")

        if image_elements:
            image_url = image_elements[0]['src']
            await client.send_photo(message.chat.id, image_url, caption="Here's a landscape poster from Bing!")
        else:
            await message.reply_text("No landscape posters found on Bing for this query.")
    except requests.exceptions.RequestException as e:
        await message.reply_text(f"Error fetching image: {e}")
