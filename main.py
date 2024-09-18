import gspread
import requests
from google.oauth2.service_account import Credentials
from datetime import date, timedelta, datetime


scope = ['https://www.googleapis.com/auth/spreadsheets']
sheet_id = 'sheet_id'

url_exchange_api = 'https://api.privatbank.ua/p24api/exchange_rates?json'


def data_from_json(update_from: str, update_to: str) -> list[dict] or None:
    start_date = datetime.strptime(update_from, '%d.%m.%Y')
    end_date = datetime.strptime(update_to,'%d.%m.%Y')
    time_period = (end_date - start_date).days

    result = []

    info_by_date = {}
    for _day in range(time_period + 1):
        user_date = (start_date + timedelta(days=_day)).strftime('%d.%m.%Y')
        response = requests.get(url=url_exchange_api, params={'date': user_date})

        if response.status_code == 200:
            json_response = response.json()
            info_by_date[json_response["date"]] = json_response
        else:
            print(f"Error fetching data for {user_date}: {response.status_code}")

    return info_by_date


def access_to_spreadsheets(json_response):
    creds = Credentials.from_service_account_file('credentials.json', scopes=scope)
    authorise = gspread.authorize(creds)
    open_sheets = authorise.open_by_key(sheet_id)
    sheets_to_update = open_sheets.worksheet('Sheet1')
    sheets_to_update.clear()

    headers = [['Date', 'Currency', 'Sale Rate NB', 'Purchase Rate NB', 'Sale Rate', 'Purchase Rate']]
    sheets_to_update.update(headers, 'A1:F1')

    # _date = json_response['date']
    rows = []
    for _date, info in json_response.items():
        rates = info['exchangeRate']
        for rate in rates:
            currency = rate.get('currency')
            sale_rate_nb = rate.get('saleRateNB')
            purchase_rate_nb = rate.get('purchaseRateNB')
            sale_rate = rate.get('saleRate', '')
            purchase_rate = rate.get('purchaseRate', '')

            rows.append([_date, currency, sale_rate_nb, purchase_rate_nb, sale_rate, purchase_rate])

    sheets_to_update.update(rows, 'A2:F{}'.format(len(rows) + 1))


def convert_date(input_date: str | None) -> str:
    if not input_date:
        current_date = datetime.now().strftime('%d.%m.%Y')
        return current_date

    return datetime.fromisoformat(input_date).strptime(input_date, '%Y-%m-%d').strftime('%d.%m.%Y')


def main():
    _update_from = input("Enter the starting date in YYYY-MM-DD format: ")
    _update_to = input("Enter the end date in YYYY-MM-DD format: ")
    update_from = convert_date(_update_from)
    update_to = convert_date(_update_to)
    from_json = data_from_json(update_from, update_to)
    access_to_spreadsheets(from_json)
    print("Successfully updated the spreadsheets")


if __name__ == '__main__':
    main()

