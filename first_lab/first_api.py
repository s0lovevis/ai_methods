import requests

def call_first_api(user_text):
    
    url = "https://sentiment-analysis9.p.rapidapi.com/sentiment"

    payload = [
        {
            "id": "1",
            "language": "en",
            "text": user_text
        }
    ]
    headers = {
        "x-rapidapi-key": "7c7d5d8398msh3d98ba8e537eaeap1fd852jsn425292850301",
        "x-rapidapi-host": "sentiment-analysis9.p.rapidapi.com",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers).json()[0]['predictions'][0]
    final_answer = {'pos': 1, 'neg': 1}

    if response['prediction'] == 'negative':
        final_answer['neg'] = response['probability']
        final_answer['pos'] = 1 - final_answer['neg']

    else:
        final_answer['pos'] = response['probability']
        final_answer['neg'] = 1 - final_answer['pos']


    final_answer['pos'] = round(100*final_answer['pos'], 1)
    final_answer['neg'] = round(100*final_answer['neg'], 1)

    return final_answer