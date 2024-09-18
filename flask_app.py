from datetime import date
from asgiref.wsgi import WsgiToAsgi
from flask import Flask, request

from main import data_from_json, access_to_spreadsheets, convert_date

app = Flask(__name__)


@app.get("/exchange_rate")
def update_data():
    update_from = request.args.get('update_from', None)
    update_to = request.args.get('update_to', None)
    from_json = data_from_json(convert_date(update_from), convert_date(update_to))
    access_to_spreadsheets(from_json)
    return f"Updated the data for range from {update_from or date.today()} to {update_to or date.today()}"


asgi_app = WsgiToAsgi(app)
