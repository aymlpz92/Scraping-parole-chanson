
import requests
from pprint import pprint
from bs4 import BeautifulSoup
from collections import Counter
import json


def get_all_urls():
    """Retourne l'url' de chaque chanson d'Aznavour
    """
    
    page_number = 1
    next_page = 1
    links = []
    while next_page < 5:
        print(f"Fetch page {page_number}")
        r = requests.get(f"https://genius.com/api/artists/13060/songs?page={page_number}&sort=popularity")
        if r.status_code == 200:
            response = r.json().get("response", {})
            next_page = response.get("next_page")
            
            songs = response.get("songs")
            for song in songs:
                link = song.get("url")
                artist_name = song.get("artist_names")
                if artist_name == "Charles Aznavour":
                    links.append(link)

            page_number += 1
    print("No more page to fetch")
    return links



def get_lyrics(url):
    
    r = requests.get(url)
    if r.status_code != 200:
        print("Problème avec l'url")
        return []
    
    soup = BeautifulSoup(r.content, 'html.parser')
    div_to_remove = soup.find("div", class_="LyricsHeader__Container-sc-6f4ef545-1 cORuWd")
    
    if div_to_remove:
        div_to_remove.extract()
    lyrics = soup.find("div", class_="Lyrics__Container-sc-68a46031-1 ibbPVY")

    if not lyrics:
        return get_lyrics(url)

    all_words = []
    for sentence in lyrics.stripped_strings:
        for word in sentence.split():
            if "[" not in word and "]" not in word:
                sentence_words = word.strip(",.\"").lower() 
                all_words.append(sentence_words)      
    return all_words



def get_all_words():
    urls = get_all_urls()
    words = []
    for url in urls:
        lyrics = get_lyrics(url=url)
        words.extend(lyrics)

    with open("data.json", "w") as f:
        json.dump(words, f, indent=4)

    # with open("data.json", "r") as f:
    #     words = json.load(f)

    counter = Counter(w for w in words if len(w) > 8)
    most_common_words = counter.most_common(15)
    pprint(most_common_words)


get_all_words()