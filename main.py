# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import json
import datetime
import requests
from bs4 import BeautifulSoup as BS

tdate = datetime.date.today()

def get_todays_news():
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    }
    # Get news from api
    response = requests.get("https://www.zakon.kz/api/all-news-ajax/?pn=1&pSize=100", headers=headers)
    # Convert into json
    data = json.loads(response.text)
    # Create list for storage links of each news
    news = []
    # Get all links of news
    for n in data.get("data_list"):
        if n.get("data") == str(tdate):
            for link in n.get("news_list"):
                news.append(link.get("alias"))

    # Get info from news with sending a links
    total = get_news_info(news)

    # Create/write JSON file to storage data
    with open("data.json", "w", encoding='utf-8') as file:
        json.dump(total, file, indent=4, ensure_ascii=False)


def get_news_info(news_list):
    return_data = []
    for link in news_list:
        # Send request to each link of news and get html content of page
        r = requests.get(f'https://www.zakon.kz/{link}')
        html = BS(r.content, "html.parser")

        # Start to find each needed element from html
        article_block = html.find("div", "articleBlock")

        title = article_block.select("h1")[0].text
        published_date = article_block.select(".date")[0].text
        comments = article_block.select(".comments")
        # Let's count the comments number, but as there were not any comments it will be always zero
        comments_counter = 0
        for el in comments:
            if el.select(".title") is not None:
                comments_counter += 1

        # To get all content from article, we had to find all tags from content class for example due to different font
        c = article_block.find("div", class_="content").findAll(['p', 'a', 'span', 'blockquote'])
        content = ""
        for e in c:
            content += e.text

        # Collect all article infos into one
        return_data.append({
            "Заголовок: ": title,
            "Контент:": content,
            "Дата публикации:": published_date,
            "Количество комментариев:": comments_counter
        })

    return return_data


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        get_todays_news()
        print("Success!")
    except:
        print("Something went wrong")
