import requests
import bs4


URL = "https://www.amazon.com/gp/product/B019OOBYH0/ref=ox_sc_act_title_1?smid=ATVPDKIKX0DER&psc=1"


#Get Amazon Response to Request
parameters = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
}

amazon_response = requests.get(url=URL, headers=parameters)

print(amazon_response)


#Create BeautifulSoup Object
amazon_html = amazon_response.text

soup = bs4.BeautifulSoup(amazon_html, "html.parser")


#Get Price of Item
dollar_selector = ".a-price-whole"
cent_selector = ".a-price-fraction"

dollars = float(soup.select_one(selector=dollar_selector).get_text())
print(dollars)
cents = int(soup.select_one(selector=cent_selector).get_text()) / 100
print(cents)
price = dollars + cents
print(price)



