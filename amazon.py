from bs4 import BeautifulSoup
import pandas as pd

import re
import requests

def asin_cost_get(target_seller_id):
    target_url = "https://www.amazon.co.jp/shops/" + target_seller_id
    target_html = requests.get(target_url).text

    soup = BeautifulSoup(target_html, "html.parser")

    div_soup = soup.find("div", attrs={"id":"pagn"})
    spans_soup = [tag.text for tag in div_soup.find_all("span") if re.match("[0-9]+", tag.text)]
    pages = int(spans_soup[-1])

    print("ストアが", pages, "ページあります。")

    matrix = []

    for page in range(1, pages+1):

        print("現在", page, "ページ目のデータを取得しています。")

        target_url = "https://www.amazon.co.jp/s?me=" + target_seller_id + "&page=" + str(page)
        target_html = requests.get(target_url).text

        soup = BeautifulSoup(target_html, "html.parser")

        target_ul = soup.find("ul", attrs={"id":"s-results-list-atf"})
        target_lis = soup.find_all("li", attrs={"class": "s-result-item s-result-card-for-container-noborder s-carded-grid celwidget"})

        for target_li in target_lis:
            target_asin = target_li["data-asin"]
            try:
                target_cost = target_li.find("span", attrs={"class": "a-size-base a-color-price a-text-bold"}).text
            except:
                target_cost = ""

            matrix.append([target_asin, re.sub("[^0-9]", "", target_cost)])

    df = pd.DataFrame(matrix, columns=['ASINコード', '価格'])
    df.to_csv(target_seller_id+".csv", index=False)




if __name__ == "__main__":

    target_seller_id = "A8YML2VFG726S"
    asin_cost_get(target_seller_id)

    target_seller_id = "A3EPCIEUK00YCH"
    asin_cost_get(target_seller_id)
