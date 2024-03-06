#from googletrans import Translator
from googleapiclient import discovery
import json

#from json import JSONDecodeError

API_KEY = 'AIzaSyCpIwsWdQ9v5Wvud2U-dluDz6BxOWwOSmA'


if __name__ == '__main__':
    #translator = Translator()
    #language = translator.detect("Andorid端实时车牌识别Realtime chinese plate recoginition on android")
    #print(language)
    #if language.lang == 'en':
    #    print("true")
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=API_KEY,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': '基于卷积神经网络APP The number gestures recognition Android APP based on convolutional neural network(CNN), which can recognize the gestures corresponding number 0 to 10）'},
        'requestedAttributes': {'TOXICITY': {}},
        'languages': ['en']
    }

    response = client.comments().analyze(body=analyze_request).execute()
    print(response['detectedLanguages'])