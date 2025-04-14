from flask import Flask, render_template, request

app = Flask(__name__)

gejala_list = [
    "Nyeri Telinga",         # G1
    "Demam",                 # G2
    "Keluar Cairan",         # G3
    "Gangguan Dengar",      # G4
    "Gatal Telinga",         # G5
    "Pusing",                # G6
    "Pendengaran Hilang",    # G7
    "Telinga Berdenging",    # G8
    "Mual",                  # G9
    "Bau Tidak Sedap",       # G10
    "Bengkak",               # G11
    "Merah"                  # G12
]

rules = {
    "Otitis Eksterna": [0, 1, 2, 4, 5, 10],  # G1, G2, G3, G5, G6, G11
    "Otitis Media": [3, 4, 6, 7, 9],          # G4, G5, G7, G8, G10
    "Otitis Interna": [4, 8, 9],              # G5, G9, G10
    "Gendang Telinga Pecah": [4, 8, 9, 10],   # G5, G9, G10, G11
    "Kolesteatoma": [3, 5, 10],               # G4, G6, G11
    "Presbikusis": [3, 4],                    # G4, G5
}

penyakit_deskripsi = {
    "Otitis Eksterna": "Otitis eksterna adalah infeksi pada saluran telinga luar, sering disebabkan oleh bakteri atau jamur. Gejala termasuk nyeri telinga, gatal, dan keluar cairan.",
    "Otitis Media": "Otitis media adalah infeksi pada telinga tengah, sering terjadi pada anak-anak. Gejala termasuk gangguan pendengaran, nyeri telinga, dan demam.",
    "Otitis Interna": "Otitis interna adalah infeksi pada telinga dalam, yang dapat menyebabkan gangguan keseimbangan dan pendengaran. Gejala termasuk pusing, mual, dan gangguan pendengaran.",
    "Gendang Telinga Pecah": "Gendang telinga pecah adalah robekan pada membran timpani. Gejala termasuk gangguan pendengaran, nyeri, dan keluar cairan dari telinga.",
    "Kolesteatoma": "Kolesteatoma adalah pertumbuhan kulit abnormal di telinga tengah, yang dapat merusak struktur telinga. Gejala termasuk gangguan pendengaran, pusing, dan keluar cairan berbau.",
    "Presbikusis": "Presbikusis adalah gangguan pendengaran yang berkaitan dengan usia. Gejala termasuk kesulitan mendengar suara frekuensi tinggi."
}

def forward_chaining(selected_gejala):
    hasil = []
    best_percentage = 0
    best_result = None

    for penyakit, rule_gejala in rules.items():
        matched = len([g for g in rule_gejala if g in selected_gejala])
        total = len(rule_gejala)
        
        if total == 0:
            continue  # skip if no rule

        percentage = round((matched / total) * 100, 1)

        if percentage > best_percentage and matched > 0:
            best_percentage = percentage
            best_result = (penyakit, percentage)

    if best_result:
        hasil.append(best_result)

    return hasil

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/deteksi', methods=["GET", "POST"])
def deteksi():     
    if request.method == "POST":
        selected_gejala = request.form.getlist("gejala")
        selected_gejala = list(map(int, selected_gejala))
        hasil_forward = forward_chaining(selected_gejala)

        hasil = []
        for penyakit, persentase in hasil_forward:
            deskripsi = penyakit_deskripsi.get(penyakit, "Deskripsi tidak tersedia.")
            hasil.append({
                "nama": penyakit,
                "persentase": persentase,
                "deskripsi": deskripsi
            })

        return render_template("hasil.html", hasil=hasil)
    
    return render_template("deteksi.html", gejala_list=gejala_list)

@app.route('/hasil')
def hasil():
    return render_template('hasil.html')

if __name__ == "__main__":
    app.run(debug=True)