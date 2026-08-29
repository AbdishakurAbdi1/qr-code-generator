# QR-kode generator

Enkel nettside for å generere QR-koder fra en lenke. Flask-backend + [`qrcode`](https://pypi.org/project/qrcode/)-biblioteket.

## Kjøre lokalt

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Åpne deretter http://127.0.0.1:5000 i nettleseren.

## Deploy

Fungerer fint på gratis-tiere hos f.eks. Render eller PythonAnywhere. Husk å sette
`debug=False` i produksjon (eller kjør med en WSGI-server som `gunicorn`).
