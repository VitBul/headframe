import json

def handle(data):
    try:
        # Парсим входные params (data — строка JSON)
        params = json.loads(data)

        # Извлекаем th_s как float (default 0)
        th_s = float(params.get('th_s', 0))

        # Извлекаем rate как float (default 0 если не число или отсутствует)
        def get_rate(key):
            try:
                return float(params.get(key, '0'))
            except ValueError:
                return 0.0

        emcd = get_rate('emcd')
        viabtc = get_rate('viabtc')
        trustpool = get_rate('trustpool')
        headframe = get_rate('headframe')

        # Рассчитываем calc-значения
        def calc(rate):
            return (th_s * 30 * rate) / 100000000

        calculations = [
            ('EMCD', calc(emcd)),
            ('ViaBTC', calc(viabtc)),
            ('Trustpool', calc(trustpool)),
            ('Headframe', calc(headframe))
        ]

        # Сортируем по calc descending (убывание)
        sorted_calcs = sorted(calculations, key=lambda x: x[1], reverse=True)

        # Формируем текст с rounding до 6 знаков
        text_lines = []
        for source, value in sorted_calcs:
            rounded_value = round(value, 6)
            text_lines.append(f"{source} – {rounded_value} BTC")

        text = "\n".join(text_lines)

        # Возвращаем JSON для Salebot
        return json.dumps({"text": text, "success": True})
    except Exception as e:
        # Обработка ошибок
        return json.dumps({"text": "", "success": False, "error": str(e)})
