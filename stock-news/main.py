import requests
import math
from newsapi import NewsApiClient
import datetime as dt
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCKAPI_KEY = os.environ.get("STOCKAPI_KEY")
NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY")
TWILIO_AUTH_SID = os.environ.get("TWILIO_AUTH_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_NUM = os.environ.get("TWILIO_NUM")
WHATSAPP_NUM = os.environ.get("WHATSAPP_NUM")

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCKAPI_KEY
}

response = requests.get(STOCK_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()


daily_stock = data["Time Series (Daily)"]


stock_info = list(daily_stock.items())

current_closing_price = float(stock_info[0][1]["4. close"])
previous_closing_price = float(stock_info[1][1]["4. close"])

difference = current_closing_price - previous_closing_price

percentage_difference = round((difference / current_closing_price) * 100)


newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

articles = newsapi.get_everything(
                                    q=COMPANY_NAME,
                                    language='en',
                                    sort_by='relevancy',
                                    page=2
                                    
)

news = articles["articles"][:3]

news_list = []
for article in news:
    title = article["title"]
    description = article["description"]
    news_list.append(title)

print(f"{title}\n{description}")

client = Client(TWILIO_AUTH_SID, TWILIO_AUTH_TOKEN)

if percentage_difference >= 5 or percentage_difference <= -5:
    for title in news_list:
        message = client.messages.create(
            body=f"{STOCK} {percentage_difference}%\nHeadline: {title}\nBrief: {description}",
            from_=f"whatsapp:{TWILIO_NUM}",
            to=f"whatsapp:{WHATSAPP_NUM}"
        )
        
        print(message.sid)

