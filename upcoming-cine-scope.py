import requests
from bs4 import BeautifulSoup
import re

# Get the HTML of the page from cinema-today
def get_html(url):
    response = requests.get(url)
    # print(response.text)
    return response.text

# Parse the HTML and get the movie URL
def parse_movie_url(html):
    soup = BeautifulSoup(html, 'html.parser')
    movies = soup.find_all(href=re.compile("^/movie/T"))
    movie_url_list = []
    for movie in movies:
        movie_url_list.append("https://www.cinematoday.jp/" + movie.attrs['href'])
    return movie_url_list

# Parse the HTML and get the movie detail
def parse_movie_detail(html):
    soup = BeautifulSoup(html, 'html.parser')
    tutle = soup.find("h1", itemprop="name")
    print(tutle.contents[0])
    pub_date = soup.find("span", class_="published")
    print(pub_date.contents[1])

if __name__ == "__main__":
    url = 'https://www.cinematoday.jp/movie/release/'
    html = get_html(url)
    movie_url_list = parse_movie_url(html)
    for movie in movie_url_list:
        html = get_html(movie)
        parse_movie_detail(html)