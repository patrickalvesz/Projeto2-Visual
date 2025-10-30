import os, colorsys
from flask import Flask, render_template, request, send_from_directory
from PIL import Image, ImageOps, ImageFilter, UnidentifiedImageError
from pillow_avif import AvifImagePlugin

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def abrir_rgb(path):
    try:
        with Image.open(path) as im:
            return im.convert("RGB")
    except UnidentifiedImageError:
        # Evita 500 e mostra mensagem amigável
        raise ValueError("Formato de imagem não suportado. Envie JPG/PNG/WebP/AVIF (requer plugin).")

# ---------- Filtros ----------
def aplicar_sepia(image_path):
    img = abrir_rgb(image_path)
    pixels = img.load()
    for i in range(img.width):
        for j in range(img.height):
            r, g, b = pixels[i, j]
            tr = int(0.393*r + 0.769*g + 0.189*b)
            tg = int(0.349*r + 0.686*g + 0.168*b)
            tb = int(0.272*r + 0.534*g + 0.131*b)
            pixels[i, j] = (min(tr,255), min(tg,255), min(tb,255))
    out = os.path.join(UPLOAD_FOLDER, "sepia_" + os.path.basename(image_path))
    img.save(out)
    return out

def aplicar_sketch(image_path):
    """Sketch simples: escala de cinza + detecção de bordas + inversão"""
    img = abrir_rgb(image_path).convert("L")
    edges = img.filter(ImageFilter.FIND_EDGES)
    sketch = ImageOps.invert(edges)
    sketch = ImageOps.autocontrast(sketch, cutoff=2).convert("RGB")
    out = os.path.join(UPLOAD_FOLDER, "sketch_" + os.path.basename(image_path))
    sketch.save(out)
    return out

def aplicar_color_pop(image_path, hex_color="#ff0000", tolerance_deg=25):
    """Destaca uma cor específica, convertendo o resto para cinza."""
    img = abrir_rgb(image_path)
    w, h = img.size
    px = img.load()

    # alvo em HSV (hue [0..1])
    r_t = int(hex_color[1:3], 16) / 255.0
    g_t = int(hex_color[3:5], 16) / 255.0
    b_t = int(hex_color[5:7], 16) / 255.0
    h_t, s_t, v_t = colorsys.rgb_to_hsv(r_t, g_t, b_t)

    tol = tolerance_deg / 360.0

    for i in range(w):
        for j in range(h):
            r, g, b = [c/255.0 for c in px[i, j]]
            h_p, s_p, v_p = colorsys.rgb_to_hsv(r, g, b)

            # distância circular de matiz
            dh = abs(h_p - h_t)
            dh = min(dh, 1.0 - dh)

            if dh <= tol and s_p > 0.15:  # mantém cor semelhante e evita brancos/cinzas
                continue
            # converte para cinza (luminância simples)
            gray = int((0.299*px[i, j][0] + 0.587*px[i, j][1] + 0.114*px[i, j][2]))
            px[i, j] = (gray, gray, gray)

    out = os.path.join(UPLOAD_FOLDER, f"colorpop_" + os.path.basename(image_path))
    img.save(out)
    return out

# ---------- Rotas ----------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        arquivo = request.files.get("file")
        filtro = request.form.get("filtro")
        original_filename = request.form.get("original_filename")

        # Se não há arquivo novo mas há original_filename, usa o arquivo original
        if not arquivo or arquivo.filename == "":
            if original_filename:
                # Usa o arquivo original já salvo
                original_path = os.path.join(app.config["UPLOAD_FOLDER"], original_filename)
                if not os.path.exists(original_path):
                    return render_template("index.html", erro="Arquivo original não encontrado.")
            else:
                return render_template("index.html", erro="Envie uma imagem.")
        else:
            # Salva novo arquivo
            original_path = os.path.join(app.config["UPLOAD_FOLDER"], arquivo.filename)
            arquivo.save(original_path)
            original_filename = arquivo.filename

        # aplica filtro selecionado
        try:
            if filtro == "sepia":
                saida = aplicar_sepia(original_path)
            elif filtro == "sketch":
                saida = aplicar_sketch(original_path)
            elif filtro == "colorpop":
                cor = request.form.get("cor", "#ff0000")
                tol = float(request.form.get("tol", 25))
                saida = aplicar_color_pop(original_path, cor, tol)
            else:
                return render_template("index.html", erro="Filtro inválido.")
        except ValueError as e:
            return render_template("index.html", erro=str(e))


        # Prepara dados para o template
        template_data = {
            "original": os.path.basename(original_path),
            "filtered": os.path.basename(saida),
            "filtro": filtro,
            "original_filename": original_filename
        }
        
        # Se for colorpop, passa também os valores de cor e tolerância
        if filtro == "colorpop":
            template_data["cor"] = request.form.get("cor", "#ff0000")
            template_data["tol"] = request.form.get("tol", "25")
        
        return render_template("index.html", **template_data)

    return render_template("index.html")

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)
