import requests
from bs4 import BeautifulSoup
import re
import datetime

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
def parse_movie_detail(html, movie_url):
    soup = BeautifulSoup(html, 'html.parser')
    
    movie_dict = {}
    
    # Get the movie id from URL
    movie_id = movie_url.split('/')[-1]
    print(movie_id)
    movie_dict['movie_id'] = movie_id
    
    # Get movie title
    title_tag = soup.find("h1", itemprop="name")
    title = title_tag.contents[0]
    print(title)
    movie_dict['title'] = title
    
    # Get movie release date
    pub_date_tag = soup.find("span", class_="published")
    # print(pub_date.contents[1])
    s_format = '%Y年%m月%d日'
    pub_date_str = pub_date_tag.contents[1].strip().replace('公開', '')
    pub_date = datetime.datetime.strptime(pub_date_str, s_format)
    print(pub_date)
    movie_dict['pub_date'] = pub_date
    
    # Get description
    description_tag = soup.find("p", itemprop="description")
    description = description_tag.contents[0]
    print(description)
    movie_dict['description'] = description
    
    # TODO: #1 Implement getting movie summary
    # summary_tag = soup.find_all("section","")
    # print(summary_tag[1])
    
    print(movie_dict)
    
    return movie_dict

if __name__ == "__main__":
    url = 'https://www.cinematoday.jp/movie/release/'
    html = get_html(url)
    movie_url_list = parse_movie_url(html)
    
    movie_list = []
    
    for movie_url in movie_url_list:
        html = get_html(movie_url)
        movie_list.append(parse_movie_detail(html, movie_url))
        
    print(movie_list)