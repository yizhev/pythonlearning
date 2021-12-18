import csv
import time
import requests
from lxml import etree


# Douban Top 250 url.
url = "https://movie.douban.com/top250"

# Defining headers.
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
}


# Set the initial paramater.
start = 0
page_num = 1

# Enter the for loop.
for i in range(0, 10):
    param = {
        "start": start,
        "filter": ""
    }

    # GET http response
    response = requests.get(url=url, headers=headers, params=param)

    # Check HTTP conntection. If doesn't work, break.
    status_code = response.status_code
    if status_code != 200:
        print("You need to check the network connection, may be your IP was blocked by Douban.")
        break


    # 解析源代码
    page = response.text

    # Get tree file.
    tree = etree.HTML(page)

    # 获取到包含页面中的电影最小单元
    lists = tree.xpath('//*[@id="content"]/div/div[1]/ol/li')
    print(f"第 {page_num} 页中的中电影元素个数是 {len(lists)}.")


    # Creating a csv file.
    f = open("Top250.csv", mode="a")
    csvwriter = csv.writer(f)


    # Using XPath to obtain the movic elements.
    for item in lists:
        movie_name_zh = item.xpath('./div/div[2]/div[1]/a/span[1]/text()')[0]
        movie_name_origin = item.xpath('./div/div[2]/div[1]/a/span[2]/text()')[0].strip(' / ')
        movie_year = item.xpath('./div/div[2]/div[2]/p[1]/text()[2]')[0].strip()[0:4]
        movie_rating = item.xpath('./div/div[2]/div[2]/div/span[2]/text()')[0]
        movie_rated_num = item.xpath('./div/div[2]/div[2]/div/span[4]/text()')[0].strip('人评价')
        movie_short_quote = item.xpath('./div/div[2]/div[2]/p[2]/span[1]/text()')
        movie_link = item.xpath('./div/div[1]/a/@href')[0]

        # List is indexed, better that dic.
        movie_list = [movie_name_zh, movie_name_origin, movie_year, movie_rating, movie_rated_num, movie_short_quote, movie_link]
        csvwriter.writerow(movie_list)


    # To remind.
    print(f"Getting Top 250 lists from {start + 1} to {start + 25}")

    # Increasing param by 25
    start += 25
    page_num += 1

    # Make code more like human.
    print("Sleep six seconds here.\n")
    time.sleep(6)

    # Close file.
    f.close()

# Close connection.
response.close()