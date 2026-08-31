# QR-kode generator

Enkel nettside for å generere QR-koder fra en lenke. Flask-backend + [`qrcode`](https://pypi.org/project/qrcode/)-biblioteket.

## Kjøre lokalt

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Åpne deretter http://127.0.0.1:5000 i nettleseren. Sett `FLASK_DEBUG=1` (f.eks.
`FLASK_DEBUG=1 python app.py`) for auto-reload og feilsøkingsvisning under utvikling
— la den stå av (standard) ellers.

## Deploy

Fungerer fint på gratis-tiere hos f.eks. Render eller PythonAnywhere. `FLASK_DEBUG`
skal ikke settes i produksjon, og PythonAnywhere kjører uansett appen via WSGI
(`from app import app as application`), så `if __name__ == '__main__'`-blokken
i `app.py` brukes ikke der i det hele tatt.
