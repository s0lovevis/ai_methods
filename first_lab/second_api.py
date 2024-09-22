import requests


def call_second_api(user_text):

    url = "https://sentiment-analyzer3.p.rapidapi.com/Sentiment"

    querystring = {"text": user_text}

    headers = {
        "x-rapidapi-key": "9b8410daa8msh3cacb37a08e9e76p13691ejsn9589d3ec3c26",
        "x-rapidapi-host": "sentiment-analyzer3.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring).json()

    final_answer = {'pos': response['pos'], 'neg': response['neg'], 'neu': response['neu']}

    final_answer['pos'] = round(100*final_answer['pos'], 1)
    final_answer['neg'] = round(100*final_answer['neg'], 1)
    final_answer['neu'] = round(100*final_answer['neu'], 1)

    return final_answer