from json import dumps

from requests import request

from config import RAPIDAPI_API_KEY


URL = 'https://deep-translate1.p.rapidapi.com/language/translate/v2'
HEADERS = {
    'content-type': 'application/json',
    'x-rapidapi-key': RAPIDAPI_API_KEY,
    'x-rapidapi-host': 'deep-translate1.p.rapidapi.com'
}
REPHRASING_LANG = 'es'


def rephrase(sentence: str) -> str:
    if not RAPIDAPI_API_KEY:
        print('Omiting translation - no api key')
        return sentence

    try:
        response = request(
            method='POST',
            url=URL,
            data=dumps({
                'q': sentence,
                'source': 'en',
                'target': REPHRASING_LANG
            }),
            headers=HEADERS
        )

        response = request(
            method='POST',
            url=URL,
            data=dumps({
                'q': response.json()
                ['data']['translations']['translatedText'],
                'source': REPHRASING_LANG,
                'target': 'en'
            }),
            headers=HEADERS
        )

        rephrased = response.json()['data']['translations']['translatedText']

        print('Rephrased successfully')

        return rephrased

    except Exception as e:
        print('Translation error or quota exceeded', str(e))
        return sentence
