import html
import random
import re
import time
from urllib.parse import quote

import streamlit as st
import streamlit.components.v1 as components

# ─────────────────────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Faurare Quiz",
    page_icon="🌲",
    layout="centered",
    initial_sidebar_state="collapsed",
)

POIN_PER_SOAL = 10

# ─────────────────────────────────────────────────────────────
# DATABASE HEWAN
# "gambar" opsional: isi link foto jika ingin foto asli (menggantikan emoji).
# "alias" opsional: variasi ejaan jawaban yang tetap dianggap benar.
# ─────────────────────────────────────────────────────────────
daftar_hewan = [
    {"nama": "komodo", "alias": ["komodo dragon", "biawak komodo"],
     "kategori": "Reptil Purba / NTT", "ikon": "🦖", "latar": "🏝️", "gambar": "",
     "clues": ["Reptil terbesar di dunia yang masih hidup.",
               "Memiliki air liur beracun untuk melumpuhkan mangsa.",
               "Hewan endemik asli Pulau Komodo dan NTT."],
     "fakta": "Komodo adalah kadal terbesar di bumi yang panjangnya bisa mencapai 3 meter dan berat hingga 70 kg!"},
    {"nama": "orangutan", "alias": ["orang utan", "orang-utan"],
     "kategori": "Primata / Sumatera & Kalimantan", "ikon": "🦧", "latar": "🌴", "gambar": "",
     "clues": ["Namanya berarti 'manusia hutan' dalam bahasa lokal.",
               "Memiliki bulu tebal berwarna jingga kecokelatan.",
               "Sebagian besar hidupnya dihabiskan di atas pohon."],
     "fakta": "Orangutan sangat cerdas dan mampu menggunakan tongkat serta alat alami untuk mencari makan."},
    {"nama": "badak jawa", "alias": ["badak"],
     "kategori": "Mamalia / Ujung Kulon", "ikon": "🦏", "latar": "🌿", "gambar": "",
     "clues": ["Salah satu mamalia paling langka dan terancam punah di bumi.",
               "Memiliki cula tunggal (bercula satu) yang khas.",
               "Habitat aslinya dilindungi di Taman Nasional Ujung Kulon."],
     "fakta": "Badak jawa sangat menyukai kubangan lumpur di hutan hujan untuk mendinginkan tubuh mereka."},
    {"nama": "harimau sumatera", "alias": ["harimau sumatra", "macan sumatera", "macan sumatra"],
     "kategori": "Karnivora / Sumatera", "ikon": "🐅", "latar": "🍂", "gambar": "",
     "clues": ["Spesies harimau terkecil yang masih bertahan hidup saat ini.",
               "Memiliki pola garis loreng hitam yang sangat rapat.",
               "Kucing besar ikonik yang asli berasal dari Pulau Sumatera."],
     "fakta": "Harimau sumatera adalah perenang yang sangat handal dan sering berenang di sungai."},
    {"nama": "anoa", "alias": ["kerbau kerdil"],
     "kategori": "Mamalia / Sulawesi", "ikon": "🐃", "latar": "⛰️", "gambar": "",
     "clues": ["Sering dijuluki sebagai kerbau kerdil hutan.",
               "Memiliki sepasang tanduk lurus dan runcing tajam.",
               "Hewan endemik kebanggaan Pulau Sulawesi."],
     "fakta": "Anoa bersifat soliter (menyendiri) dan sangat menyukai kubangan air serta mata air pegunungan."},
    {"nama": "cendrawasih", "alias": ["cenderawasih", "burung cendrawasih", "burung cenderawasih", "burung surga"],
     "kategori": "Burung / Papua", "ikon": "🦜", "latar": "✨", "gambar": "",
     "clues": ["Dijuluki secara internasional sebagai 'Bird of Paradise' (Burung Surga).",
               "Memiliki bulu ekor yang sangat megah, panjang, dan penuh warna.",
               "Habitat utamanya berada di rimbunnya hutan Papua."],
     "fakta": "Keindahan bulu cendrawasih membuat burung ini disakralkan sebagai simbol budaya Papua."},
    {"nama": "babirusa", "alias": ["babi rusa"],
     "kategori": "Mamalia / Sulawesi", "ikon": "🐗", "latar": "🦷", "gambar": "",
     "clues": ["Penampakannya mirip perpaduan unik antara babi dan rusa.",
               "Memiliki taring melengkung ke atas yang menembus moncongnya.",
               "Satwa liar endemik yang hanya bisa ditemukan di Sulawesi."],
     "fakta": "Taring jantan babirusa bisa melingkar hampir menyentuh bagian mata seiring bertambahnya usia."},
    {"nama": "maleo", "alias": ["burung maleo"],
     "kategori": "Burung / Sulawesi", "ikon": "🥚", "latar": "🔥", "gambar": "",
     "clues": ["Memiliki benjolan unik di atas kepalanya.",
               "Tidak mengerami telur, melainkan menimbunnya di dalam pasir.",
               "Memanfaatkan panas alami bumi / vulkanik untuk penetasan."],
     "fakta": "Anak burung maleo sudah bisa langsung terbang mandiri begitu menetas dari dalam tanah."},
    {"nama": "tarsius", "alias": ["tarsier", "tarsius sulawesi"],
     "kategori": "Primata / Sulawesi", "ikon": "👀", "latar": "🌿", "gambar": "",
     "clues": ["Primata berukuran sangat kecil dengan mata bulat raksasa.",
               "Lehernya sangat fleksibel dan bisa berputar hingga 180 derajat.",
               "Suka melompat dari pohon ke pohon di hutan Sulawesi."],
     "fakta": "Bola mata tarsius sebenarnya lebih besar daripada otaknya sendiri!"},
    {"nama": "jalak bali", "alias": ["curik bali", "jalak putih"],
     "kategori": "Burung / Bali", "ikon": "🕊️", "latar": "🌺", "gambar": "",
     "clues": ["Didominasi warna bulu putih bersih dengan lingkaran mata biru.",
               "Memiliki jambul indah di bagian belakang kepalanya.",
               "Satwa maskot fauna resmi Provinsi Bali."],
     "fakta": "Jalak bali termasuk salah satu burung pengicau paling dilindungi dan langka di dunia."},
]
# Hewan ke-10 (dipisah supaya mudah ditambah / diganti).
daftar_hewan.append(
    {"nama": "gajah sumatera", "alias": ["gajah sumatra", "gajah"],
     "kategori": "Mamalia / Sumatera", "ikon": "🐘", "latar": "🌳", "gambar": "",
     "clues": ["Subspesies gajah Asia yang berstatus sangat terancam punah.",
               "Bertelinga lebih kecil dibanding gajah Afrika dan berbelalai panjang.",
               "Hidup di hutan-hutan Pulau Sumatera dan sering dijuluki 'insinyur hutan'."],
     "fakta": "Gajah sumatera membantu menyebarkan biji pohon lewat kotorannya, sehingga hutan bisa tumbuh kembali."}
)

