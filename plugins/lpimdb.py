from pyrogram import Client, filters
from pyrogram.types import Message
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

# Replace with your bot token and API ID
@Client.on_message(filters.command("poster"))
async def poster(client, message):
  movie_name = message.text.split(" ", 1)[1]
  search_url = f"https://www.google.com/search?q={movie_name}+landscape+poster&tbm=isch&tbs=isz:l"

  try:
    response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all image results and filter for high quality, size, and landscape orientation
    image_results = soup.find_all('img', {'class': 'rg_i Q4LuWd'})
    high_quality_images = [
      img['src'] for img in image_results
      if 'jpg' in img['src'] or 'png' in img['src']
      and 'https://' in img['src']
      and urlparse(img['src']).netloc != 'encrypted-tbn0.gstatic.com'
      and int(img.get('width', 0)) > 500 
      and int(img.get('height', 0)) > 300
      and int(img.get('width', 0)) / int(img.get('height', 0)) > 1.2 # Aspect ratio check
      and ('landscape' in img.get('alt', '').lower() or 
         'poster' in img.get('alt', '').lower() or 
         'movie poster' in img.get('alt', '').lower()) # Keyword check in alt text
    ]

    if high_quality_images:
      # Send the first high-quality image found
      await client.send_photo(message.chat.id, high_quality_images[0], caption=f"Poster for: {movie_name}")
    else:
      await client.send_message(message.chat.id, "No high-quality landscape posters found.")
  except Exception as e:
    await client.send_message(message.chat.id, f"Error: {e}")

