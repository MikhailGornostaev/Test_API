Общее описание API:
====================================
API конвертирует рубли в доллары, евро, швейцарские франки, фунты стерлингов или китайские юани.
Информация по курсам валют была взята из открытого API "Exchangerate.host" - https://api.exchangerate.host<br>
URL: http://23.88.52.139:5042

Эндпоинты:
====================================
<pre>
1) /info <br>
*Method: GET.<br>
-Содержит cправочную информацию по работе API.<br>
-Параметры тела запроса(form-data):<br>
a) endpoint
      +Без указания значения параметра:
          Справочная информация по работе API
      +Значение параметра = info:
          Справочная информация по работе эндпоинта info
      +Значение параметра = ruex:
          Справочная информация по работе эндпоинта ruex   
      +Значение параметра = cur_list:
          Справочная информация по работе эндпоинта cur_list
      +Значение параметра = cur_rate:
          Справочная информация по работе эндпоинта cur_rate
          
2) /ruex <br>
*Method: GET.<br>
-Принимает параметры тела запроса value(сумма к обмену) и currency(выбранная валюта).
Возвращает ответ в формате JSON c ключами Currency(выбранная валюта) и Money(сконвертированная в данную валюту, сумма)<br>
-Параметры тела запроса(form-data):<br>
a) value
      +Конвертируемая сумма в рублях type: int/float
b) currency
      +Валюта для конвертации (USD, EUR, CHF, GBP, CNY) type: string

3) /cur_list <br>
*Method: GET.<br>
-Не требует уточнения параметров.
Возвращает ответ в формате JSON c ключами в виде кодов поддерживаемых валют.
В значениях указаны их полные названия.

4) /cur_rate <br>
*Method: GET.<br>
-Не требует уточнения параметров.
Возвращает ответ в формате JSON c ключами в виде кодов поддерживаемых валют.
В значениях указан их текущий курс.)<br>
*Method: POST.<br>
-Выводит курс только выбранной валюты.
Принимает JSON в теле запроса с ключом currency(USD, EUR, CHF, GBP, CNY) type: string.
Возвращает ответ в формате JSON c ключом в виде кода выбранной валюты.
В значении указан текущий курс валюты.
</pre>