TOTAL_SOAL = len(daftar_hewan)
SKOR_MAKS = TOTAL_SOAL * POIN_PER_SOAL

EMOJI_BENAR = ["🥳", "😄", "🤩", "😸", "🎉"]
EMOJI_SALAH = ["😢", "😭", "🥺", "😿"]

# ─────────────────────────────────────────────────────────────
# KARAKTER PIXEL ART (digambar dari grid teks 12 kolom → SVG)
#  H/h = topi/rambut (terang/gelap)   S = kulit    E = mata   m = mulut
#  C/c = baju (terang/gelap)          W = aksen    P = celana B = sepatu
# ─────────────────────────────────────────────────────────────
SPRITE_BADAN = [
    "...hhhhhh...",
    "..hHHHHHHh..",
    "..HHHHHHHH..",
    "..hhhhhhhh..",
    "..SSSSSSSS..",
    "..SESSSSES..",
    "..SSSSSSSS..",
    "...SSmmSS...",
    "..CCCCCCCC..",
    ".SCCWWWWCCS.",
    ".SCCCCCCCCS.",
    "..cCCCCCCc..",
    "..PPPPPPPP..",
]
SPRITE_KAKI = [
    ["..PP....PP..", "..BB....BB.."],   # langkah lebar
    ["...PPPPPP...", "...BBBBBB..."],   # kaki merapat
]

KARAKTER = {
    "red": {
        "nama": "Red", "bola": "#ef4444",
        "palet": {"H": "#dc2626", "h": "#7f1d1d", "S": "#fcd9b6", "E": "#111827", "m": "#b45309",
                  "C": "#ef4444", "c": "#b91c1c", "W": "#f8fafc", "P": "#1e3a8a", "B": "#111827"},
    },
    "blue": {
        "nama": "Blue", "bola": "#3b82f6",
        "palet": {"H": "#92400e", "h": "#451a03", "S": "#fcd9b6", "E": "#111827", "m": "#b45309",
                  "C": "#3b82f6", "c": "#1d4ed8", "W": "#e2e8f0", "P": "#334155", "B": "#0f172a"},
    },
    "leaf": {
        "nama": "Leaf", "bola": "#22c55e",
        "palet": {"H": "#f8fafc", "h": "#94a3b8", "S": "#fcd9b6", "E": "#111827", "m": "#b45309",
                  "C": "#22c55e", "c": "#15803d", "W": "#fef3c7", "P": "#92400e", "B": "#1c1917"},
    },
}


def rapat(teks: str) -> str:
    """Gabungkan HTML multi-baris jadi satu baris (aman dari aturan indentasi markdown)."""
    return "".join(baris.strip() for baris in teks.splitlines())


def sprite_svg(kunci: str, lebar: int = 56, frame: int = 0, kelas: str = "") -> str:
    pal = KARAKTER[kunci]["palet"]
    baris = SPRITE_BADAN + SPRITE_KAKI[frame]
    rects = []
    for y, row in enumerate(baris):
        x = 0
        while x < len(row):
            ch = row[x]
            if ch == ".":
                x += 1
                continue
            j = x
            while j < len(row) and row[j] == ch:
                j += 1
            rects.append(f'<rect x="{x}" y="{y}" width="{j - x}" height="1" fill="{pal[ch]}"/>')
            x = j
    tinggi = round(lebar * len(baris) / 12)
    return (f'<svg class="{kelas}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 {len(baris)}" '
            f'width="{lebar}" height="{tinggi}" shape-rendering="crispEdges">{"".join(rects)}</svg>')


def pokeball_svg(warna: str = "#ef4444", ukuran: int = 26) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" width="{ukuran}" height="{ukuran}">'
            '<circle cx="10" cy="10" r="9" fill="#f8fafc" stroke="#0f172a" stroke-width="1.4"/>'
            f'<path d="M1 10a9 9 0 0 1 18 0z" fill="{warna}" stroke="#0f172a" stroke-width="1.4"/>'
            '<line x1="1" y1="10" x2="19" y2="10" stroke="#0f172a" stroke-width="1.6"/>'
            '<circle cx="10" cy="10" r="3" fill="#f8fafc" stroke="#0f172a" stroke-width="1.4"/></svg>')


