import io
import os

import qrcode
import qrcode.constants
from urllib.parse import urlsplit
from flask import Flask, abort, render_template, request, send_file

app = Flask(__name__)

MAX_DATA_LENGTH = 20

ALLOWED_TLDS = {
    'no', 'com', 'org', 'net', 'edu', 'gov', 'io', 'eu',
    'se', 'dk', 'fi', 'uk', 'de', 'info', 'app', 'dev', 'co',
}

ERROR_CORRECTION_LEVELS = {
    'L': qrcode.constants.ERROR_CORRECT_L,  # ~7% kan gjenopprettes
    'M': qrcode.constants.ERROR_CORRECT_M,  # ~15% (standard)
    'Q': qrcode.constants.ERROR_CORRECT_Q,  # ~25%
    'H': qrcode.constants.ERROR_CORRECT_H,  # ~30%
}


def is_website(data):
    candidate = data if '://' in data else 'http://' + data
    try:
        parts = urlsplit(candidate)
        host = parts.hostname or ''
    except ValueError:
        return False
    if parts.scheme not in ('http', 'https'):
        return False
    name, dot, tld = host.rpartition('.')
    return bool(name) and dot == '.' and tld in ALLOWED_TLDS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate')
def generate():
    data = request.args.get('data', '').strip()
    if not data:
        abort(400, description='Mangler data-parameter')
    if len(data) > MAX_DATA_LENGTH:
        abort(400, description='Teksten er for lang')
    if not is_website(data):
        abort(400, description='Ikke en gyldig nettadresse')

    ec_param = request.args.get('ec', 'M').upper()
    error_correction = ERROR_CORRECTION_LEVELS.get(ec_param, ERROR_CORRECTION_LEVELS['M'])

    qr = qrcode.QRCode(
        error_correction=error_correction,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    return send_file(buffer, mimetype='image/png')


if __name__ == '__main__':
    # Sett FLASK_DEBUG=1 lokalt for auto-reload og feilsøkingsvisning.
    # Skal ALDRI stå på i produksjon (PythonAnywhere bruker uansett WSGI,
    # så denne blokken kjøres ikke der, men holder vanen trygg).
    debug_mode = os.environ.get('FLASK_DEBUG') == '1'
    app.run(debug=debug_mode)
