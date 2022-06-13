import requests
import bs4
import smtplib
import os


URL = "https://www.amazon.com/TheraBand-Resistance-Non-Latex-Professional-Dispenser/dp/B019OOBYH0/ref=sr_1_6?crid=2NAI7P1CUME6A&keywords=theraband+gold&qid=1655148036&s=sporting-goods&sprefix=theraband+gold%2Csporting%2C105&sr=1-6"
FROM_EMAIL = os.environ.get("FROM_EMAIL")
AUTH_CODE = os.environ.get("AUTH_CODE")
TO_EMAIL = os.environ.get("TO_EMAIL")
PRICE_LIMIT = 105.00


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


#Get Product Name
product_name_selector = ".product-title-word-break"
product_name = soup.select_one(selector=product_name_selector).get_text()


#Send email if price is below PRICE_LIMIT
if price < PRICE_LIMIT:
    try:
        with smtplib.SMTP("smtp.mail.yahoo.com", port=587) as smtp_connection:
            smtp_connection.starttls()
            print(smtp_connection.login(user=FROM_EMAIL, password=AUTH_CODE))
            smtp_connection.sendmail(from_addr=FROM_EMAIL,
                                     to_addrs=TO_EMAIL,
                                     msg=f"Subject: {product_name} is now only ${price}\n\nHere is the link:\n{URL}")
    except Exception as error_message:
        print(f"Something Went Wrong In Sending The Email:\n{error_message}")
    else:
        print("Email was sent.")
