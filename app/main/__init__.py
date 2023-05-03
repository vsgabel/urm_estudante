from flask import Blueprint, render_template, url_for
import datetime
import qrcode

main = Blueprint('main', __name__)

alunos = {
    1: {
        "id": 1,
        "nome": "Yago Viana",
        "curso": "Hotelaria",
        "nivel": "Graduação"
    },
    2: {
        "id": 2,
        "nome": "Nelson Martins",
        "curso": "Ciência da Computação",
        "nivel": "Graduação"
    },
    3: {
        "id": 3,
        "nome": "Jéssica Aparício",
        "curso": "Biomedicina",
        "nivel": "Pós-Graduação"
    }
}

@main.route("/")
def index():
    return render_template("index.html", alunos=alunos)

@main.route('/carteirinha/<int:id>')
def carteirinha(id: int):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(f"http://localhost:5000/verificar/{id}")
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    img.save("app/"+url_for("static", filename=f"img/{id}.png"))
    return render_template('carteirinha.html', aluno=alunos[id])

@main.route('/verificar/<int:id>')
def verificar(id: int):
    if id not in alunos.keys():
        return "Aluno não encontrado", 404
    validade = datetime.datetime.now() + datetime.timedelta(days=365*2)
    validade = validade.strftime("%m/%Y")
    return render_template("verificar.html", aluno=alunos[id], validade=validade)