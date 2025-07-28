import json

def handle(data):
    try:
        params = json.loads(data)
        th_s = float(params.get('th_s', 0))
        def get_rate(key):
            try:
                return float(params.get(key, '0'))
            except ValueError:
                return 0.0
        emcd = get_rate('emcd')
        viabtc = get_rate('viabtc')
        trustpool = get_rate('trustpool')
        headframe = get_rate('headframe')
        def calc(rate):
            return (th_s * 30 * rate) / 100000000
        calculations = [('EMCD', calc(emcd)), ('ViaBTC', calc(viabtc)), ('Trustpool', calc(trustpool)), ('Headframe', calc(headframe))]
        sorted_calcs = sorted(calculations, key=lambda x: x[1], reverse=True)
        text_lines = [f"{source} – {round(value, 6)} BTC" for source, value in sorted_calcs]
        text = "\n".join(text_lines)
        return json.dumps({"text": text, "success": True})
    except Exception as e:
        return json.dumps({"text": "", "success": False, "error": str(e)})
