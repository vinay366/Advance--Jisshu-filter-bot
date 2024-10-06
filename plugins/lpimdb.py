from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import requests
from bs4 import BeautifulSoup

@Client.on_message(filters.command("imdbposter"))
async def imdb_poster(client, message):
  try:
    # Get the search text and year from the message
    search_text, year = message.text.split(" ", 1)[1].split(" ", 1)

    # Search for the movie on IMDb with year filtering
    response = requests.get(f"https://www.imdb.com/find?q={search_text}+({year})&ref_=nv_sr_sm")
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract the first search result link
    result_link = soup.find("td", class_="result_text").find("a")['href']
    imdb_id = result_link.split('/')[2]

    # Retrieve the movie's page to get poster details
    movie_page = requests.get(f"https://www.imdb.com{result_link}")
    movie_soup = BeautifulSoup(movie_page.text, "html.parser")

    # Find the poster image tag and extract the media view ID
    poster_div = movie_soup.find("div", class_="poster")
    if poster_div:
      poster_tag = poster_div.find("a")
      if poster_tag:
        media_view_id = poster_tag['href'].split("/")[4] 

        # Construct the IMDb URL for landscape poster
        poster_url = f"https://m.imdb.com/title/{imdb_id}/mediaviewer/{media_view_id}/?ref_=tt_ov_i"

        # Verify if the year matches on the result page
        result_page = requests.get(f"https://www.imdb.com{result_link}")
        result_soup = BeautifulSoup(result_page.text, "html.parser")
        title = result_soup.find("h1").text

        if year in title: # Check for year in the title
          # Send the poster
          await message.reply_photo(photo=poster_url, caption=f"IMDb Poster for {title}")
        else:
          await message.reply(f"No matching movie found for {search_text} ({year})")
      else:
        await message.reply(f"No poster found for {search_text} ({year})")
    else:
      await message.reply(f"No poster found for {search_text} ({year})")

  except Exception as e:
    await message.reply(f"Error: {e}")

