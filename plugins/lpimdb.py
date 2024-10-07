import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from PIL import Image # Install PIL (Pillow) library: pip install Pillow

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

  # Prioritize sizes known to be landscape (or larger)
  poster_sizes = ["w1280", "w780", "w500", "w342"]

  for size in poster_sizes:
   poster_url = f"https://image.tmdb.org/t/p/{size}{poster_path}"
   response = requests.get(poster_url, stream=True)
   if response.status_code == 200:
    filename = poster_url.split("/")[-1]
    with open(filename, "wb") as f:
     for chunk in response.iter_content(chunk_size=8192):
      f.write(chunk)

    # Check aspect ratio using PIL
    img = Image.open(filename)
    width, height = img.size
    if width / height > 1.0: # Landscape aspect ratio (width > height)
     await message.reply_document(filename)
     os.remove(filename)
     return # Success, stop searching

    os.remove(filename) # Delete the portrait poster

  await message.reply("No landscape poster found for this movie.")
 except requests.exceptions.RequestException as e:
  await message.reply(f"Error: {e}")
 except IndexError:
  await message.reply(f"Movie not found: '{movie_title}'")
 except Exception as e: # Catch any other potential errors
  await message.reply(f"An error occurred: {e}")
