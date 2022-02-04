# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import json
import datetime
import requests
from bs4 import BeautifulSoup as BS

tdate = datetime.date.today()

def getTodaysNews():
    h = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    }
    # Get news from api
    req = requests.get("https://www.zakon.kz/api/all-news-ajax/?pn=1&pSize=100", headers=h)
    # Convert into json
    data = json.loads(req.text)
    # Create list for storage links of each news
    news = []
    # Get all links of news
    for n in data.get("data_list"):
        if n.get("data") == str(tdate):
            for link in n.get("news_list"):
                news.append(link.get("alias"))

    # Get info from news with sending a links
    total = getNewsInfo(news)

    # Create/write JSON file to storage data
    with open("data.json", "w", encoding='utf-8') as file:
        json.dump(total, file, indent=4, ensure_ascii=False)

def getNewsInfo(news_list):
    returnData = []
    for link in news_list:
        # Send request to each link of news and get html content of page
        r = requests.get(f'https://www.zakon.kz/{link}')
        html = BS(r.content, "html.parser")

        # Start to find each needed element from html
        articleBlock = html.find("div", "articleBlock")

        title = articleBlock.select("h1")[0].text
        publishedDate = articleBlock.select(".date")[0].text
        comments = articleBlock.select(".comments")
        # Let's count the comments number, but as there were not any comments it will be always zero
        commentsCounter = 0
        for el in comments:
            if el.select(".title") is not None:
                commentsCounter += 1

        # To get all content from article, we had to find all tags from content class for example due to different font
        c = articleBlock.find("div", class_="content").findAll(['p', 'a', 'span', 'blockquote'])
        content = ""
        for e in c:
            content += e.text

        returnData.append({
            "Заголовок: ": title,
            "Контент:": content,
            "Дата публикации:": publishedDate,
            "Количество комментариев:": commentsCounter
        })

    return returnData


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    getTodaysNews()
    # print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
