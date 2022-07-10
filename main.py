from twilio.rest import Client
import requests
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "DV6AILHWDIB1SIMR"
NEWS_API_KEY = "8221a9c27f654158bb6c82b7523fc66d"

TWILLIO_SID = "AC8b32e8b2dc9c0768302040542bec78a5"
TWILLIO_AUTH_TOKEN = "c06ded08aaa7df0c2559183c5b43169f"
    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_params = {
	"function": "TIME_SERIES_DAILY",
	"symbol": STOCK_NAME,
	"apikey": STOCK_API_KEY
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
print(response.json())
data = response.json()["Time Series (Daily)"]
data_list = [value for (key,value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

day_before_yesterday = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday["4. close"]
print(day_before_yesterday_closing_price)

difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
print(difference)

difference_percentage = (difference/float(yesterday_closing_price)) * 100
print(difference_percentage)

if difference_percentage > 2:
	news_params={
		"apiKey": NEWS_API_KEY,
		"qInTitle": COMPANY_NAME
	}
	new_response = requests.get(NEWS_ENDPOINT, params=news_params)
	articles = new_response.json()["articles"]

	three_article = articles[:3]
	print(three_article)
	formated_articles = [f"Headline: {articles['title']}. \nBrief: {articles['description']}" for articles in three_article]
	client = Client(TWILLIO_SID, TWILLIO_AUTH_TOKEN)


	for articles in formated_articles:
		message = client.messages.create(
			body=articles,
			from_='+19382382901',
			to='+420605026890')

	print(message.status)