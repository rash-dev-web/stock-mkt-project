import requests
from twilio.rest import Client
import os

TWILIO_ACCOUNT_ID = os.environ.get("TWILIO_ACCOUNT_ID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
client = Client(TWILIO_ACCOUNT_ID, TWILIO_AUTH_TOKEN)

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries.
#  e.g. [new_value for (key, value) in dictionary.items()]
stock_parameter = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": "PLTZDGY00LMF7HGU",
}
# https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&apikey=PLTZDGY00LMF7HGU
response = requests.get(url=STOCK_ENDPOINT, params=stock_parameter)
stock_price_list = response.json()

date_wise_data = stock_price_list["Time Series (Daily)"]
yesterday_date = list(date_wise_data)[0]

yesterday_closing_price = [date_wise_data[yesterday_date]["4. close"] for (key, value) in date_wise_data.items()
                           if key == yesterday_date]
print(yesterday_closing_price)

# TODO 2. - Get the day before yesterday's closing stock price
day_before_yesterday_date = list(date_wise_data)[1]
# print(day_before_yesterday_date)
day_before_yesterday_closing_price = [date_wise_data[day_before_yesterday_date]["4. close"] for (key, value)
                                      in date_wise_data.items()
                                      if key == day_before_yesterday_date]
print(day_before_yesterday_closing_price)

# TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20.
#  Hint: https://www.w3schools.com/python/ref_func_abs.asp
# print(yesterday_closing_price[0])
positive_diff = abs(float(yesterday_closing_price[0]) - float(day_before_yesterday_closing_price[0]))
print(positive_diff)

# TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day
#  before yesterday.
percent_diff = (positive_diff / float(day_before_yesterday_closing_price[0])) * 100
print(percent_diff)

# TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
# STEP 2: https://newsapi.org/
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

# TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.

# TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint:
#  https://stackoverflow.com/questions/509211/understanding-slice-notation
news_parameter = {
    "q": COMPANY_NAME,
    "apiKey": "8dbe6a82153e41328e1ff51b3e8b1fec",
}

three_news = 0
if percent_diff > 5:
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameter)
    articles = news_response.json()["articles"]
    article_list = [source for source in articles]

## STEP 3: Use twilio.com/docs/sms/quickstart/python
# to send a separate message with each article's title and description to your phone number.

# TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

    for_message_list = [f"Title: {source['title']}\nDescription: {source['description']}" for source in article_list[:3]]
    print(for_message_list)
    # TODO 9. - Send each article as a separate message via Twilio.

    for message in for_message_list:
        message = client.messages \
                        .create(
                             body=message,
                             from_='+16785821290',
                             to='+917838138645'
                         )

        print(message.status)



# Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
