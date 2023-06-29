import requests
import gnureadline as readline


def run():
    print('small shell to send expressions for yakmachine to evaluate...')
    print('use `exit` to quit or Ctrl-C')
    response = ''
    while response != 'bye!':
        expression = input('yak> ')
        response = (
            requests
            .post('http://localhost:45133/evaluate', json={'expression': expression})
            .json()
            .get('result', '')
        )
        print(response)
