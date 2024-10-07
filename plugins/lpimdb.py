import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from bs4 import BeautifulSoup
from PIL import Image

@Client.on_message(filters.command("poster"))
async def poster_handler(client, message):
  """
  This handler will process messages starting with /poster and download a movie poster.
  It uses Bing Images to search for high-quality posters.
  """
  try:
    movie_title = message.text.split(" ", 1)[1]
    search_term = f"{movie_title} movie poster high resolution official"

    # Search Bing Images
    bing_search_url = f"https://www.bing.com/images/search?q={search_term}&qft=+filterui:imagesize-large"
    response = requests.get(bing_search_url, headers={'User-Agent': 'Mozilla/5.0'})
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the first image link 
    img_tag = soup.find('a', {'class': 'ius_s'}) # Adjust selector if needed
    if img_tag is not None:
      img_link = img_tag['href'] # Extract the href attribute
      img_link = img_link.split("&")[0] # Get the base URL part of the link

      # Download the image
      response = requests.get(img_link, stream=True)
      response.raise_for_status()
      filename = img_link.split("/")[-1]
      with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
          f.write(chunk)

      # Check aspect ratio and send
      img = Image.open(filename)
      width, height = img.size
      if width / height > 1.0: # Landscape aspect ratio
        await message.reply_document(filename)
        os.remove(filename)
        return # Success, stop searching

      os.remove(filename) # Delete if not landscape

    # If no suitable landscape poster found, try smaller sizes
    for size in ["medium", "small"]: # Try medium and small images
      bing_search_url = f"https://www.bing.com/images/search?q={search_term}&qft=+filterui:imagesize-{size}"
      response = requests.get(bing_search_url, headers={'User-Agent': 'Mozilla/5.0'})
      response.raise_for_status()

      soup = BeautifulSoup(response.content, 'html.parser')
      img_tag = soup.find('a', {'class': 'ius_s'})
      if img_tag is not None:
        img_link = img_tag['href']
        img_link = img_link.split("&")[0]
        response = requests.get(img_link, stream=True)
        response.raise_for_status()
        filename = img_link.split("/")[-1]
        with open(filename, "wb") as f:
          for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

        img = Image.open(filename)
        width, height = img.size
        if width / height > 1.0: # Landscape aspect ratio
          await message.reply_document(filename)
          os.remove(filename)
          return # Success, stop searching

        os.remove(filename) # Delete if not landscape

    await message.reply("No suitable landscape poster found. Please try a different search term.")

  except requests.exceptions.RequestException as e:
    await message.reply(f"Error: {e}")
  except Exception as e: # Catch any other potential errors
    await message.reply(f"An error occurred: {e}")

