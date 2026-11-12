import base64
import html
import os
import random
import re
import textwrap

import streamlit as st
import streamlit.components.v1 as components

# ─────────────────────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RareFauna Retro Quiz",
    page_icon="🌲",
    layout="centered",
    initial_sidebar_state="expanded",
)

POIN_PER_SOAL = 10

# Opsional: taruh file "backsound.mp3" (musik tegang pilihanmu) di folder yang
# sama dengan app.py. Jika ada, file itu dipakai di pemutar sidebar. Jika tidak
# ada, dipakai musik chiptune tegang buatan sendiri (dibuat langsung di browser).
BACKSOUND_LOKAL = "backsound.mp3"

# ─────────────────────────────────────────────────────────────
# DATABASE 10 HEWAN ENDEMIK
# ─────────────────────────────────────────────────────────────
daftar_hewan = [
    {"nama": "komodo", "alias": ["komodo dragon", "biawak komodo"],
     "kategori": "Reptil Purba / NTT", "ikon": "🦎", "latar": "🏝️",
     "clues": ["Reptil terbesar di dunia yang masih hidup.",
               "Memiliki air liur beracun untuk melumpuhkan mangsa.",
               "Hewan endemik asli Pulau Komodo dan NTT."],
     "fakta": "Komodo adalah kadal terbesar di bumi yang panjangnya bisa mencapai 3 meter dan berat hingga 70 kg!"},
    {"nama": "orangutan", "alias": ["orang utan", "orang-utan"],
     "kategori": "Primata / Sumatera & Kalimantan", "ikon": "🦧", "latar": "🌴",
     "clues": ["Namanya berarti 'manusia hutan' dalam bahasa lokal.",
               "Memiliki bulu tebal berwarna jingga kecokelatan.",
               "Sebagian besar hidupnya dihabiskan di atas pohon."],
     "fakta": "Orangutan sangat cerdas dan mampu menggunakan tongkat serta alat alami untuk mencari makan."},
    {"nama": "badak jawa", "alias": ["badak"],
     "kategori": "Mamalia / Ujung Kulon", "ikon": "🦏", "latar": "🌿",
     "clues": ["Salah satu mamalia paling langka dan terancam punah di bumi.",
               "Memiliki cula tunggal (bercula satu) yang khas.",
               "Habitat aslinya dilindungi di Taman Nasional Ujung Kulon."],
     "fakta": "Badak jawa sangat menyukai kubangan lumpur di hutan hujan untuk mendinginkan tubuh mereka."},
    {"nama": "harimau sumatera", "alias": ["harimau sumatra", "macan sumatera", "macan sumatra"],
     "kategori": "Karnivora / Sumatera", "ikon": "🐅", "latar": "🍂",
     "clues": ["Spesies harimau terkecil yang masih bertahan hidup saat ini.",
               "Memiliki pola garis loreng hitam yang sangat rapat.",
               "Kucing besar ikonik yang asli berasal dari Pulau Sumatera."],
     "fakta": "Harimau sumatera adalah perenang yang sangat handal dan sering berenang di sungai."},
    {"nama": "anoa", "alias": ["kerbau kerdil"],
     "kategori": "Mamalia / Sulawesi", "ikon": "🐃", "latar": "⛰️",
     "clues": ["Sering dijuluki sebagai kerbau kerdil hutan.",
               "Memiliki sepasang tanduk lurus dan runcing tajam.",
               "Hewan endemik kebanggaan Pulau Sulawesi."],
     "fakta": "Anoa bersifat soliter (menyendiri) dan sangat menyukai kubangan air serta mata air pegunungan."},
    {"nama": "cendrawasih", "alias": ["cenderawasih", "burung cendrawasih", "burung cenderawasih", "burung surga"],
     "kategori": "Burung / Papua", "ikon": "🦜", "latar": "✨",
     "clues": ["Dijuluki secara internasional sebagai 'Bird of Paradise' (Burung Surga).",
               "Memiliki bulu ekor yang sangat megah, panjang, dan penuh warna.",
               "Habitat utamanya berada di rimbunnya hutan Papua."],
     "fakta": "Keindahan bulu cendrawasih membuat burung ini disakralkan sebagai simbol budaya Papua."},
    {"nama": "babirusa", "alias": ["babi rusa"],
     "kategori": "Mamalia / Sulawesi", "ikon": "🐗", "latar": "🦷",
     "clues": ["Penampakannya mirip perpaduan unik antara babi dan rusa.",
               "Memiliki taring melengkung ke atas yang menembus moncongnya.",
               "Satwa liar endemik yang hanya bisa ditemukan di Sulawesi."],
     "fakta": "Taring jantan babirusa bisa melingkar hampir menyentuh bagian mata seiring bertambahnya usia."},
    {"nama": "maleo", "alias": ["burung maleo"],
     "kategori": "Burung / Sulawesi", "ikon": "🥚", "latar": "🔥",
     "clues": ["Memiliki benjolan unik di atas kepalanya.",
               "Tidak mengerami telur, melainkan menimbunnya di dalam pasir.",
               "Memanfaatkan panas alami bumi / vulkanik untuk penetasan."],
     "fakta": "Anak burung maleo sudah bisa langsung terbang mandiri begitu menetas dari dalam tanah."},
    {"nama": "tarsius", "alias": ["tarsier", "tarsius sulawesi"],
     "kategori": "Primata / Sulawesi", "ikon": "👀", "latar": "🌿",
     "clues": ["Primata berukuran sangat kecil dengan mata bulat raksasa.",
               "Lehernya sangat fleksibel dan bisa berputar hingga 180 derajat.",
               "Suka melompat dari pohon ke pohon di hutan Sulawesi."],
     "fakta": "Bola mata tarsius sebenarnya lebih besar daripada otaknya sendiri!"},
    {"nama": "jalak bali", "alias": ["curik bali", "jalak putih"],
     "kategori": "Burung / Bali", "ikon": "🕊️", "latar": "🌺",
     "clues": ["Didominasi warna bulu putih bersih dengan lingkaran mata biru.",
               "Memiliki jambul indah di bagian belakang kepalanya.",
               "Satwa maskot fauna resmi Provinsi Bali."],
     "fakta": "Jalak bali termasuk salah satu burung pengicau paling dilindungi dan langka di dunia."},
]
TOTAL_SOAL = len(daftar_hewan)
SKOR_MAKS = TOTAL_SOAL * POIN_PER_SOAL

