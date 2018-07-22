import requests

api_key = 'kjgkjhkjhg'
sender = 'priya'
mobile_number = '8765875876'


def send_message(message):
    response = requests.get(
        url='http://api.msg91.com/api/sendhttp.php?authkey=' + api_key +
            '&mobiles=' + mobile_number + '&message=' + message + '&sender=' +
            sender + '&route=4&country=91')
    print(response.raw)
