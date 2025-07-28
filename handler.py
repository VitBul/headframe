import json
import sys

# Чтение params из stdin (Salebot передаёт их как аргумент)
if len(sys.argv) > 1:
    params_str = sys.argv[1]
    params = json.loads(params_str)
else:
    params = {}

# Получение переменных из params (они приходят как JSON)
th_s = float(params.get('th_s', 0))
emcd = float(params.get('emcd', 0))
viabtc = float(params.get('viabtc', 0))
trustpool = float(params.get('trustpool', 0))
headframe = float(params.get('headframe', 0))

# Расчёт calc-значений
emcd_calc = th_s * 30 * emcd / 100000000
viabtc_calc = th_s * 30 * viabtc / 100000000
trustpool_calc = th_s * 30 * trustpool / 100000000
headframe_calc = th_s * 30 * headframe / 100000000

# Список для сортировки
rates = [
    {'source': 'EMCD', 'rate': emcd_calc},
    {'source': 'ViaBTC', 'rate': viabtc_calc},
    {'source': 'Trustpool', 'rate': trustpool_calc},
    {'source': 'Headframe', 'rate': headframe_calc}
]

# Сортировка по rate в порядке убывания
sorted_rates = sorted(rates, key=lambda x: x['rate'], reverse=True)

# Формирование текста
text = ''
for item in sorted_rates:
    text += f"{item['source']} – {round(item['rate'], 6)} BTC\n"

# Возврат результата (Salebot сохранит в r)
print(text)
