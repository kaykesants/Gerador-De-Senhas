from flask import Flask, request, jsonify, render_template_string
import secrets
import string
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Kazin DEV - Gerador PRO</title>

<style>
body{
    background: #0b0616;
    font-family: Arial;
    color: white;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    margin:0;
}

.container{
    background:#140a2e;
    padding:40px;
    border-radius:15px;
    box-shadow:0 0 30px purple;
    width:400px;
    text-align:center;
}

h1{
    color:#bb00ff;
}

input[type="number"]{
    width:100%;
    padding:10px;
    border:none;
    border-radius:8px;
    margin:10px 0;
}

.options{
    text-align:left;
    margin:15px 0;
}

button{
    width:100%;
    padding:12px;
    border:none;
    border-radius:8px;
    background:#7b00ff;
    color:white;
    font-weight:bold;
    cursor:pointer;
    transition:0.3s;
    margin-top:10px;
}

button:hover{
    background:#a100ff;
    box-shadow:0 0 15px #a100ff;
}

.result{
    margin-top:20px;
    font-size:18px;
    word-break:break-all;
    color:#00ffcc;
}

.strength{
    margin-top:10px;
    height:10px;
    border-radius:5px;
    background:#333;
}

.strength-bar{
    height:100%;
    width:0%;
    border-radius:5px;
    transition:0.3s;
}
</style>
</head>

<body>

<div class="container">
    <h1>🔐 Gerador PRO</h1>

    <input type="number" id="tamanho" placeholder="Tamanho da senha" value="12">

    <div class="options">
        <label><input type="checkbox" id="letras" checked> Letras</label><br>
        <label><input type="checkbox" id="numeros" checked> Números</label><br>
        <label><input type="checkbox" id="simbolos" checked> Símbolos</label>
    </div>

    <button onclick="gerarSenha()">GERAR SENHA</button>

    <div class="result" id="resultado"></div>

    <button onclick="copiarSenha()">Copiar</button>

    <div class="strength">
        <div class="strength-bar" id="barra"></div>
    </div>
</div>

<script>
async function gerarSenha(){
    const tamanho = document.getElementById("tamanho").value
    const letras = document.getElementById("letras").checked
    const numeros = document.getElementById("numeros").checked
    const simbolos = document.getElementById("simbolos").checked

    const response = await fetch("/gerar",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({tamanho, letras, numeros, simbolos})
    })

    const data = await response.json()
    document.getElementById("resultado").innerText = data.senha

    avaliarForca(data.senha)
}

function copiarSenha(){
    const senha = document.getElementById("resultado").innerText
    navigator.clipboard.writeText(senha)
    alert("Senha copiada!")
}

function avaliarForca(senha){
    let forca = senha.length * 5
    const barra = document.getElementById("barra")

    if(forca < 40){
        barra.style.width = "30%"
        barra.style.background = "red"
    }
    else if(forca < 70){
        barra.style.width = "60%"
        barra.style.background = "orange"
    }
    else{
        barra.style.width = "100%"
        barra.style.background = "lime"
    }
}
</script>

</body>
</html>
"""

def gerar_senha(tamanho, letras, numeros, simbolos):
    caracteres = ""
    if letras:
        caracteres += string.ascii_letters
    if numeros:
        caracteres += string.digits
    if simbolos:
        caracteres += string.punctuation

    if not caracteres:
        return "Selecione pelo menos uma opção!"

    return ''.join(secrets.choice(caracteres) for _ in range(tamanho))

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/gerar", methods=["POST"])
def gerar():
    data = request.json
    senha = gerar_senha(
        int(data["tamanho"]),
        data["letras"],
        data["numeros"],
        data["simbolos"]
    )
    return jsonify({"senha": senha})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
