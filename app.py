import io

import qrcode
import qrcode.constants
from flask import Flask, abort, render_template, request, send_file

app = Flask(__name__)

MAX_DATA_LENGTH = 2000  # guard against absurdly long input

ERROR_CORRECTION_LEVELS = {
    'L': qrcode.constants.ERROR_CORRECT_L,  # ~7% kan gjenopprettes
    'M': qrcode.constants.ERROR_CORRECT_M,  # ~15% (standard)
    'Q': qrcode.constants.ERROR_CORRECT_Q,  # ~25%
    'H': qrcode.constants.ERROR_CORRECT_H,  # ~30%
}


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
    app.run(debug=True)