PUJIAN = [
    "Mantap, Explorer! Matamu setajam elang hutan!",
    "Luar biasa! Penjaga rimba pasti bangga padamu!",
    "Tepat sekali! Kamu memang jago satwa Nusantara!",
    "Kereeen! Satu hewan langka berhasil kamu kenali!",
    "Yeay! Ranger hutan memberimu jempol! 👍",
]
RATAPAN = [
    "Waduh, karakter pixel-mu tersandung akar pohon!",
    "Salah! Ada suara aneh dari semak-semak...",
    "Aduh! Kamu salah jalan di tengah hutan gelap!",
    "Bukan itu! Hewannya mengintip dan menggeleng...",
    "Yah, tebakanmu meleset! Coba buka petunjuk dulu.",
]
REAKSI_BENAR = ["😄", "🥳", "🤩", "😍", "🎉", "🐵", "🦜", "🐯"]


# <ART>
# ─────────────────────────────────────────────────────────────
# PIXEL ART — semua gambar dibuat dengan kode (SVG), tanpa file / internet
# ─────────────────────────────────────────────────────────────
def _data_uri_svg(svg: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def _pohon(rects, cx, dasar, tinggi, warna, gelap):
    """Satu pohon pinus pixel: tiga tingkat daun + batang."""
    tingkat = max(3, tinggi // 7)
    baris = tinggi - 3
    for r in range(baris):
        t = (r % (baris // tingkat + 1)) / (baris // tingkat + 1)
        lebar = 1 + int((r / baris) * (tinggi * 0.32)) + int(t * 3)
        lebar = lebar if lebar % 2 else lebar + 1
        y = dasar - tinggi + r
        rects.append(f'<rect x="{cx - lebar // 2}" y="{y}" width="{lebar}" height="1" fill="{warna}"/>')
        if r % 5 == 4:  # sisi gelap supaya terlihat bertekstur
            rects.append(f'<rect x="{cx - lebar // 2}" y="{y}" width="{max(1, lebar // 3)}" height="1" fill="{gelap}"/>')
    rects.append(f'<rect x="{cx - 1}" y="{dasar - 3}" width="2" height="3" fill="#2b1a10"/>')


def bangun_latar() -> str:
    """Hutan pinus misterius bergaya pixel art di malam hari (192x108 piksel)."""
    W, H = 192, 108
    rnd = random.Random(11)
    p = []
    # Langit berpita (gradasi pixel)
    warna_langit = ["#040b12", "#06121b", "#08192a", "#0a2230", "#0c2c36", "#0f3a3c", "#14504a", "#1a6354"]
    tinggi_pita = H // len(warna_langit) + 1
    for i, w in enumerate(warna_langit):
        p.append(f'<rect x="0" y="{i * tinggi_pita}" width="{W}" height="{tinggi_pita}" fill="{w}"/>')
    # Bintang berkedip
    for _ in range(38):
        x, y = rnd.randrange(W), rnd.randrange(0, 48)
        dur = round(rnd.uniform(1.6, 4.2), 1)
        p.append(
            f'<rect x="{x}" y="{y}" width="1" height="1" fill="#e2f3ff">'
            f'<animate attributeName="opacity" values="0.2;1;0.2" dur="{dur}s" repeatCount="indefinite"/></rect>'
        )
    # Bulan sabit pixel
    for dy in range(-8, 9):
        for dx in range(-8, 9):
            if dx * dx + dy * dy <= 64 and (dx + 3) ** 2 + (dy - 1) ** 2 > 56:
                p.append(f'<rect x="{150 + dx}" y="{20 + dy}" width="1" height="1" fill="#f1f5c4"/>')
    # Lapisan pohon: jauh -> dekat
    lapisan = [
        (78, (24, 32), "#0e3b38", "#0b302f", 9),
        (90, (32, 44), "#0a2a26", "#071f1d", 11),
        (102, (44, 62), "#051811", "#030f0b", 15),
    ]
    for dasar, (tmin, tmax), warna, gelap, jarak in lapisan:
        x = -2
        while x < W + 6:
            _pohon(p, x, dasar, rnd.randint(tmin, tmax), warna, gelap)
            x += jarak + rnd.randint(-3, 4)
        p.append(f'<rect x="0" y="{dasar}" width="{W}" height="{H - dasar}" fill="{warna}"/>')
        # Kabut tipis di tiap lapisan
        p.append(f'<rect x="0" y="{dasar - 5}" width="{W}" height="6" fill="#9fe3c8" opacity="0.06"/>')
    # Tanah + rumput depan
    p.append(f'<rect x="0" y="100" width="{W}" height="8" fill="#08150c"/>')
    for x in range(0, W, 2):
        if rnd.random() < 0.55:
            p.append(f'<rect x="{x}" y="{99 - rnd.randint(0, 1)}" width="1" height="2" fill="#14532d"/>')
    # Kunang-kunang melayang
    for _ in range(26):
        x, y = rnd.randrange(8, W - 8), rnd.randrange(50, 98)
        dur = round(rnd.uniform(2.5, 6.0), 1)
        dx = rnd.choice([-6, -4, 4, 6])
        p.append(
            f'<rect x="{x}" y="{y}" width="1" height="1" fill="#fde047">'
            f'<animate attributeName="opacity" values="0;1;0.2;1;0" dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="x" values="{x};{x + dx};{x}" dur="{dur * 2}s" repeatCount="indefinite"/></rect>'
        )
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'preserveAspectRatio="xMidYMax slice" shape-rendering="crispEdges">' + "".join(p) + "</svg>"
    )
    return _data_uri_svg(svg)


def bangun_sprite(frame: int) -> str:
    """Penjelajah pixel (topi safari + ransel), dua frame kaki untuk animasi lari."""
    r = [
        ("#7c4a1e", 2, 0, 8, 2), ("#7c4a1e", 1, 2, 10, 1),   # topi
        ("#f2c9a0", 3, 3, 6, 3), ("#111111", 4, 4, 1, 1), ("#111111", 7, 4, 1, 1),  # wajah
        ("#2f9e44", 3, 6, 6, 5), ("#5c3a14", 3, 9, 6, 1),    # badan + sabuk
        ("#b45309", 0, 6, 3, 5), ("#92400e", 0, 6, 3, 1),    # ransel
    ]
    if frame == 0:
        r += [("#f2c9a0", 8, 7, 2, 3),
              ("#1e3a8a", 3, 11, 2, 4), ("#111111", 3, 15, 3, 1),
              ("#1e3a8a", 7, 11, 2, 3), ("#111111", 7, 14, 2, 1)]
    else:
        r += [("#f2c9a0", 9, 7, 2, 3),
              ("#1e3a8a", 3, 11, 2, 3), ("#111111", 2, 14, 2, 1),
              ("#1e3a8a", 7, 11, 2, 4), ("#111111", 7, 15, 3, 1)]
    body = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"/>' for c, x, y, w, h in r)
    return _data_uri_svg(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 16" shape-rendering="crispEdges">{body}</svg>'
    )
# </ART>


# ─────────────────────────────────────────────────────────────
# CSS — tema pixel art hutan misterius
# ─────────────────────────────────────────────────────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');

html, body, .stApp, p, label, li, span, div, input, textarea, button {
    font-family: 'VT323', monospace;
}
.stApp p, .stApp li, .stApp label, [data-testid="stMarkdownContainer"] { font-size: 1.35rem; line-height: 1.25; }
h1, h2, h3, .judul, .pixel-font, .stButton button, [data-testid="stFormSubmitButton"] button {
    font-family: 'Press Start 2P', monospace !important;
}

.stApp {
    background:
        linear-gradient(rgba(2, 10, 8, 0.38), rgba(2, 10, 8, 0.38)),
        url("__LATAR__") center bottom / cover no-repeat fixed;
    background-color: #06121b;
    color: #e5f5e8;
}
.stApp, .stApp > header, .stApp .main { image-rendering: pixelated; }
[data-testid="stHeader"] { background: transparent; }
footer, #MainMenu { visibility: hidden; }
.block-container { position: relative; z-index: 2; max-width: 760px; padding-top: 1.2rem; padding-bottom: 130px; }
.stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label, .stApp li,
[data-testid="stMarkdownContainer"] { color: #e5f5e8; }
[data-testid="stCaptionContainer"] { color: #a7d7b5; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(4, 16, 12, 0.92);
    border-right: 4px solid #22c55e;
    z-index: 5;
}

/* Kotak pixel (kaca gelap + bingkai tebal) */
.pixel-box {
    background: rgba(6, 22, 16, 0.78);
    backdrop-filter: blur(4px);
    border: 4px solid #22c55e;
    box-shadow: 0 0 0 4px #04130c, 8px 8px 0 4px rgba(0, 0, 0, 0.55);
    padding: 20px 16px;
    margin: 6px 6px 22px;
    text-align: center;
}
.pixel-box.emas { border-color: #facc15; }
.pixel-box.hijau { border-color: #4ade80; background: rgba(21, 128, 61, 0.28); }
.pixel-box.merah { border-color: #f87171; background: rgba(153, 27, 27, 0.34); }
.pixel-box.oranye { border-color: #fb923c; background: rgba(154, 52, 18, 0.30); }

.judul {
    text-align: center; color: #86efac !important; line-height: 1.5;
    font-size: clamp(0.95rem, 4.4vw, 1.55rem); text-shadow: 3px 3px 0 #052e16;
    margin: 0 0 12px 0;
}
.judul .emas { color: #facc15; }
.sub { font-size: 1.45rem; opacity: 0.92; margin-bottom: 8px; }

.hud { display: flex; justify-content: space-between; gap: 8px; margin: 4px 6px 14px; }
.hud span {
    flex: 1; text-align: center; padding: 8px 4px; font-family: 'Press Start 2P', monospace;
    font-size: clamp(0.55rem, 2.6vw, 0.75rem); background: rgba(4, 19, 12, 0.85);
    border: 3px solid #facc15; color: #fde68a; box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.5);
}
.bar { height: 16px; margin: 0 6px 16px; background: #04130c; border: 3px solid #22c55e; padding: 2px; }
.bar > i { display: block; height: 100%; background: repeating-linear-gradient(90deg, #4ade80 0 8px, #22c55e 8px 10px); }

.lencana {
    display: inline-block; padding: 6px 10px; font-family: 'Press Start 2P', monospace;
    font-size: clamp(0.5rem, 2.4vw, 0.68rem); color: #052e16; background: #facc15;
    border: 3px solid #78350f; box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.5);
}
.ikon-besar {
    display: block; font-size: clamp(76px, 22vw, 120px); line-height: 1.2; margin: 12px 0 4px;
    animation: lompat 1.1s steps(2, end) infinite;
    filter: drop-shadow(5px 5px 0 rgba(0, 0, 0, 0.55));
}
.ikon-latar { position: absolute; right: 14px; top: 10px; font-size: 2rem; opacity: 0.6; }
.kartu { position: relative; }
.bisik { font-size: 1.45rem; font-style: italic; color: #bef264; margin-top: 4px; }

.clue {
    background: rgba(250, 204, 21, 0.10); border-left: 6px solid #facc15;
    padding: 8px 12px; margin: 8px 6px; font-size: 1.4rem; animation: muncul .35s steps(4) both;
}

/* Reaksi benar / salah */
.reaksi { font-size: clamp(2.4rem, 12vw, 4rem); letter-spacing: 6px; margin-bottom: 6px; }
.reaksi.benar span { display: inline-block; animation: lompat .6s steps(2, end) infinite; }
.reaksi.benar span:nth-child(2) { animation-delay: .15s; }
.reaksi.benar span:nth-child(3) { animation-delay: .3s; }
.reaksi.salah { animation: getar .5s steps(2, end) 3; }
.teks-reaksi { font-family: 'Press Start 2P', monospace; font-size: clamp(.6rem, 3vw, .85rem); line-height: 1.7; margin-bottom: 8px; }
.kilat-merah::after {
    content: ""; position: fixed; inset: 0; background: rgba(239, 68, 68, 0.28);
    pointer-events: none; z-index: 40; animation: kilat .7s steps(5) forwards;
}
.hujan { position: fixed; top: -50px; font-size: 1.8rem; pointer-events: none; z-index: 40; animation: jatuh 3.2s linear forwards; }

.gelar {
    text-align: center; font-family: 'Press Start 2P', monospace; color: #facc15;
    font-size: clamp(1.3rem, 7vw, 2.6rem); text-shadow: 4px 4px 0 #78350f; margin: 10px 0; line-height: 1.4;
}

/* Tombol pixel */
.stButton > button, [data-testid="stFormSubmitButton"] > button {
    min-height: 3.2rem; border-radius: 0; border: 4px solid #052e16; color: #052e16;
    font-size: clamp(.55rem, 2.7vw, .78rem); line-height: 1.5; padding: 10px 8px;
    background: #4ade80; box-shadow: 0 6px 0 #166534, 0 6px 0 4px #04130c;
    transition: none; margin-bottom: 8px;
}
.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover { background: #86efac; color: #052e16; border-color: #052e16; }
.stButton > button:active, [data-testid="stFormSubmitButton"] > button:active { transform: translateY(5px); box-shadow: 0 1px 0 #166534, 0 1px 0 4px #04130c; }
.stButton > button[kind="primary"], [data-testid="stFormSubmitButton"] > button[kind="primary"] {
    background: #facc15; box-shadow: 0 6px 0 #a16207, 0 6px 0 4px #04130c;
}
.stButton > button[kind="primary"]:hover { background: #fde047; }

/* Input */
.stTextInput input {
    min-height: 3.2rem; border-radius: 0 !important; font-size: 1.6rem;
    background: #04130c !important; color: #f0fdf4 !important; border: 4px solid #22c55e !important;
}
.stTextInput input::placeholder { color: #86a894 !important; }
.stTextInput input:focus { border-color: #facc15 !important; box-shadow: none !important; }
[data-testid="stForm"] { background: rgba(6, 22, 16, 0.72); border: 4px dashed #22c55e; border-radius: 0; }
[data-testid="stExpander"] { background: rgba(6, 22, 16, 0.78); border: 3px solid #22c55e; border-radius: 0; }
[data-testid="stMetricValue"] { font-family: 'Press Start 2P', monospace; color: #facc15; font-size: 1.3rem; }
[data-testid="stMetricLabel"] p { color: #a7d7b5; }
[data-testid="stAlert"] { border-radius: 0; border: 3px solid currentColor; }
hr { border-color: rgba(74, 222, 128, 0.35) !important; }
iframe[height="0"] { display: none; }

/* Lintasan penjelajah (gaya runner retro) */
.lintasan { position: fixed; left: 0; right: 0; bottom: 0; height: 104px; pointer-events: none; z-index: 1; overflow: hidden; }
.tanah {
    position: absolute; left: 0; right: 0; bottom: 0; height: 22px;
    background:
        repeating-linear-gradient(90deg, transparent 0 14px, rgba(0, 0, 0, .35) 14px 18px, transparent 18px 32px),
        linear-gradient(#22c55e 0 6px, #166534 6px 10px, #3f2a14 10px 100%);
    background-size: 32px 100%, 100% 100%;
    border-top: 4px solid #04130c; animation: geser .45s linear infinite;
}
.penjelajah { position: absolute; bottom: 20px; left: 0; width: 60px; height: 80px; animation: lari 15s linear infinite; }
.penjelajah .isi { position: absolute; inset: 0; animation: ayun .36s steps(1) infinite; }
.penjelajah img { position: absolute; inset: 0; width: 100%; height: 100%; image-rendering: pixelated; }
.penjelajah .fa { animation: fa .36s steps(1) infinite; }
.penjelajah .fb { animation: fb .36s steps(1) infinite; }
.penjelajah .awan {
    position: absolute; left: 62px; top: -4px; white-space: nowrap; font-family: 'Press Start 2P', monospace;
    font-size: .5rem; color: #052e16; background: #fef9c3; border: 3px solid #04130c; padding: 5px 6px;
}
@keyframes lari { from { transform: translateX(-90px); } to { transform: translateX(calc(100vw + 200px)); } }
@keyframes geser { from { background-position: 0 0, 0 0; } to { background-position: -32px 0, 0 0; } }
@keyframes ayun { 0% { transform: translateY(0); } 50% { transform: translateY(-4px); } }
@keyframes fa { 0% { opacity: 1; } 50% { opacity: 0; } }
@keyframes fb { 0% { opacity: 0; } 50% { opacity: 1; } }
@keyframes lompat { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-12px); } }
@keyframes getar { 0%, 100% { transform: translateX(0); } 25% { transform: translateX(-10px); } 75% { transform: translateX(10px); } }
@keyframes kilat { 0% { opacity: 1; } 100% { opacity: 0; } }
@keyframes jatuh { to { transform: translateY(110vh) rotate(260deg); } }
@keyframes muncul { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }

@media (max-width: 640px) {
    .block-container { padding-left: .7rem; padding-right: .7rem; }
    .pixel-box { padding: 14px 10px; margin-left: 2px; margin-right: 2px; }
    .penjelajah { width: 48px; height: 64px; }
    .penjelajah .awan { display: none; }
}
@media (prefers-reduced-motion: reduce) {
    .penjelajah, .tanah, .ikon-besar, .reaksi span, .reaksi.salah { animation: none !important; }
    .penjelajah { left: 20px; }
}
"""


def blok(teks: str):
    st.markdown(textwrap.dedent(teks).strip(), unsafe_allow_html=True)


def pasang_tema():
    st.markdown(f"<style>{CSS.replace('__LATAR__', bangun_latar())}</style>", unsafe_allow_html=True)
    blok(
        f"""
        <div class="lintasan">
          <div class="penjelajah">
            <div class="isi">
              <img class="fa" src="{bangun_sprite(0)}" alt="">
              <img class="fb" src="{bangun_sprite(1)}" alt="">
            </div>
            <div class="awan">Ayo jelajah!</div>
          </div>
          <div class="tanah"></div>
        </div>
        """
    )


# ─────────────────────────────────────────────────────────────
# AUDIO
# ─────────────────────────────────────────────────────────────
PEMUTAR_SINTESIS = """
<style>
  body { margin: 0; font-family: monospace; color: #e5f5e8; }
  .w { background: #04130c; border: 3px solid #facc15; padding: 8px; }
  button { width: 100%; padding: 10px 4px; font-family: monospace; font-weight: bold; font-size: 14px;
           color: #052e16; background: #facc15; border: 3px solid #78350f; cursor: pointer; }
  button:active { transform: translateY(2px); }
  .r { display: flex; align-items: center; gap: 8px; margin-top: 8px; font-size: 13px; }
  input[type=range] { flex: 1; accent-color: #facc15; }
  .s { margin-top: 6px; font-size: 12px; opacity: .85; }
</style>
<div class="w">
  <button id="tb">▶ MAINKAN MUSIK</button>
  <div class="r"><span>🔊</span><input id="vol" type="range" min="0" max="100" value="45"></div>
  <div class="s" id="st">Musik tegang 8-bit (loop)</div>
</div>
<script>
(function () {
  var AC = window.AudioContext || window.webkitAudioContext, ctx = null, master = null;
  var main = false, timer = null, step = 0, next = 0;
  var BPM = 150, S = 60 / BPM / 4;
  var roots = [110, 87.31, 98, 82.41];                       // Am, F, G, E
  var chords = [[220, 261.63, 329.63], [174.61, 220, 261.63], [196, 246.94, 293.66], [164.81, 207.65, 246.94]];
  var noise = null;
  function mk() {
    ctx = new AC(); master = ctx.createGain(); master.gain.value = 0.45; master.connect(ctx.destination);
    var b = ctx.createBuffer(1, ctx.sampleRate, ctx.sampleRate), d = b.getChannelData(0);
    for (var i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
    noise = b;
  }
  function osc(f, t, dur, type, vol) {
    var o = ctx.createOscillator(), g = ctx.createGain();
    o.type = type; o.frequency.value = f;
    g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    o.connect(g); g.connect(master); o.start(t); o.stop(t + dur + 0.02);
  }
  function kick(t) {
    var o = ctx.createOscillator(), g = ctx.createGain();
    o.frequency.setValueAtTime(150, t); o.frequency.exponentialRampToValueAtTime(40, t + 0.14);
    g.gain.setValueAtTime(0.9, t); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.16);
    o.connect(g); g.connect(master); o.start(t); o.stop(t + 0.2);
  }
  function hit(t, dur, vol, hp) {
    var n = ctx.createBufferSource(), f = ctx.createBiquadFilter(), g = ctx.createGain();
    n.buffer = noise; f.type = 'highpass'; f.frequency.value = hp;
    g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    n.connect(f); f.connect(g); g.connect(master); n.start(t); n.stop(t + dur + 0.02);
  }
  function play(s, t) {
    var bar = Math.floor(s / 16) % 4, k = s % 16;
    var tones = chords[bar];
    if (k % 2 === 0) osc(roots[bar] * (k % 4 === 2 ? 2 : 1), t, S * 1.8, 'triangle', 0.38);   // bass berdenyut
    var arp = [0, 1, 2, 1][k % 4], oct = (k >= 8 && bar % 2 === 1) ? 2 : 1;
    osc(tones[arp] * oct, t, S * 0.9, 'square', 0.09);                                          // arpeggio tegang
    if (k % 8 === 0) osc(tones[2] * 2, t, S * 3.2, 'sawtooth', 0.05);                           // nada panjang
    if (k % 4 === 0) kick(t);
    if (k === 4 || k === 12) hit(t, 0.12, 0.35, 1800);                                           // snare
    hit(t, 0.03, 0.12, 7000);                                                                    // hi-hat
    if (bar === 3 && k >= 12) hit(t, 0.06, 0.3, 2500);                                           // roll penutup
  }
  function sched() {
    while (next < ctx.currentTime + 0.25) { play(step, next); next += S; step = (step + 1) % 64; }
  }
  var tb = document.getElementById('tb'), vol = document.getElementById('vol'), st = document.getElementById('st');
  tb.onclick = function () {
    if (!AC) { st.textContent = 'Browser tidak mendukung audio.'; return; }
    if (!ctx) mk();
    if (!main) {
      ctx.resume(); next = ctx.currentTime + 0.08; step = 0; timer = setInterval(sched, 60);
      main = true; tb.textContent = '⏸ JEDA MUSIK'; st.textContent = '♪ Musik sedang berputar...';
    } else {
      clearInterval(timer); main = false; tb.textContent = '▶ MAINKAN MUSIK'; st.textContent = 'Dijeda';
    }
  };
  vol.oninput = function () { if (master) master.gain.value = vol.value / 100; };
})();
</script>
"""


def tampilkan_pemutar():
    """Pemutar musik di sidebar. Harus dirender PERTAMA agar tidak ter-reset saat halaman berganti."""
    if os.path.exists(BACKSOUND_LOKAL):
        with open(BACKSOUND_LOKAL, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        components.html(
            f"""
            <audio controls loop preload="auto" style="width:100%">
              <source src="data:audio/mpeg;base64,{b64}" type="audio/mpeg">
            </audio>
            """,
            height=60,
        )
    else:
        components.html(PEMUTAR_SINTESIS, height=118)


SFX_JS = """
<script>
(function () {
  var P = window.parent;
  function ctx() {
    var AC = P.AudioContext || P.webkitAudioContext; if (!AC) return null;
    if (!P.__rfCtx) P.__rfCtx = new AC();
    if (P.__rfCtx.state === 'suspended') P.__rfCtx.resume();
    return P.__rfCtx;
  }
  function nada(f, mulai, dur, tipe, vol) {
    var c = ctx(); if (!c) return;
    var o = c.createOscillator(), g = c.createGain(), t = c.currentTime + mulai;
    o.type = tipe; o.frequency.setValueAtTime(f, t);
    g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(vol, t + 0.02);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    o.connect(g); g.connect(c.destination); o.start(t); o.stop(t + dur + 0.05);
  }
  P.__rfSfx = function (j) {
    if (j === 'klik') nada(700, 0, 0.07, 'square', 0.07);
    if (j === 'benar') [523, 659, 784, 1047, 1319].forEach(function (f, i) { nada(f, i * 0.08, 0.2, 'square', 0.1); });
    if (j === 'salah') { nada(196, 0, 0.22, 'sawtooth', 0.14); nada(147, 0.2, 0.22, 'sawtooth', 0.14); nada(98, 0.4, 0.5, 'sawtooth', 0.16); }
    if (j === 'lewat') { nada(440, 0, 0.12, 'square', 0.09); nada(330, 0.12, 0.12, 'square', 0.09); nada(262, 0.24, 0.25, 'square', 0.09); }
    if (j === 'selesai') [523, 659, 784, 1047, 784, 1047, 1319, 1568].forEach(function (f, i) { nada(f, i * 0.12, 0.28, 'square', 0.1); });
  };
  if (!P.__rfBound) {
    P.__rfBound = true;
    P.document.addEventListener('click', function (e) {
      if (e.target && e.target.closest && e.target.closest('button')) P.__rfSfx('klik');
    }, true);
  }
  var jenis = "__JENIS__";   /* nonce: __NONCE__ */
  if (jenis) setTimeout(function () { P.__rfSfx(jenis); }, 150);
})();
</script>
"""


def mainkan_sfx(jenis: str):
    st.session_state.sfx = jenis


def render_sfx():
    jenis = st.session_state.pop("sfx", "")
    st.session_state.nonce = st.session_state.get("nonce", 0) + 1
    components.html(
        SFX_JS.replace("__JENIS__", jenis).replace("__NONCE__", str(st.session_state.nonce)),
        height=0,
    )


# ─────────────────────────────────────────────────────────────
# LOGIKA
# ─────────────────────────────────────────────────────────────
def normalisasi(teks: str) -> str:
    teks = re.sub(r"[^a-z0-9\s]", " ", teks.lower())
    return re.sub(r"\s+", " ", teks).strip()


def cek_jawaban(jawaban: str, hewan: dict) -> bool:
    kunci = {normalisasi(hewan["nama"])} | {normalisasi(a) for a in hewan.get("alias", [])}
    return normalisasi(jawaban) in kunci


def gelar_dari_skor(skor: int):
    if skor >= 90:
        return "S.Hwn", "Master Penjaga Hutan Nusantara!", "🏆"
    if skor >= 60:
        return "S.k", "Penjelajah Handal!", "🥈"
    if skor >= 30:
        return "S.Tda", "Petualang Pemula!", "🥉"
    return "ADOHHHHH, heran", "Tersesat di semak belukar!", "🏕️"


def mulai_ulang(pertahankan_nama: bool = True):
    nama = st.session_state.get("nama_pemain", "") if pertahankan_nama else ""
    st.session_state.skor = 0
    st.session_state.no_soal = 0
    st.session_state.status = None        # None | "benar" | "lewat"
    st.session_state.clue_buka = 0
    st.session_state.salah_kali = 0
    st.session_state.reaksi_salah = ""
    st.session_state.reaksi_benar = None
    st.session_state.nama_pemain = nama
    st.session_state.soal_acak = random.sample(daftar_hewan, len(daftar_hewan))


def hujan_emoji(daftar, jumlah=14):
    rnd = random.Random()
    item = "".join(
        f'<span class="hujan" style="left:{rnd.randint(2, 95)}%;animation-delay:{rnd.random() * 1.2:.2f}s">'
        f"{rnd.choice(daftar)}</span>"
        for _ in range(jumlah)
    )
    st.markdown(item, unsafe_allow_html=True)


if "soal_acak" not in st.session_state:
    mulai_ulang(pertahankan_nama=False)

# ─────────────────────────────────────────────────────────────
# SIDEBAR (pemutar musik dirender paling awal agar stabil)
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎵 MUSIK TEGANG")
    tampilkan_pemutar()
    st.caption("Tekan tombol putar dulu (aturan browser). Di HP, buka sidebar lewat ikon » di kiri atas.")

pasang_tema()
sudah_masuk = st.session_state.nama_pemain != ""

if sudah_masuk:
    with st.sidebar:
        st.divider()
        st.markdown(f"**🌲 Explorer: {html.escape(st.session_state.nama_pemain)}**")
        st.metric("Skor", f"{st.session_state.skor} Poin")
        st.progress(min(st.session_state.no_soal / TOTAL_SOAL, 1.0))
        st.caption(f"Pos {min(st.session_state.no_soal + 1, TOTAL_SOAL)} / {TOTAL_SOAL}")
        st.divider()
        if st.button("🔄 Mulai Ulang (Acak)", use_container_width=True):
            mulai_ulang()
            st.rerun()

# ─────────────────────────────────────────────────────────────
# HALAMAN DEPAN
# ─────────────────────────────────────────────────────────────
if not sudah_masuk:
    blok(
        """
        <div class="pixel-box emas">
          <div class="judul">🌲 RAREFAUNA<br><span class="emas">8-BIT EXPEDITION</span> 🌲</div>
          <div class="sub">Jelajahi hutan misterius, kenali satwa langka Nusantara, dan raih gelar Sarjana Satwa Sejati!</div>
          <div style="font-size:2.6rem;">🦧 🐅 🦏 🦜 🦎</div>
        </div>
        """
    )
    blok(
        """
        <div class="pixel-box" style="text-align:left;">
          <div class="pixel-font" style="font-size:.7rem;margin-bottom:10px;color:#facc15;">📖 CARA BERMAIN</div>
          1. Lihat kartu hewan dan wilayah asalnya.<br>
          2. Ketik nama hewannya, lalu tekan Enter / tombol tebak.<br>
          3. Bingung? Buka petunjuk satu per satu (maks. 3).<br>
          4. Benar = +10 poin &amp; baca fakta uniknya. Soal selalu diacak!<br>
          5. Gelar: 90-100 <b>S.Hwn</b> · 60-80 <b>S.k</b> · 30-50 <b>S.Tda</b> · &lt;30 <b>ADOHHHHH, heran</b>
        </div>
        """
    )
    with st.form("form_daftar"):
        nama = st.text_input("🎮 Masukkan Nama Explorer:", placeholder="Ketik namamu...")
        masuk = st.form_submit_button("🕹️ MULAI PETUALANGAN", use_container_width=True, type="primary")
    if masuk:
        if nama.strip():
            mulai_ulang(pertahankan_nama=False)
            st.session_state.nama_pemain = nama.strip()
            mainkan_sfx("benar")
            st.rerun()
        else:
            st.warning("⚠️ Masukkan nama dulu, Explorer!")
            mainkan_sfx("salah")
    render_sfx()
    st.stop()

# ─────────────────────────────────────────────────────────────
# PERMAINAN
# ─────────────────────────────────────────────────────────────
if st.session_state.no_soal < TOTAL_SOAL:
    h = st.session_state.soal_acak[st.session_state.no_soal]
    nomor = st.session_state.no_soal + 1
    persen = int(st.session_state.no_soal / TOTAL_SOAL * 100)

    blok(
        f"""
        <div class="hud">
          <span>⭐ {st.session_state.skor}</span>
          <span>🧭 {nomor}/{TOTAL_SOAL}</span>
        </div>
        <div class="bar"><i style="width:{persen}%"></i></div>
        <div class="pixel-box kartu">
          <span class="ikon-latar">{h['latar']}</span>
          <span class="lencana">📍 {html.escape(h['kategori'])}</span>
          <span class="ikon-besar">{h['ikon']}</span>
          <div class="bisik">"Makhluk misterius terlihat di semak-semak hutan..."</div>
        </div>
        """
    )

    # ── Jawaban benar / menyerah → fakta + tombol lanjut
    if st.session_state.status in ("benar", "lewat"):
        terakhir = nomor == TOTAL_SOAL
        if st.session_state.status == "benar":
            e = st.session_state.reaksi_benar or ["😄", "🥳", "🎉"]
            hujan_emoji(["🎉", "⭐", "🌟", "🍃", "✨"], 14)
            blok(
                f"""
                <div class="pixel-box hijau">
                  <div class="reaksi benar"><span>{e[0]}</span><span>{e[1]}</span><span>{e[2]}</span></div>
                  <div class="teks-reaksi">{html.escape(st.session_state.pujian)}</div>
                  <div class="pixel-font" style="font-size:.7rem;color:#facc15;margin:8px 0;">+{POIN_PER_SOAL} POIN</div>
                  <div style="font-size:1.5rem;">🐾 <b>{html.escape(h['nama'].title())}</b></div>
                  <div style="font-size:1.45rem;margin-top:6px;">💡 <b>Fakta Hutan:</b> {html.escape(h['fakta'])}</div>
                </div>
                """
            )
        else:
            blok(
                f"""
                <div class="pixel-box oranye">
                  <div class="reaksi">🏃💨</div>
                  <div class="teks-reaksi">KAMU KABUR!</div>
                  <div style="font-size:1.5rem;">🐾 Jawabannya: <b>{html.escape(h['nama'].title())}</b></div>
                  <div style="font-size:1.45rem;margin-top:6px;">💡 <b>Fakta Hutan:</b> {html.escape(h['fakta'])}</div>
                </div>
                """
            )
        label = "🏁 LIHAT HASIL AKHIR" if terakhir else "➡️ LANJUT KE SOAL BERIKUTNYA"
        if st.button(label, use_container_width=True, type="primary"):
            st.session_state.status = None
            st.session_state.clue_buka = 0
            st.session_state.salah_kali = 0
            st.session_state.reaksi_salah = ""
            st.session_state.no_soal += 1
            if terakhir:
                mainkan_sfx("selesai")
            st.rerun()

    # ── Masih menebak
    else:
        if st.session_state.reaksi_salah:
            blok(
                f"""
                <div class="kilat-merah"></div>
                <div class="pixel-box merah">
                  <div class="reaksi salah">😭👎❌</div>
                  <div class="teks-reaksi">{html.escape(st.session_state.reaksi_salah)}</div>
                  <div style="font-size:1.4rem;">Percobaan salah: {st.session_state.salah_kali} — ayo tebak lagi!</div>
                </div>
                """
            )
            hujan_emoji(["😭", "👎", "💧"], 8)

        for i in range(st.session_state.clue_buka):
            blok(f'<div class="clue"><b>💡 Petunjuk {i + 1}:</b> {html.escape(h["clues"][i])}</div>')
        if st.session_state.clue_buka < len(h["clues"]):
            sisa = len(h["clues"]) - st.session_state.clue_buka
            if st.button(f"🔍 BUKA PETUNJUK ({sisa} tersisa)", use_container_width=True):
                st.session_state.clue_buka += 1
                st.rerun()

        with st.form(key=f"form_{st.session_state.no_soal}", clear_on_submit=True):
            jawaban = st.text_input("Ketik nama hewan yang kamu temui:", placeholder="contoh: komodo")
            kirim = st.form_submit_button("⚔️ KONFIRMASI TEBAKAN", use_container_width=True, type="primary")

        if kirim:
            if not jawaban.strip():
                st.warning("Ketik jawabanmu dulu ya, Explorer!")
            elif cek_jawaban(jawaban, h):
                st.session_state.skor += POIN_PER_SOAL
                st.session_state.status = "benar"
                st.session_state.reaksi_salah = ""
                st.session_state.pujian = random.choice(PUJIAN)
                st.session_state.reaksi_benar = random.sample(REAKSI_BENAR, 3)
                mainkan_sfx("benar")
                st.rerun()
            else:
                st.session_state.salah_kali += 1
                st.session_state.reaksi_salah = random.choice(RATAPAN)
                mainkan_sfx("salah")
                st.rerun()

        if st.button("🏳️ KABUR / LEWATI", use_container_width=True):
            st.session_state.status = "lewat"
            st.session_state.reaksi_salah = ""
            mainkan_sfx("lewat")
            st.rerun()

# ─────────────────────────────────────────────────────────────
# HASIL AKHIR
# ─────────────────────────────────────────────────────────────
else:
    skor = st.session_state.skor
    gelar, predikat, ikon_gelar = gelar_dari_skor(skor)
    st.balloons()
    blok(
        f"""
        <div class="pixel-box emas">
          <div class="judul">🏆 EKSPEDISI HUTAN SELESAI 🏆</div>
          <div class="sub">Sidang Kelulusan: <b>{html.escape(st.session_state.nama_pemain)}</b></div>
          <div style="font-size:3rem;">{ikon_gelar}</div>
          <div class="gelar">{html.escape(gelar)}</div>
          <div class="teks-reaksi">{html.escape(predikat)}</div>
          <div class="sub">Total Poin: <b>{skor} / {SKOR_MAKS}</b></div>
        </div>
        """
    )
    st.markdown("### 🏛️ MUSEUM ARSIP SATWA HUTAN")
    for i, item in enumerate(daftar_hewan, start=1):
        with st.expander(f"{item['ikon']} {i}. {item['nama'].title()} — {item['kategori']}"):
            st.write(f"**Arsip Fakta:** {item['fakta']}")
            for c in item["clues"]:
                st.write(f"• {c}")
    st.divider()
    if st.button("🔄 MULAI EKSPEDISI BARU (ACAK ULANG)", use_container_width=True, type="primary"):
        mulai_ulang()
        mainkan_sfx("klik")
        st.rerun()

render_sfx()