def uri_pohon(warna: str, daftar) -> str:
    """Tile SVG pohon pinus (200x80) sebagai data-URI untuk latar yang bergulir."""
    bagian = []
    for cx, h, w in daftar:
        dasar = 80
        for puncak, kaki, lebar_rel in ((1.0, 0.45, 0.5), (0.72, 0.18, 0.7), (0.45, 0.0, 0.9)):
            pts = (f"{cx},{dasar - h * puncak:.0f} "
                   f"{cx - w * lebar_rel:.0f},{dasar - h * kaki:.0f} "
                   f"{cx + w * lebar_rel:.0f},{dasar - h * kaki:.0f}")
            bagian.append(f'<polygon points="{pts}" fill="{warna}"/>')
        bagian.append(f'<rect x="{cx - 2}" y="{dasar - 6}" width="4" height="6" fill="{warna}"/>')
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 80" width="200" height="80">'
           + "".join(bagian) + "</svg>")
    return "data:image/svg+xml;utf8," + quote(svg)


POHON_JAUH = uri_pohon("#0f3d36", [(25, 50, 22), (78, 60, 26), (132, 46, 20), (180, 58, 24)])
POHON_DEKAT = uri_pohon("#06241b", [(40, 78, 32), (112, 68, 30), (166, 76, 34)])


# ─────────────────────────────────────────────────────────────
# GAYA TAMPILAN (CSS)
# ─────────────────────────────────────────────────────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Poppins:wght@400;500;600&family=Press+Start+2P&display=swap');

html, body, [class*="css"], .stApp, p, label, li, span, div { font-family: 'Poppins', sans-serif; }
h1, h2, h3, .gelar, .nomor, .nama-profil { font-family: 'Fredoka', sans-serif !important; }

