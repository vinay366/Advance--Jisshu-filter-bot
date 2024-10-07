from pyrogram import Client, filters
from pyrogram.types import Message
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_poster_url(movie_name):
  """Tries to extract the poster URL from BookMyShow for a given movie."""

  base_url = "https://in.bookmyshow.com"
  search_url = f"{base_url}/search/movies?q={movie_name}"

  try:
    response = requests.get(search_url)
    response.raise_for_status() 

    soup = BeautifulSoup(response.text, 'html.parser')

    movie_listing = soup.find('div', class_='movie-listing')
    if movie_listing:
      poster_element = movie_listing.find('img', class_='movie-poster')
      if poster_element:
        poster_url = poster_element['src']
        return urljoin(base_url, poster_url)
      else:
        return "Poster not found for this movie."
    else:
      return "No movie listing found."

  except requests.exceptions.RequestException as e:
    return f"Error fetching data: {e}"

@Client.on_message(filters.command(["poster"]))
async def movie_poster(client, message):
  movie_name = message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else None

  if movie_name:
    poster_url = get_poster_url(movie_name)
    if poster_url:
      await client.send_photo(message.chat.id, poster_url, caption=f"Here's the poster for {movie_name}")
    else:
      await message.reply_text(poster_url) # Send the error message as text
  else:
    await message.reply_text("Please provide a movie name after the /poster command.")


