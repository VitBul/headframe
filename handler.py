import json

def handle(data):
    try:
        # Парсим входные params (data — строка JSON)
        params = json.loads(data)
        api_response = params.get('api_response', '[]')  # API-ответ как строка
        th_s = float(params.get('th_s', 0))  # th_s как float, default 0

        # Парсим API-ответ в список dict
        rates_data = json.loads(api_response)

        # Создаём словарь source -> rate (float, или 0 если ошибка)
        rates = {}
        for item in rates_data:
            source = item.get('source', '').lower()  # lowercase для consistency
            try:
                rate = float(item.get('rate', 0))
            except ValueError:
                rate = 0.0
            rates[source] = rate

        # Извлекаем конкретные rates (default 0 если не найдены)
        emcd = rates.get('emcd', 0.0)
        viabtc = rates.get('viabtc', 0.0)
        trustpool = rates.get('trustpool', 0.0)
        headframe = rates.get('headframe', 0.0)

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
        # Обработка ошибок (возврат для debugging)
        return json.dumps({"text": "", "success": False, "error": str(e)})
