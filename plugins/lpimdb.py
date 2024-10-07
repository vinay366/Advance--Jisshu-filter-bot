from pyrogram import Client, filters
from pyrogram.types import Message
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re


def get_google_poster_url(movie_name):
  """Tries to extract a landscape poster URL from Google Images."""

  search_url = f"https://www.google.com/search?q={movie_name}+landscape+poster&tbm=isch&tbs=isz:l"
  headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
  }

  try:
    response = requests.get(search_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find image elements with specific class names
    image_elements = soup.find_all(
      'img',
      attrs={'src': True, 'alt': True, 'data-src': True},
      class_=['rg_i', 'yWs4tf'] # Common classes for Google image results
    )

    if image_elements:
      # Try to find the most likely landscape image by checking for aspect ratio
      for element in image_elements:
        if 'data-src' in element.attrs:
          url = element['data-src']
        else:
          url = element['src']

        # Extract width and height from the URL (if present)
        match = re.search(r'w(\d+)-h(\d+)', url)
        if match:
          width = int(match.group(1))
          height = int(match.group(2))
          if width > height: # Landscape
            return url

      # If no clear landscape found, return the first poster
      return image_elements[0]['src']
    else:
      return "No landscape posters found on Google Images."

  except requests.exceptions.RequestException as e:
    return f"Error fetching images: {e}"

@Client.on_message(filters.command(["poster"]))
async def movie_poster(client, message):
  movie_name = message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else None

  if movie_name:
    poster_url = get_google_poster_url(movie_name)
    if poster_url:
      await client.send_photo(message.chat.id, poster_url, caption=f"Here's a landscape poster for {movie_name}")
    else:
      await message.reply_text(poster_url) # Send the error message as text
  else:
    await message.reply_text("Please provide a movie name after the /poster command.")
