import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message


tmdb_api_key = "f830b3e2c32aaae83c99d6a3ad5c7ef3"

@Client.on_message(filters.command("poster"))
async def poster_handler(client, message):
  """
  This handler will process messages starting with /poster and download a movie poster.
  It uses TMDb API to fetch the poster URL based on movie title.
  """
  try:
    movie_title = message.text.split(" ", 1)[1]
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_api_key}&query={movie_title}"
    response = requests.get(search_url)
    response.raise_for_status()
    data = response.json()
    poster_path = data["results"][0]["poster_path"]
    poster_url = f"https://image.tmdb.org/t/p/w780{poster_path}"
    response = requests.get(poster_url, stream=True)
    response.raise_for_status()
    filename = poster_url.split("/")[-1]
    with open(filename, "wb") as f:
      for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
    await message.reply_document(filename)
    os.remove(filename)
  except requests.exceptions.RequestException as e:
    await message.reply(f"Error: {e}")
  except IndexError:
    await message.reply(f"Movie not found: '{movie_title}'")
