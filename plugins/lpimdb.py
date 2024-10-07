from pyrogram import Client, filters
from pyrogram.types import Message
import requests
from bs4 import BeautifulSoup


@Client.on_message(filters.command(["poster"]))
async def landscape_poster(client, message):
    query = message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else "landscape"

    url = f"https://www.bing.com/images/search?q={query}&qft=+filterui:aspect-w4h3+filterui:license-public&form=HDRSC2"

    headers = {
        "User -Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find image elements that are likely posters
        image_elements = soup.find_all('img', attrs={'src': True})

        # Filter out image elements that aren't likely posters
        poster_elements = [
            element 
            for element in image_elements
            if element['src'].startswith("https://")  # Ensure the src attribute is a direct URL
        ]

        if poster_elements:
            image_url = poster_elements[0]['src']  # Take the first matching element
            await client.send_photo(message.chat.id, image_url, caption="Here's a high-quality landscape poster from Bing!")
        else:
            await message.reply_text("No landscape posters found on Bing for this query.")
    except requests.exceptions.RequestException as e:
        await message.reply_text(f"Error fetching image: {e}")
