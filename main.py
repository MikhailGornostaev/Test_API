import re
from flask import Flask, jsonify, request, abort
import requests

app = Flask(__name__)


def rate_parse(cur):
    urls = {
        'USD': 'https://api.exchangerate.host/latest?base=USD&symbols=RUB&places=2',
        'EUR': 'https://api.exchangerate.host/latest?base=EUR&symbols=RUB&places=2',
        'CHF': 'https://api.exchangerate.host/latest?base=CHF&symbols=RUB&places=2',
        'GBP': 'https://api.exchangerate.host/latest?base=GBP&symbols=RUB&places=2',
        'CNY': 'https://api.exchangerate.host/latest?base=CNY&symbols=RUB&places=2'
    }
    chosen_cur = urls[cur]
    resp = requests.get(chosen_cur)
    cur_data = resp.json()
    rate = cur_data['rates']['RUB']
    return rate


@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


@app.errorhandler(405)
def wrong_method(e):
    return jsonify(error=str(e)), 405


@app.route("/ruex", methods=["GET"])
def exchange():
    available_cur = ['USD', 'EUR', 'CHF', 'GBP', 'CNY']
    if request.method == "GET":
        value = request.form.get("value")
        cur = request.form.get("currency")
        if cur in available_cur:
            if value == "":
                abort(400, description="Value field must not be empty")
            elif value.startswith("-"):
                abort(400, description="Value should be a positive number")
            elif re.search(r'[!@#$%^&*()\[\]=+;\'{}\"/A-Za-zА-Яа-я]', value):
                abort(400, description="Value should be a number")
            else:
                value = float(value)
                if cur == 'USD':
                    result = '{:.2f}'.format(value / rate_parse("USD"))
                elif cur == 'EUR':
                    result = '{:.2f}'.format(value / rate_parse("EUR"))
                elif cur == 'CHF':
                    result = '{:.2f}'.format(value / rate_parse("CHF"))
                elif cur == 'GBP':
                    result = '{:.2f}'.format(value / rate_parse("GBP"))
                elif cur == 'CNY':
                    result = '{:.2f}'.format(value / rate_parse("CNY"))
    else:
        abort(405)
    if cur == "":
        abort(400, description="Currency field must not be empty")
    else:
        resp = {'Currency': cur,
                'Money': result}
        return jsonify(resp)


@app.route("/cur_list", methods=["GET"])
def cur_list():
    if request.method == 'GET':
        result = {
            'USD': 'Доллар США',
            'EUR': 'Евро',
            'CHF': 'Швейцарский франк',
            'GBP': 'Фунт стерлингов',
            'CNY': 'Китайский юань'
        }
    else:
        abort(405)
    return jsonify(result)


@app.route('/cur_rate', methods=['GET', 'POST'])
def cur_rate():
    if request.method == 'GET':
        result = {
            'USD': rate_parse("USD"),
            'EUR': rate_parse("EUR"),
            'CHF': rate_parse("CHF"),
            'GBP': rate_parse("GBP"),
            'CNY': rate_parse("CNY")
        }

        return result

    elif request.method == 'POST':
        in_data = request.get_json()
        if in_data["currency"] == 'USD':
            result = '{:.2f}'.format(rate_parse("USD"))
        elif in_data["currency"] == 'EUR':
            result = '{:.2f}'.format(rate_parse("EUR"))
        elif in_data["currency"] == 'CHF':
            result = '{:.2f}'.format(rate_parse("CHF"))
        elif in_data["currency"] == 'GBP':
            result = '{:.2f}'.format(rate_parse("GBP"))
        elif in_data["currency"] == 'CNY':
            result = '{:.2f}'.format(rate_parse("CNY"))
        elif in_data["currency"] == 'USD':
            result = '{:.2f}'.format(rate_parse("USD"))
        else:
            abort(400, description='Currency is not supported')
    else:
        abort(405)

    current_rate = {
        in_data["currency"]: result
    }
    return jsonify(current_rate)


@app.route("/info", methods=["GET"])
def info():
    if request.method == "GET":
        endpoint = request.form.get("endpoint")
        if endpoint is None:
            result = {
                'msg': 'АPI-обменник, переводит рубли в самые популярные валюты. Эндпоинты: /info, /ruex, /cur_list, '
                       '/cur_rate. Чтобы узнать информацию о каждом эндпоинте, введите его название(без слэша) в поле '
                       'endpoint параметров тела запроса. '
            }
        elif endpoint == 'ruex':
            result = {
                'msg': 'Введите вашу сумму в рублях в поле value параметров тела запроса и валюту в которую нужно '
                       'сконвертировать в поле currency ',
                'method': 'GET'
            }
        elif endpoint == 'cur_list':
            result = {
                'msg': 'Выводит список поддерживаемых валют',
                'method': 'GET'
            }
        elif endpoint == 'cur_rate':
            result = {
                1: {
                    'msg': 'Выводит текущий обменный курс поддерживаемых валют к рублю',
                    'method': 'GET'
                },
                2: {
                    'msg': 'Передайте в формате JSON искомую валюту, чтобы получить только ее курс - key: currency, '
                           'value: код выбранной валюты',
                    'method': 'POST'
                }
            }
        elif endpoint == 'info':
            result = {
                'msg': 'Информация о сервисе',
                'method': 'GET'
            }
        else:
            abort(400)
    else:
        abort(405)
    return jsonify(result)