/* Latar malam hutan pinus */
.stApp {
    background:
        radial-gradient(circle at 80% 6%, rgba(254, 243, 199, 0.10), transparent 30%),
        radial-gradient(circle at 50% 105%, rgba(16, 185, 129, 0.20), transparent 55%),
        linear-gradient(165deg, #04180f 0%, #08302a 50%, #0a2433 100%);
    background-attachment: fixed;
    color: #e8f3ee;
}

/* Bersihkan UI bawaan Streamlit: tanpa sidebar, menu, toolbar, status */
[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"], #MainMenu, footer { display: none !important; }

.block-container { padding-top: 3.4rem; padding-bottom: 3rem; max-width: 720px; }

.stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label, .stApp li,
[data-testid="stMarkdownContainer"] { color: #e8f3ee; }
[data-testid="stCaptionContainer"] { color: #b6cbc2; }

/* Kontainer kaca */
.glass {
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 22px; padding: 20px;
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.30);
    margin-bottom: 16px;
}

.logo {
    text-align: center; font-family: 'Press Start 2P', monospace; line-height: 1.5;
    font-size: clamp(1.05rem, 4.6vw, 1.6rem);
    background: linear-gradient(90deg, #fde68a, #6ee7b7, #67e8f9);
    -webkit-background-clip: text; background-clip: text; color: transparent !important;
    margin: 4px 0 8px 0;
}
.subjudul { text-align: center; opacity: 0.8; font-size: 0.92rem; }

/* Adegan penjelajah (pelari pixel di hutan pinus) */
.adegan {
    position: relative; height: 124px; border-radius: 20px; overflow: hidden; margin-bottom: 16px;
    background: linear-gradient(180deg, #0b2f3a 0%, #0d3f3a 55%, #0b3a2c 100%);
    border: 1px solid rgba(255, 255, 255, 0.12); box-shadow: 0 10px 28px rgba(0, 0, 0, 0.30);
}
.adegan .bulan {
    position: absolute; top: 14px; right: 26px; width: 22px; height: 22px; border-radius: 50%;
    background: #fef3c7; box-shadow: 0 0 22px 8px rgba(254, 243, 199, 0.22);
}
.adegan .lapis {
    position: absolute; left: 0; right: 0; bottom: 12px; height: 80px;
    background-repeat: repeat-x; background-position: 0 100%; background-size: 200px 80px;
}
.adegan .jauh { background-image: url("__POHON_JAUH__"); opacity: 0.85; animation: geser 28s linear infinite; }
.adegan .dekat { background-image: url("__POHON_DEKAT__"); animation: geser 10s linear infinite; }
.adegan .tanah {
    position: absolute; left: 0; right: 0; bottom: 0; height: 14px;
    background: #06261a; border-top: 2px solid #0f4a35;
}
.adegan .tanah::after {
    content: ""; position: absolute; left: 0; right: 0; top: 4px; height: 3px; background-size: 34px 3px;
    background-image: repeating-linear-gradient(90deg, rgba(255,255,255,0.14) 0 14px, transparent 14px 34px);
    animation: garis 0.7s linear infinite;
}
.pelari { position: absolute; left: 18%; bottom: 9px; width: 52px; height: 65px; animation: pantul 0.36s steps(2, end) infinite; }
.pelari svg { position: absolute; left: 0; bottom: 0; image-rendering: pixelated; }
.pelari .k1 { animation: kaki1 0.36s steps(1, end) infinite; }
.pelari .k2 { animation: kaki2 0.36s steps(1, end) infinite; }
@keyframes geser { from { background-position: 0 100%; } to { background-position: -200px 100%; } }
@keyframes garis { from { background-position: 0 0; } to { background-position: -34px 0; } }
@keyframes kaki1 { 0%, 49.9% { opacity: 1; } 50%, 100% { opacity: 0; } }
@keyframes kaki2 { 0%, 49.9% { opacity: 0; } 50%, 100% { opacity: 1; } }
@keyframes pantul { 0% { transform: translateY(0); } 50% { transform: translateY(-3px); } 100% { transform: translateY(0); } }

/* Profil pemain (karakter mendampingi selama kuis) */
.profil {
    display: flex; align-items: center; gap: 12px; padding: 8px 14px 8px 10px; margin-bottom: 12px;
    background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.13);
    border-radius: 18px; backdrop-filter: blur(10px);
}
.profil .ava { width: 40px; height: 44px; display: flex; align-items: center; justify-content: center; }
.profil .ava svg { image-rendering: pixelated; }
.profil .info { flex: 1; line-height: 1.25; min-width: 0; }
.profil .nama-profil { font-weight: 600; font-size: 1.05rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.profil .meta { display: flex; align-items: center; gap: 6px; font-size: 0.8rem; opacity: 0.8; }
.profil .skor {
    font-family: 'Fredoka', sans-serif; font-weight: 600; color: #fde68a;
    background: rgba(253, 230, 138, 0.12); border: 1px solid rgba(253, 230, 138, 0.35);
    padding: 4px 12px; border-radius: 999px;
}

/* Kartu hewan */
.kartu-hewan { position: relative; text-align: center; overflow: hidden; padding: 22px 16px 18px; }
.kartu-hewan .lencana {
    display: inline-block; padding: 5px 14px; border-radius: 999px; font-size: 0.8rem; font-weight: 500;
    background: rgba(110, 231, 183, 0.12); border: 1px solid rgba(110, 231, 183, 0.40); color: #a7f3d0;
}
.kartu-hewan .ikon-besar {
    font-size: clamp(76px, 22vw, 120px); line-height: 1.2; display: block; margin: 8px 0 2px;
    animation: melayang 3.6s ease-in-out infinite; filter: drop-shadow(0 10px 16px rgba(0, 0, 0, 0.45));
}
.kartu-hewan .ikon-latar { position: absolute; right: 14px; top: 10px; font-size: 1.8rem; opacity: 0.45; animation: melayang 5s ease-in-out infinite reverse; }
.kartu-hewan .nomor { font-size: 1rem; opacity: 0.8; margin-bottom: 4px; }
.kartu-hewan .tanya { font-weight: 600; margin-top: 4px; }

@keyframes melayang { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-9px); } }
@keyframes muncul { from { opacity: 0; transform: translateY(12px) scale(0.985); } to { opacity: 1; transform: none; } }
@keyframes goyang { 0%, 100% { transform: translateX(0); } 20% { transform: translateX(-7px); } 40% { transform: translateX(6px); } 60% { transform: translateX(-4px); } 80% { transform: translateX(3px); } }
@keyframes loncat { 0%, 100% { transform: translateY(0) scale(1); } 40% { transform: translateY(-14px) scale(1.12); } }
.animasi { animation: muncul 0.5s ease both; }

/* Clue */
.clue { background: rgba(255, 255, 255, 0.06); border-left: 4px solid #6ee7b7; border-radius: 12px; padding: 10px 14px; margin: 8px 0; animation: muncul 0.4s ease both; }

/* Reaksi jawaban */
.hasil-benar { border-color: rgba(110, 231, 183, 0.55); background: rgba(16, 185, 129, 0.14); }
.hasil-lewat { border-color: rgba(253, 186, 116, 0.55); background: rgba(249, 115, 22, 0.12); }
.hasil-salah { border-color: rgba(252, 165, 165, 0.55); background: rgba(239, 68, 68, 0.12); animation: goyang 0.5s ease both; padding: 14px 18px; }
.reaksi { text-align: center; font-size: 3.2rem; line-height: 1.2; margin-bottom: 4px; }
.reaksi span { display: inline-block; animation: loncat 0.9s ease-in-out infinite; }
.reaksi span + span { animation-delay: 0.18s; margin-left: 10px; }
.salah-baris { display: flex; align-items: center; gap: 14px; }
.salah-baris .emo { font-size: 2.6rem; animation: loncat 1.2s ease-in-out infinite; }

/* Gelar */
.gelar {
    text-align: center; font-weight: 700; font-size: clamp(2rem, 9vw, 3.2rem); margin: 4px 0;
    background: linear-gradient(90deg, #fde68a, #fb923c); -webkit-background-clip: text; background-clip: text; color: transparent !important;
}

/* Pilih karakter */
.kar-kartu {
    text-align: center; padding: 12px 4px 10px; border-radius: 18px; transition: all 0.2s ease;
    background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.13);
}
.kar-kartu.pilih {
    border-color: #6ee7b7; background: rgba(110, 231, 183, 0.13); transform: translateY(-3px);
    box-shadow: 0 0 0 2px rgba(110, 231, 183, 0.22), 0 10px 24px rgba(0, 0, 0, 0.30);
}
.kar-kartu svg { image-rendering: pixelated; max-width: 100%; height: auto; }
.kar-nama { font-family: 'Fredoka', sans-serif; font-weight: 600; margin: 6px 0 4px; }
.label-bagian { font-weight: 600; margin: 6px 0 8px; }

/* Tombol: besar, tenang, mudah disentuh */
.stButton > button, [data-testid="stFormSubmitButton"] > button {
    min-height: 3rem; border-radius: 14px; font-weight: 600; font-size: 1rem;
    color: #e8f3ee; background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.22);
    transition: transform 0.15s ease, filter 0.15s ease, background 0.15s ease;
}
.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
    background: rgba(255, 255, 255, 0.14); border-color: rgba(255, 255, 255, 0.35); color: #fff; transform: translateY(-1px);
}
.stButton > button[kind="primary"], [data-testid="stBaseButton-primary"],
[data-testid="stFormSubmitButton"] > button[kind="primary"], [data-testid="stBaseButton-primaryFormSubmit"] {
    color: #052e16; border: none; background: linear-gradient(135deg, #6ee7b7, #67e8f9);
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.28);
}
.stButton > button[kind="primary"]:hover, [data-testid="stBaseButton-primary"]:hover,
[data-testid="stFormSubmitButton"] > button[kind="primary"]:hover, [data-testid="stBaseButton-primaryFormSubmit"]:hover {
    color: #052e16; filter: brightness(1.07);
    background: linear-gradient(135deg, #6ee7b7, #67e8f9);
}
.stButton > button:active, [data-testid="stFormSubmitButton"] > button:active { transform: scale(0.97); }

/* Input */
.stTextInput input {
    min-height: 3rem; font-size: 1.05rem; border-radius: 14px;
    background: rgba(255, 255, 255, 0.08) !important; color: #f8fafc !important;
    border: 1px solid rgba(255, 255, 255, 0.24) !important;
}
.stTextInput input::placeholder { color: #b6cbc2 !important; opacity: 0.8; }
[data-testid="stExpander"], [data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 16px; backdrop-filter: blur(10px);
}
hr { border-color: rgba(255, 255, 255, 0.14) !important; }

/* Kolom pilih karakter tetap berjajar 3 di layar HP */
[data-testid="stHorizontalBlock"] { flex-direction: row !important; flex-wrap: nowrap !important; gap: 0.6rem !important; }
[data-testid="stColumn"], [data-testid="column"] { min-width: 0 !important; width: auto !important; flex: 1 1 0 !important; }

/* Transisi masuk ekspedisi */
.transisi {
    position: fixed; inset: 0; z-index: 99998; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 14px;
    background: radial-gradient(circle at 50% 45%, #0f5a47 0%, #04200f 72%); animation: layarMasuk 0.45s ease both;
}
.transisi .bola { width: 96px; height: 96px; animation: gocang 0.9s ease-in-out 0.5s 1 both, denyut 0.5s ease-in-out 1.5s 1 both; }
.transisi .bola svg { width: 100%; height: 100%; }
.transisi .teks { font-family: 'Fredoka', sans-serif; font-size: 1.4rem; font-weight: 600; color: #e8f3ee; animation: muncul 0.6s ease 0.3s both; }
.transisi .sub { opacity: 0.75; animation: muncul 0.6s ease 0.6s both; }
.transisi .kilat { position: absolute; inset: 0; background: #ecfdf5; opacity: 0; pointer-events: none; animation: cahaya 0.6s ease 1.45s both; }
@keyframes layarMasuk { from { opacity: 0; } to { opacity: 1; } }
@keyframes gocang { 0%, 100% { transform: rotate(0); } 20% { transform: rotate(-22deg); } 40% { transform: rotate(20deg); } 60% { transform: rotate(-14deg); } 80% { transform: rotate(10deg); } }
@keyframes denyut { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.18); } }
@keyframes cahaya { 0% { opacity: 0; } 45% { opacity: 0.5; } 100% { opacity: 0; } }

iframe[height="0"] { display: none; }

@media (max-width: 640px) {
    .block-container { padding-left: 0.9rem; padding-right: 0.9rem; }
    .glass { padding: 16px; border-radius: 18px; }
}
@media (prefers-reduced-motion: reduce) {
    .ikon-besar, .ikon-latar, .animasi, .clue, .pelari, .pelari svg, .lapis, .tanah::after,
    .reaksi span, .salah-baris .emo, .hasil-salah, .transisi * { animation: none !important; }
}
"""
CSS = CSS.replace("__POHON_JAUH__", POHON_JAUH).replace("__POHON_DEKAT__", POHON_DEKAT)
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# AUDIO: efek suara + musik latar tegang (semua dibuat WebAudio, tanpa file)
# Tombol musik on/off dipasang di pojok kanan atas halaman.
# ─────────────────────────────────────────────────────────────
JS_AUDIO = """
<script>
(function() {
  var P = window.parent;
  function ctx() {
    var AC = P.AudioContext || P.webkitAudioContext;
    if (!AC) return null;
    if (!P.__rfCtx) P.__rfCtx = new AC();
    if (P.__rfCtx.state === 'suspended') P.__rfCtx.resume();
    return P.__rfCtx;
  }
  function nadaAt(f, t, dur, tipe, vol) {
    var c = ctx(); if (!c) return;
    var o = c.createOscillator(), g = c.createGain();
    o.type = tipe || 'sine'; o.frequency.value = f;
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol || 0.18, t + 0.015);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    o.connect(g); g.connect(c.destination);
    o.start(t); o.stop(t + dur + 0.05);
  }
  function nada(f, mulai, dur, tipe, vol) {
    var c = ctx(); if (c) nadaAt(f, c.currentTime + mulai, dur, tipe, vol);
  }

  // ── Efek suara
  P.__rfSfx = function(jenis) {
    if (jenis === 'klik')    { nada(660, 0, 0.08, 'triangle', 0.10); }
    if (jenis === 'benar')   { [523, 659, 784, 1047].forEach(function(f, i) { nada(f, i * 0.09, 0.22, 'triangle', 0.18); }); }
    if (jenis === 'salah')   { nada(220, 0, 0.18, 'sawtooth', 0.10); nada(150, 0.16, 0.3, 'sawtooth', 0.10); }
    if (jenis === 'lewat')   { nada(440, 0, 0.12, 'sine', 0.12); nada(330, 0.12, 0.2, 'sine', 0.12); }
    if (jenis === 'mulai')   { [392, 523, 659, 784, 1047].forEach(function(f, i) { nada(f, i * 0.11, 0.26, 'triangle', 0.18); }); }
    if (jenis === 'selesai') { [523, 659, 784, 1047, 784, 1047, 1319].forEach(function(f, i) { nada(f, i * 0.12, 0.3, 'triangle', 0.18); }); }
  };

  // ── Musik latar tegang: bass berdenyut + arpeggio staccato (A minor → F → G → E)
  var AKOR = [
    {b: 55.00, n: [220.00, 261.63, 329.63]},
    {b: 43.65, n: [174.61, 220.00, 261.63]},
    {b: 49.00, n: [196.00, 246.94, 293.66]},
    {b: 41.20, n: [164.81, 207.65, 246.94]}
  ];
  P.__rfTick = function() {
    if (!P.__rfMusikOn) return;
    var c = ctx(); if (!c) return;
    while (P.__rfNext < c.currentTime + 0.4) {
      var s = P.__rfStep, ak = AKOR[Math.floor(s / 8) % 4], t = P.__rfNext;
      nadaAt(s % 2 === 0 ? ak.b : ak.b * 2, t, 0.12, 'sawtooth', s % 4 === 0 ? 0.060 : 0.038);
      nadaAt(ak.n[s % 3], t, 0.09, 'square', 0.022);
      if (s % 8 === 7) nadaAt(ak.n[2] * 2, t, 0.10, 'square', 0.028);
      P.__rfNext += 0.14; P.__rfStep++;
    }
  };
  if (!P.__rfTimer) P.__rfTimer = P.setInterval(function() { if (P.__rfTick) P.__rfTick(); }, 100);

  // ── Tombol musik minimalis (pojok kanan atas)
  function labelTombol() {
    var b = P.document.getElementById('rf-musik');
    if (b) { b.textContent = P.__rfMusikOn ? '🔊' : '🔇'; b.style.opacity = P.__rfMusikOn ? '1' : '0.7'; }
  }
  P.__rfToggleMusik = function() {
    var c = ctx(); if (!c) return;
    P.__rfMusikOn = !P.__rfMusikOn;
    if (P.__rfMusikOn) { P.__rfNext = c.currentTime + 0.05; P.__rfStep = 0; }
    labelTombol();
  };
  if (!P.document.getElementById('rf-musik')) {
    var b = P.document.createElement('button');
    b.id = 'rf-musik'; b.type = 'button'; b.setAttribute('aria-label', 'Musik on/off');
    b.style.cssText = 'position:fixed;top:12px;right:12px;z-index:99999;width:40px;height:40px;border-radius:50%;' +
      'border:1px solid rgba(255,255,255,.25);background:rgba(10,40,30,.55);color:#e8f3ee;font-size:18px;cursor:pointer;' +
      'backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);display:flex;align-items:center;justify-content:center;padding:0;';
    b.addEventListener('click', function() { if (P.__rfToggleMusik) P.__rfToggleMusik(); });
    P.document.body.appendChild(b);
  }
  labelTombol();

  // ── Suara klik otomatis di semua tombol (dipasang sekali)
  if (!P.__rfBound) {
    P.__rfBound = true;
    P.document.addEventListener('click', function(e) {
      var btn = e.target && e.target.closest ? e.target.closest('button') : null;
      if (btn && btn.id !== 'rf-musik' && P.__rfSfx) P.__rfSfx('klik');
    }, true);
  }

  var jenis = "__JENIS__";   // nonce: __NONCE__
  if (jenis) setTimeout(function() { P.__rfSfx(jenis); }, 120);
})();
</script>
"""


def mainkan_sfx(jenis: str):
    """Jadwalkan efek suara; dibunyikan di akhir run lewat render_sfx()."""
    st.session_state.sfx = jenis


def render_sfx():
    jenis = st.session_state.pop("sfx", "")
    st.session_state.nonce = st.session_state.get("nonce", 0) + 1
    kode = JS_AUDIO.replace("__JENIS__", jenis).replace("__NONCE__", str(st.session_state.nonce))
    components.html(kode, height=0)


# ─────────────────────────────────────────────────────────────
# FUNGSI BANTU
# ─────────────────────────────────────────────────────────────
def normalisasi(teks: str) -> str:
    teks = re.sub(r"[^a-z0-9\s]", " ", teks.lower())
    return re.sub(r"\s+", " ", teks).strip()


def cek_jawaban(jawaban: str, hewan: dict) -> bool:
    kunci = {normalisasi(hewan["nama"])} | {normalisasi(a) for a in hewan.get("alias", [])}
    return normalisasi(jawaban) in kunci


def gelar_dari_skor(skor: int):
    if skor >= 90:
        return "S.Hwn", "Luar Biasa! Sarjana Hewan sejati!", "🏆"
    if skor >= 60:
        return "S.k", "Hebat! Wawasan faunamu keren!", "🥈"
    if skor >= 30:
        return "S.Tda", "Cukup! Masih bisa lebih baik lagi!", "🥉"
    return "ADOHHHHH, heran", "Yuk ujian ulang dan baca petunjuknya!", "🤦"


def adegan_lari(kunci: str) -> str:
    return rapat(f"""
        <div class="adegan">
            <div class="bulan"></div>
            <div class="lapis jauh"></div>
            <div class="lapis dekat"></div>
            <div class="tanah"></div>
            <div class="pelari">
                {sprite_svg(kunci, 52, 0, "k1")}
                {sprite_svg(kunci, 52, 1, "k2")}
            </div>
        </div>
    """)


def bar_profil() -> str:
    kunci = st.session_state.karakter
    info = KARAKTER[kunci]
    nomor = min(st.session_state.no_soal + 1, TOTAL_SOAL)
    return rapat(f"""
        <div class="profil animasi">
            <div class="ava">{sprite_svg(kunci, 34, 1)}</div>
            <div class="info">
                <div class="nama-profil">{html.escape(st.session_state.nama_pemain)}</div>
                <div class="meta">{pokeball_svg(info['bola'], 16)} {info['nama']} · Soal {nomor}/{TOTAL_SOAL}</div>
            </div>
            <div class="skor">⭐ {st.session_state.skor}</div>
        </div>
    """)


def mulai_ulang():
    """Reset kuis; nama dan karakter tetap dipertahankan."""
    st.session_state.skor = 0
    st.session_state.no_soal = 0
    st.session_state.status = None          # None | "benar" | "lewat"
    st.session_state.clue_buka = 0
    st.session_state.salah_kali = 0
    st.session_state.emoji = "😄"
    st.session_state.balon = False
    st.session_state.soal_acak = random.sample(daftar_hewan, len(daftar_hewan))


st.session_state.setdefault("nama_pemain", "")
st.session_state.setdefault("karakter", "red")
if "soal_acak" not in st.session_state:
    mulai_ulang()


# ─────────────────────────────────────────────────────────────
# HALAMAN AWAL: nama + pilih karakter
# ─────────────────────────────────────────────────────────────
if st.session_state.nama_pemain == "":
    st.markdown(
        rapat("""
        <div class="glass animasi">
            <div class="logo">FAURARE QUIZ</div>
            <div class="subjudul">Kuis fauna endemik Nusantara · raih gelar Sarjana Hewan</div>
        </div>
        """),
        unsafe_allow_html=True,
    )
    st.markdown(adegan_lari(st.session_state.karakter), unsafe_allow_html=True)

    st.markdown("<div class='label-bagian'>Siapa namamu, calon penjelajah?</div>", unsafe_allow_html=True)
    st.text_input("Nama", key="input_nama", max_chars=20, placeholder="Ketik namamu di sini...",
                  label_visibility="collapsed")

    st.markdown("<div class='label-bagian'>Pilih karakter pendampingmu</div>", unsafe_allow_html=True)
    for kolom, (kunci, info) in zip(st.columns(3), KARAKTER.items()):
        with kolom:
            terpilih = st.session_state.karakter == kunci
            st.markdown(
                rapat(f"""
                <div class="kar-kartu {'pilih' if terpilih else ''}">
                    {sprite_svg(kunci, 58, 1)}
                    <div class="kar-nama">{info['nama']}</div>
                    {pokeball_svg(info['bola'], 26)}
                </div>
                """),
                unsafe_allow_html=True,
            )
            if st.button("✔ Dipilih" if terpilih else "Pilih", key=f"pilih_{kunci}",
                         use_container_width=True, type="primary" if terpilih else "secondary"):
                st.session_state.karakter = kunci
                st.rerun()

    st.write("")
    mulai = st.button("🌲 Mulai Ekspedisi", type="primary", use_container_width=True)

    with st.expander("📖 Cara bermain & gelar"):
        st.markdown(
            f"""
1. Lihat **kartu hewan** dan wilayah asalnya, lalu tebak namanya.
2. Bingung? Buka **petunjuk** satu per satu (maks. 3).
3. Jawaban benar = **+{POIN_PER_SOAL} poin** dan kamu bisa baca fakta uniknya.
4. Soal selalu **diacak**: {TOTAL_SOAL} soal, skor maksimal {SKOR_MAKS}.

🎓 **Gelar:** 90–100 `S.Hwn` · 60–80 `S.k` · 30–50 `S.Tda` · di bawah 30 `ADOHHHHH, heran`
"""
        )

    if mulai:
        nama = st.session_state.get("input_nama", "").strip()
        if not nama:
            st.warning("Tulis namamu dulu ya!")
            mainkan_sfx("salah")
        else:
            mulai_ulang()
            st.session_state.nama_pemain = nama
            info = KARAKTER[st.session_state.karakter]
            mainkan_sfx("mulai")
            render_sfx()
            st.markdown(
                rapat(f"""
                <div class="transisi">
                    <div class="bola">{pokeball_svg(info['bola'], 96)}</div>
                    <div class="teks">Memasuki hutan…</div>
                    <div class="sub">Selamat berpetualang, {html.escape(nama)}!</div>
                    <div class="kilat"></div>
                </div>
                """),
                unsafe_allow_html=True,
            )
            time.sleep(2.0)
            st.rerun()

    render_sfx()
    st.stop()


# ─────────────────────────────────────────────────────────────
# PERMAINAN
# ─────────────────────────────────────────────────────────────
nama_aman = html.escape(st.session_state.nama_pemain)

if st.session_state.no_soal < TOTAL_SOAL:
    h = st.session_state.soal_acak[st.session_state.no_soal]
    nomor = st.session_state.no_soal + 1

    st.markdown(bar_profil(), unsafe_allow_html=True)
    st.markdown(adegan_lari(st.session_state.karakter), unsafe_allow_html=True)

    if h.get("gambar"):
        kartu_visual = f"<img src='{html.escape(h['gambar'])}' style='max-width:100%; border-radius:16px; margin:10px 0;'>"
    else:
        kartu_visual = f"<span class='ikon-besar'>{h['ikon']}</span>"

    st.markdown(
        rapat(f"""
        <div class="glass kartu-hewan animasi">
            <span class="ikon-latar">{h['latar']}</span>
            <div class="nomor">Soal {nomor} / {TOTAL_SOAL}</div>
            <span class="lencana">📍 {html.escape(h['kategori'])}</span>
            {kartu_visual}
            <div class="tanya">Hewan endemik apakah ini?</div>
        </div>
        """),
        unsafe_allow_html=True,
    )

    # ── Setelah menjawab benar / menyerah: reaksi + fakta + tombol lanjut
    if st.session_state.status in ("benar", "lewat"):
        terakhir = nomor == TOTAL_SOAL
        nama_hewan = html.escape(h["nama"].title())
        fakta = html.escape(h["fakta"])
        if st.session_state.status == "benar":
            st.markdown(
                rapat(f"""
                <div class="glass hasil-benar animasi">
                    <div class="reaksi"><span>{st.session_state.emoji}</span><span>{h['ikon']}</span></div>
                    <h3 style="margin:0 0 6px 0; text-align:center;">Benar! +{POIN_PER_SOAL} poin</h3>
                    <b>🐾 {nama_hewan}</b><br>
                    <span>💡 <b>Fakta Unik:</b> {fakta}</span>
                </div>
                """),
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                rapat(f"""
                <div class="glass hasil-lewat animasi">
                    <div class="reaksi"><span>😿</span></div>
                    <h3 style="margin:0 0 6px 0; text-align:center;">Tidak apa-apa, kita belajar!</h3>
                    <b>🐾 Jawabannya: {nama_hewan}</b><br>
                    <span>💡 <b>Fakta Unik:</b> {fakta}</span>
                </div>
                """),
                unsafe_allow_html=True,
            )
        label = "🏁 Lihat Hasil Akhir" if terakhir else "➡️ Lanjut ke Soal Berikutnya"
        if st.button(label, use_container_width=True, type="primary"):
            st.session_state.status = None
            st.session_state.clue_buka = 0
            st.session_state.salah_kali = 0
            st.session_state.no_soal += 1
            if terakhir:
                mainkan_sfx("selesai")
            st.rerun()

    # ── Masih menebak
    else:
        for i in range(st.session_state.clue_buka):
            st.markdown(
                f"<div class='clue'><b>💡 Petunjuk {i + 1}:</b> {html.escape(h['clues'][i])}</div>",
                unsafe_allow_html=True,
            )
        if st.session_state.clue_buka < len(h["clues"]):
            sisa = len(h["clues"]) - st.session_state.clue_buka
            if st.button(f"💡 Buka Petunjuk Berikutnya ({sisa} tersisa)", use_container_width=True):
                st.session_state.clue_buka += 1
                st.rerun()

        with st.form(key=f"form_{st.session_state.no_soal}", clear_on_submit=True):
            jawaban = st.text_input("Ketik tebakan nama hewan:", placeholder="contoh: komodo")
            kirim = st.form_submit_button("🎯 Kirim Jawaban", use_container_width=True, type="primary")

        if kirim:
            if not jawaban.strip():
                st.warning("Ketik jawabanmu dulu ya!")
            elif cek_jawaban(jawaban, h):
                st.session_state.skor += POIN_PER_SOAL
                st.session_state.status = "benar"
                st.session_state.emoji = random.choice(EMOJI_BENAR)
                mainkan_sfx("benar")
                st.rerun()
            else:
                st.session_state.salah_kali += 1
                mainkan_sfx("salah")
                saran = "Coba buka petunjuk di atas!" if st.session_state.clue_buka < len(h["clues"]) else "Baca petunjuknya sekali lagi."
                st.markdown(
                    rapat(f"""
                    <div class="glass hasil-salah">
                        <div class="salah-baris">
                            <span class="emo">{random.choice(EMOJI_SALAH)}</span>
                            <div><b>Yah, belum tepat!</b> (salah: {st.session_state.salah_kali})<br>
                            <span style="opacity:0.85;">{saran}</span></div>
                        </div>
                    </div>
                    """),
                    unsafe_allow_html=True,
                )

        if st.button("🏳️ Menyerah & Lewati", use_container_width=True):
            st.session_state.status = "lewat"
            mainkan_sfx("lewat")
            st.rerun()

# ─────────────────────────────────────────────────────────────
# HALAMAN HASIL AKHIR
# ─────────────────────────────────────────────────────────────
else:
    skor = st.session_state.skor
    gelar, predikat, ikon_gelar = gelar_dari_skor(skor)
    kunci = st.session_state.karakter

    if not st.session_state.balon:
        st.session_state.balon = True
        st.balloons()

    st.markdown(adegan_lari(kunci), unsafe_allow_html=True)
    st.markdown(
        rapat(f"""
        <div class="glass animasi" style="text-align:center;">
            <div class="subjudul">🎉 Ujian &amp; Ekspedisi Nusantara Selesai 🎉</div>
            <h2 style="margin:6px 0 0 0;">Sidang Kelulusan: {nama_aman}</h2>
            <div style="margin-top:8px;">{sprite_svg(kunci, 64, 1)}</div>
            <div style="font-size:2.6rem;">{ikon_gelar}</div>
            <div class="gelar">{html.escape(gelar)}</div>
            <div style="font-weight:600;">{html.escape(predikat)}</div>
            <div style="margin-top:12px; font-size:1.15rem;">
                Total Nilai Akhir: <b>{skor} / {SKOR_MAKS}</b> poin
            </div>
        </div>
        """),
        unsafe_allow_html=True,
    )

    st.markdown("### 🏛️ Museum Mini Ensiklopedia Fauna Indonesia")
    st.caption(f"Pelajari kembali fakta unik dari ke-{TOTAL_SOAL} hewan endemik:")
    for i, item in enumerate(daftar_hewan, start=1):
        with st.expander(f"{item['ikon']} {i}. {item['nama'].title()} — {item['kategori']}"):
            st.write(f"**Fakta Unik:** {item['fakta']}")
            for c in item["clues"]:
                st.write(f"• {c}")

    st.divider()
    if st.button("🔄 Ujian Ulang (Soal Diacak)", use_container_width=True, type="primary"):
        mulai_ulang()
        mainkan_sfx("mulai")
        st.rerun()
    if st.button("👤 Ganti Pemain / Karakter", use_container_width=True):
        mulai_ulang()
        st.session_state.nama_pemain = ""
        st.session_state.pop("input_nama", None)
        st.rerun()

render_sfx()
