from pyrogram import Client, filters
from pyrogram.types import Message
from bs4 import BeautifulSoup
import requests


@Client.on_message(filters.command("poster"))
async def poster(client, message):
    movie_name = message.text.split(" ", 1)[1].strip()  # Get movie name from command
    search_url = f"https://www.google.com/search?q={movie_name}+landscape+poster&tbm=isch&tbs=isz:l"
    
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find the first image
    image_tag = soup.find("img", {"class": "rg_i Q4LuWd"})
    
    if image_tag:
        image_url = image_tag["src"]
        await message.reply_photo(image_url)
    else:
        await message.reply("Couldn't find a poster for that movie.")
