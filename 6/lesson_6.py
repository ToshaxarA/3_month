import schedule, requests

def send_message():
    print("Здравствуйте, ребята, у вас сегодня урок в 19:00")

def two_send_message():
    print("Здравствуйте, ребята, у вас сегодня урок в 19:00")


def get_price_btc():
    print("Price BTC...")
    response = requests.get('https://yobit.net/api/3/ticker/btc_usd').json()
    print(f"{response['btc_usd']['last']}$")
    
def main():
    # schedule.every(1).minutes.do(send_message)
    # schedule.every(1).minutes.do(two_send_message)
    # schedule.every().day.at('20:23').do(two_send_message)
    # schedule.every().saturday.at('20:25:01').do(get_price_btc).at
    schedule.every(5).seconds.do(get_price_btc)
    while True:
        schedule.run_pending()






main()

