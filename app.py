import html
import json
import random
import re
import time
from urllib.parse import quote

import streamlit as st
import streamlit.components.v1 as components

# Catatan: butuh Streamlit >= 1.39 (untuk class .st-key-... pada tombol Start & Pixel Critter).

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
BONUS_CRITTER = 5        # poin per Pixel Critter yang ditemukan
JUMLAH_CRITTER = 3       # berapa soal yang disembuni critter
MAX_NYAWA = 3            # jumlah nyawa (hati) per permainan
OFFSET_FOTO = 12.6       # detik: foto bersama baru muncul setelah adegan penangkapan pelaku

# ─────────────────────────────────────────────────────────────
# DATABASE HEWAN
# "gambar" opsional: isi link foto jika ingin foto asli (menggantikan sprite pixel di kartu soal).
# "alias" opsional: variasi ejaan jawaban yang tetap dianggap benar.
# Sprite pixel tiap hewan ada di SPRITE_HEWAN (di bawah), dikunci dengan "nama".
# ─────────────────────────────────────────────────────────────
daftar_hewan = [
    {"nama": "komodo", "alias": ["komodo dragon", "biawak komodo"],
     "kategori": "Reptil Purba / NTT", "latar": "🏝️", "gambar": "",
     "clues": ["Reptil terbesar di dunia yang masih hidup.",
               "Memiliki air liur beracun untuk melumpuhkan mangsa.",
               "Hewan endemik asli Pulau Komodo dan NTT."],
     "fakta": "Komodo adalah kadal terbesar di bumi yang panjangnya bisa mencapai 3 meter dan berat hingga 70 kg!"},
    {"nama": "orangutan", "alias": ["orang utan", "orang-utan"],
     "kategori": "Primata / Sumatera & Kalimantan", "latar": "🌴", "gambar": "",
     "clues": ["Namanya berarti 'manusia hutan' dalam bahasa lokal.",
               "Memiliki bulu tebal berwarna jingga kecokelatan.",
               "Sebagian besar hidupnya dihabiskan di atas pohon."],
     "fakta": "Orangutan sangat cerdas dan mampu menggunakan tongkat serta alat alami untuk mencari makan."},
    {"nama": "badak jawa", "alias": ["badak"],
     "kategori": "Mamalia / Ujung Kulon", "latar": "🌿", "gambar": "",
     "clues": ["Salah satu mamalia paling langka dan terancam punah di bumi.",
               "Memiliki cula tunggal (bercula satu) yang khas.",
               "Habitat aslinya dilindungi di Taman Nasional Ujung Kulon."],
     "fakta": "Badak jawa sangat menyukai kubangan lumpur di hutan hujan untuk mendinginkan tubuh mereka."},
    {"nama": "harimau sumatera", "alias": ["harimau sumatra", "macan sumatera", "macan sumatra"],
     "kategori": "Karnivora / Sumatera", "latar": "🍂", "gambar": "",
     "clues": ["Spesies harimau terkecil yang masih bertahan hidup saat ini.",
               "Memiliki pola garis loreng hitam yang sangat rapat.",
               "Kucing besar ikonik yang asli berasal dari Pulau Sumatera."],
     "fakta": "Harimau sumatera adalah perenang yang sangat handal dan sering berenang di sungai."},
    {"nama": "anoa", "alias": ["kerbau kerdil"],
     "kategori": "Mamalia / Sulawesi", "latar": "⛰️", "gambar": "",
     "clues": ["Sering dijuluki sebagai kerbau kerdil hutan.",
               "Memiliki sepasang tanduk lurus dan runcing tajam.",
               "Hewan endemik kebanggaan Pulau Sulawesi."],
     "fakta": "Anoa bersifat soliter (menyendiri) dan sangat menyukai kubangan air serta mata air pegunungan."},
    {"nama": "cendrawasih", "alias": ["cenderawasih", "burung cendrawasih", "burung cenderawasih", "burung surga"],
     "kategori": "Burung / Papua", "latar": "✨", "gambar": "",
     "clues": ["Dijuluki secara internasional sebagai 'Bird of Paradise' (Burung Surga).",
               "Memiliki bulu ekor yang sangat megah, panjang, dan penuh warna.",
               "Habitat utamanya berada di rimbunnya hutan Papua."],
     "fakta": "Keindahan bulu cendrawasih membuat burung ini disakralkan sebagai simbol budaya Papua."},
    {"nama": "babirusa", "alias": ["babi rusa"],
     "kategori": "Mamalia / Sulawesi", "latar": "🦷", "gambar": "",
     "clues": ["Penampakannya mirip perpaduan unik antara babi dan rusa.",
               "Memiliki taring melengkung ke atas yang menembus moncongnya.",
               "Satwa liar endemik yang hanya bisa ditemukan di Sulawesi."],
     "fakta": "Taring jantan babirusa bisa melingkar hampir menyentuh bagian mata seiring bertambahnya usia."},
    {"nama": "maleo", "alias": ["burung maleo"],
     "kategori": "Burung / Sulawesi", "latar": "🔥", "gambar": "",
     "clues": ["Memiliki benjolan unik di atas kepalanya.",
               "Tidak mengerami telur, melainkan menimbunnya di dalam pasir.",
               "Memanfaatkan panas alami bumi / vulkanik untuk penetasan."],
     "fakta": "Anak burung maleo sudah bisa langsung terbang mandiri begitu menetas dari dalam tanah."},
    {"nama": "tarsius", "alias": ["tarsier", "tarsius sulawesi"],
     "kategori": "Primata / Sulawesi", "latar": "🌿", "gambar": "",
     "clues": ["Primata berukuran sangat kecil dengan mata bulat raksasa.",
               "Lehernya sangat fleksibel dan bisa berputar hingga 180 derajat.",
               "Suka melompat dari pohon ke pohon di hutan Sulawesi."],
     "fakta": "Bola mata tarsius sebenarnya lebih besar daripada otaknya sendiri!"},
    {"nama": "jalak bali", "alias": ["curik bali", "jalak putih"],
     "kategori": "Burung / Bali", "latar": "🌺", "gambar": "",
     "clues": ["Didominasi warna bulu putih bersih dengan lingkaran mata biru.",
               "Memiliki jambul indah di bagian belakang kepalanya.",
               "Satwa maskot fauna resmi Provinsi Bali."],
     "fakta": "Jalak bali termasuk salah satu burung pengicau paling dilindungi dan langka di dunia."},
]
# Hewan ke-10 (dipisah supaya mudah ditambah / diganti).
daftar_hewan.append(
    {"nama": "gajah sumatera", "alias": ["gajah sumatra", "gajah"],
     "kategori": "Mamalia / Sumatera", "latar": "🌳", "gambar": "",
     "clues": ["Subspesies gajah Asia yang berstatus sangat terancam punah.",
               "Bertelinga lebih kecil dibanding gajah Afrika dan berbelalai panjang.",
               "Hidup di hutan-hutan Pulau Sumatera dan sering dijuluki 'insinyur hutan'."],
     "fakta": "Gajah sumatera membantu menyebarkan biji pohon lewat kotorannya, sehingga hutan bisa tumbuh kembali."}
)

HEWAN_BY_NAMA = {h["nama"]: h for h in daftar_hewan}
TOTAL_SOAL = len(daftar_hewan)
SKOR_MAKS = TOTAL_SOAL * POIN_PER_SOAL

EMOJI_BENAR = ["🥳", "😄", "🤩", "😸", "🎉"]
EMOJI_SALAH = ["😢", "😭", "🥺", "😿"]

# Posisi Pixel Critter (bergantian tiap soal). Pojok kanan atas dikosongkan untuk tombol musik.
SUDUT_CRITTER = [
    "bottom:18px;left:12px",
    "bottom:18px;right:12px",
    "top:70px;left:8px",
    "bottom:110px;right:6px",
]

# ─────────────────────────────────────────────────────────────
# SPRITE HEWAN PIXEL ART (grid 12 x 8, menghadap kanan / depan)
# Tiap hewan punya palet sendiri. "." = transparan, "k" = mata/gelap.
# Baris yang lebih pendek otomatis diisi "." sampai lebar 12.
# ─────────────────────────────────────────────────────────────
SPRITE_HEWAN = {
    "komodo": ([
        "............",
        "........gg..",
        ".......gkgg.",
        "..ggggggggrr",
        ".gggdgdgdgg.",
        "gggggggggg..",
        "gg.gg..gg.g.",
        ".d.dd..dd.d.",
    ], {"g": "#65a30d", "d": "#3f6212", "r": "#ef4444", "k": "#111827"}),
    "orangutan": ([
        "...oooooo...",
        "..oooooooo..",
        ".ooossssooo.",
        "oooskssksooo",
        "ooosssssoooo",
        "oooosddsoooo",
        ".oooooooooo.",
        ".oo.oooo.oo.",
    ], {"o": "#ea580c", "d": "#7c2d12", "s": "#fcd9b6", "k": "#111827"}),
    "badak jawa": ([
        "..........h.",
        "....rrrrrrr.",
        "..rrrrrrkrr.",
        ".rrrrrrrrrrr",
        "rrrdrrrrrrr.",
        "rrrrrrrrrrr.",
        ".rr.rr..rr.r",
        ".dd.dd..dd.d",
    ], {"r": "#9ca3af", "d": "#4b5563", "h": "#fde68a", "k": "#111827"}),
    "harimau sumatera": ([
        "oo........oo",
        "oooooooooooo",
        "oodoooooodoo",
        "owkwoooowkwo",
        "ooooonnooooo",
        "owwwoddowwwo",
        ".oodoooodoo.",
        "..oo....oo..",
    ], {"o": "#f97316", "d": "#111827", "w": "#f8fafc", "k": "#111827", "n": "#fb7185"}),
    "anoa": ([
        "........h..h",
        ".....bbbbbbb",
        "..bbbbbbbkbb",
        ".bbbbbbbbbbb",
        "bbbbdbbbbbb.",
        "bbbbbbbbbbb.",
        ".bb.bb..bb.b",
        ".dd.dd..dd.d",
    ], {"b": "#92400e", "d": "#451a03", "h": "#fde68a", "k": "#111827"}),
    "cendrawasih": ([
        ".......yyy..",
        "......yykyya",
        "gg...yyyyy..",
        ".ggg.yyyyy..",
        "..gggeeeey..",
        "...ggeeeee..",
        "..gg..yyyy..",
        "....a..a....",
    ], {"y": "#facc15", "g": "#16a34a", "e": "#dc2626", "a": "#f97316", "k": "#111827"}),
    "babirusa": ([
        "..........w.",
        "....pppppppw",
        "..ppppppkppw",
        ".ppppppppppp",
        "ppppdpppppp.",
        "ppppppppppp.",
        ".pp.pp..pp.p",
        ".dd.dd..dd.d",
    ], {"p": "#a8a29e", "d": "#57534e", "w": "#fefce8", "k": "#111827"}),
    "maleo": ([
        ".......cc...",
        "......bbbb..",
        "......bwbbaa",
        "....bbbbbb..",
        "...bbbooobb.",
        "..bbboooobb.",
        "...bbbbbbb..",
        "....a...a...",
    ], {"b": "#1f2937", "o": "#fb923c", "c": "#fbbf24", "a": "#f59e0b", "w": "#f8fafc"}),
    "tarsius": ([
        ".ttt....ttt.",
        ".tttttttttt.",
        "ttwwwttwwwtt",
        "ttwkwttwkwtt",
        "ttwwwttwwwtt",
        ".tttttnnttt.",
        "..tttttttt..",
        "..tt.tt.tt..",
    ], {"t": "#a16207", "w": "#f8fafc", "k": "#111827", "n": "#fb7185"}),
    "jalak bali": ([
        ".www........",
        ".wwwwwww....",
        "..wwwwbkbwaa",
        "..wwwwwwww..",
        ".wwwwwwwwww.",
        "wwwwgwwwwg..",
        ".wwwwwwwww..",
        "....a..a....",
    ], {"w": "#f8fafc", "g": "#cbd5e1", "b": "#38bdf8", "a": "#facc15", "k": "#111827"}),
    "gajah sumatera": ([
        "..gggggg....",
        ".gggggggg...",
        ".ggggggkggg.",
        "ggggggggggg.",
        "ggggggggggwg",
        "gggggggggg.g",
        ".gg.gg..gg.g",
        ".dd.dd..dd.d",
    ], {"g": "#9ca3af", "d": "#6b7280", "w": "#fefce8", "k": "#111827"}),
}

# ─────────────────────────────────────────────────────────────
# PIXEL ART KARAKTER (digambar dari grid teks → SVG)
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

# Pixel Critter: hamster mungil yang bersembunyi di sudut layar
CRITTER_GRID = [
    ".oo....oo.",
    "oppo..oppo",
    "oooooooooo",
    "oookoookoo",
    "oooonnoooo",
    "oocoooocoo",
    ".oooooooo.",
    "..oo..oo..",
]
CRITTER_PALET = {"o": "#d6a56b", "p": "#f9a8d4", "k": "#111827", "n": "#fb7185", "c": "#fda4af"}


def rapat(teks: str) -> str:
    """Gabungkan HTML multi-baris jadi satu baris (aman dari aturan indentasi markdown)."""
    return "".join(baris.strip() for baris in teks.splitlines())


def grid_ke_rects(baris, palet) -> str:
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
            rects.append(f'<rect x="{x}" y="{y}" width="{j - x}" height="1" fill="{palet.get(ch, "#9ca3af")}"/>')
            x = j
    return "".join(rects)


def sprite_svg(kunci: str, lebar: int = 56, frame: int = 0, kelas: str = "", palet=None) -> str:
    baris = SPRITE_BADAN + SPRITE_KAKI[frame]
    tinggi = round(lebar * len(baris) / 12)
    return (f'<svg class="{kelas}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 {len(baris)}" '
            f'width="{lebar}" height="{tinggi}" shape-rendering="crispEdges">'
            f'{grid_ke_rects(baris, palet or KARAKTER[kunci]["palet"])}</svg>')


def hewan_svg(h: dict, lebar: int = 44, kelas: str = "") -> str:
    """Sprite pixel art SVG untuk satu hewan (pengganti emoji)."""
    grid, palet = SPRITE_HEWAN[h["nama"]]
    lbr = max(len(r) for r in grid)
    baris = [r.ljust(lbr, ".") for r in grid]
    tinggi = round(lebar * len(baris) / lbr)
    return (f'<svg class="{kelas}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {lbr} {len(baris)}" '
            f'width="{lebar}" height="{tinggi}" shape-rendering="crispEdges">'
            f'{grid_ke_rects(baris, palet)}</svg>')


def grid_svg(grid, palet, lebar: int = 32, kelas: str = "") -> str:
    lbr = max(len(r) for r in grid)
    baris = [r.ljust(lbr, ".") for r in grid]
    tinggi = round(lebar * len(baris) / lbr)
    return (f'<svg class="{kelas}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {lbr} {len(baris)}" '
            f'width="{lebar}" height="{tinggi}" shape-rendering="crispEdges">'
            f'{grid_ke_rects(baris, palet)}</svg>')


# Rintangan di jalur lemparan Pokéball
GRID_BATANG = ["..bbbbbbbb..", "rrbbbbbbbbrr", "rdbbbbbbbbdr", ".dddddddddd."]
PALET_BATANG = {"b": "#92400e", "d": "#451a03", "r": "#d6a56b"}
GRID_BATU = ["..gggg..", ".ggGGggg", "ggggggdd", "gdddddd."]
PALET_BATU = {"g": "#9ca3af", "G": "#d1d5db", "d": "#6b7280"}

# Api (ending kebakaran hutan)
GRID_API = ["...y....", "...yy...", "..yyo...", ".yyooy..", ".yooory.", "yoorrooy",
            "orrrrrro", "orrrrrro", ".orrrro.", "..oooo.."]
PALET_API = {"y": "#fde047", "o": "#fb923c", "r": "#ef4444"}

# Palet aparat & pembakar (memakai badan sprite karakter yang sama)
PAL_POLISI = {"H": "#1e3a8a", "h": "#0f1f4a", "S": "#fcd9b6", "E": "#111827", "m": "#b45309",
              "C": "#3b82f6", "c": "#1d4ed8", "W": "#fde047", "P": "#1e293b", "B": "#111827"}
PAL_PEMADAM = {"H": "#f59e0b", "h": "#b45309", "S": "#fcd9b6", "E": "#111827", "m": "#b45309",
               "C": "#ea580c", "c": "#c2410c", "W": "#fef3c7", "P": "#78350f", "B": "#1c1917"}
PAL_PEMBAKAR = {"H": "#4b5563", "h": "#111827", "S": "#fcd9b6", "E": "#111827", "m": "#b45309",
                "C": "#374151", "c": "#111827", "W": "#6b7280", "P": "#0f172a", "B": "#000000"}


PAL_PENYEL = {"H": "#a16207", "h": "#713f12", "S": "#fcd9b6", "E": "#111827", "m": "#b45309",
              "C": "#4d7c0f", "c": "#365314", "W": "#a3a3a3", "P": "#57534e", "B": "#1c1917"}


def pokeball_svg(warna: str = "#ef4444", ukuran: int = 26) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" width="{ukuran}" height="{ukuran}">'
            '<circle cx="10" cy="10" r="9" fill="#f8fafc" stroke="#0f172a" stroke-width="1.4"/>'
            f'<path d="M1 10a9 9 0 0 1 18 0z" fill="{warna}" stroke="#0f172a" stroke-width="1.4"/>'
            '<line x1="1" y1="10" x2="19" y2="10" stroke="#0f172a" stroke-width="1.6"/>'
            '<circle cx="10" cy="10" r="3" fill="#f8fafc" stroke="#0f172a" stroke-width="1.4"/></svg>')


def uri_critter() -> str:
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 8" shape-rendering="crispEdges">'
           + grid_ke_rects(CRITTER_GRID, CRITTER_PALET) + "</svg>")
    return "data:image/svg+xml;utf8," + quote(svg)


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

/* ── Layar judul (Press Start) ── */
.judul-layar { text-align: center; padding-top: 6px; }
.jl-atas { font-family: 'Press Start 2P', monospace; font-size: 0.6rem; color: #fde68a; letter-spacing: 0.14em; margin-bottom: 14px; }
.jl-logo {
    font-family: 'Press Start 2P', monospace; line-height: 1.4; font-size: clamp(1.8rem, 9.5vw, 3.1rem);
    background: linear-gradient(180deg, #fef3c7 0%, #6ee7b7 55%, #22d3ee 100%);
    -webkit-background-clip: text; background-clip: text; color: transparent !important;
    filter: drop-shadow(0 4px 0 #064e3b) drop-shadow(0 8px 14px rgba(0, 0, 0, 0.45));
}
.jl-hint { font-family: 'Press Start 2P', monospace; font-size: 0.55rem; line-height: 1.8; opacity: 0.75; margin: 4px 0 16px; }
.jl-hak { font-family: 'Press Start 2P', monospace; font-size: 0.5rem; opacity: 0.5; text-align: center; margin-top: 18px; }
.st-key-start button {
    font-family: 'Press Start 2P', monospace !important; font-size: clamp(0.8rem, 3.8vw, 1.15rem) !important;
    min-height: 3.8rem; letter-spacing: 0.08em; animation: kedip 1.1s steps(2, end) infinite;
}
.st-key-start button p { font-family: 'Press Start 2P', monospace !important; font-size: inherit !important; }
@keyframes kedip { 0%, 100% { opacity: 1; } 50% { opacity: 0.35; } }

/* ── Adegan penjelajah (pelari pixel di hutan pinus) ── */
.adegan {
    --st: clamp(11px, 3.4vw, 26px);
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
    background: #06261a; border-top: 2px solid #0f4a35; z-index: 2;
}
.adegan .tanah::after {
    content: ""; position: absolute; left: 0; right: 0; top: 4px; height: 3px; background-size: 34px 3px;
    background-image: repeating-linear-gradient(90deg, rgba(255,255,255,0.14) 0 14px, transparent 14px 34px);
    animation: garis 0.7s linear infinite;
}
.pelari { position: absolute; left: 34%; bottom: 9px; width: 52px; height: 65px; z-index: 3; animation: pantul 0.36s steps(2, end) infinite; }
.pelari svg { position: absolute; left: 0; bottom: 0; image-rendering: pixelated; }
.pelari .k1 { animation: kaki1 0.36s steps(1, end) infinite; }
.pelari .k2 { animation: kaki2 0.36s steps(1, end) infinite; }
@keyframes geser { from { background-position: 0 100%; } to { background-position: -200px 100%; } }
@keyframes garis { from { background-position: 0 0; } to { background-position: -34px 0; } }
@keyframes kaki1 { 0%, 49.9% { opacity: 1; } 50%, 100% { opacity: 0; } }
@keyframes kaki2 { 0%, 49.9% { opacity: 0; } 50%, 100% { opacity: 1; } }
@keyframes pantul { 0% { transform: translateY(0); } 50% { transform: translateY(-3px); } 100% { transform: translateY(0); } }

/* ── Hewan pengikut (companion) berbaris di belakang penjelajah ── */
.adegan .ikut { position: absolute; bottom: 13px; z-index: 3; }
.adegan .ikut svg { display: block; image-rendering: pixelated; }
.adegan .ikut-b { animation: pantul 0.36s steps(2, end) infinite; }
.adegan .ikut.baru { opacity: 0; animation: ikutMasuk 0.6s ease 2.6s forwards; }
@keyframes ikutMasuk { from { opacity: 0; transform: translateX(34px) scale(0.6); } to { opacity: 1; transform: none; } }

/* ── Adegan layar judul: penjelajah mengejar hewan ── */
.adegan.kejar { height: 150px; margin: 14px 0 10px; }
.adegan.kejar .pelari { left: 11%; }
.adegan .buru { position: absolute; bottom: 14px; z-index: 3; animation: pantul 0.3s steps(2, end) infinite; }
.adegan .buru svg { display: block; image-rendering: pixelated; }
.adegan .buru-b { animation: kejarX 1.8s ease-in-out infinite alternate; }
@keyframes kejarX { from { transform: translateX(-8px); } to { transform: translateX(12px); } }
.adegan .seru {
    position: absolute; left: 27%; top: 26px; z-index: 5; font-family: 'Press Start 2P', monospace; font-size: 1rem;
    color: #fde68a; animation: kedip 0.6s steps(2, end) infinite;
}

/* ── Menangkap hewan: hewan + bola lempar + kilau ── */
.adegan .hewan { position: absolute; left: 72%; bottom: 14px; line-height: 1; z-index: 3; transform-origin: 50% 100%; }
.adegan .hewan span { display: inline-block; animation: napas 1.2s ease-in-out infinite; }
.adegan .hewan svg { display: block; image-rendering: pixelated; }
.adegan .lempar { position: absolute; left: 43%; bottom: 36px; opacity: 0; z-index: 4; }
.adegan .lr svg { width: 20px; height: 20px; display: block; }
.adegan .kilau { position: absolute; left: 73%; bottom: 24px; font-size: 1.4rem; opacity: 0; z-index: 5; }
.adegan .tag {
    position: absolute; left: 50%; top: 10px; transform: translateX(-50%); z-index: 5; white-space: nowrap;
    padding: 3px 12px; border-radius: 999px; font-size: 0.78rem; font-weight: 600; opacity: 0;
    background: rgba(10, 40, 30, 0.75); border: 1px solid rgba(110, 231, 183, 0.5); color: #a7f3d0;
    animation: tagMuncul 0.5s ease 2s forwards;
}
.adegan .tag.oren { border-color: rgba(253, 186, 116, 0.6); color: #fdba74; animation-delay: 0.8s; }
@keyframes napas { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-4px); } }
@keyframes tagMuncul { from { opacity: 0; } to { opacity: 1; } }

/* mode loop (sedang menebak): tangkap berulang tiap 6 detik */
.adegan.loop .hewan { animation: hewanLoop 6s ease-in-out infinite; }
.adegan.loop .lempar { animation: bolaX 6s linear infinite; }
.adegan.loop .ly { animation: bolaY 6s infinite; }
.adegan.loop .lr { animation: bolaR 6s linear infinite; }
.adegan.loop .kilau { display: none; }
.adegan.loop .miss { animation: missLoop 6s infinite; }
.adegan.loop .rintangan.log { animation: logGoyang 6s infinite; }
@keyframes bolaX { 0%, 34% { left: 43%; opacity: 0; } 35% { left: 43%; opacity: 1; } 43% { left: 52%; opacity: 1; } 48% { left: 46%; opacity: 1; } 54% { left: 41%; opacity: 1; } 58%, 100% { left: 41%; opacity: 0; } }
@keyframes bolaY { 0%, 35% { transform: translateY(0); animation-timing-function: ease-out; } 40% { transform: translateY(-30px); animation-timing-function: ease-in; } 43.5% { transform: translateY(6px); animation-timing-function: ease-out; } 49% { transform: translateY(-16px); animation-timing-function: ease-in; } 54%, 100% { transform: translateY(14px); } }
@keyframes bolaR { 0%, 35% { transform: rotate(0deg); } 43% { transform: rotate(360deg); } 58%, 100% { transform: rotate(-200deg); } }
@keyframes hewanLoop { 0%, 40% { transform: translateY(0); } 43% { transform: translateY(-16px); } 47% { transform: translateY(0); } 50% { transform: translateY(-8px); } 54%, 100% { transform: translateY(0); } }
@keyframes missLoop { 0%, 42% { opacity: 0; } 44%, 56% { opacity: 1; } 60%, 100% { opacity: 0; } }
@keyframes logGoyang { 0%, 42% { transform: none; } 44% { transform: translateX(3px); } 46% { transform: translateX(-2px); } 48%, 100% { transform: none; } }


/* mode tangkap (jawaban benar): sekali jalan, hewan tertangkap lalu ikut berbaris */
.adegan.tangkap .hewan { animation: hewanOnce 3.2s ease forwards; }
.adegan.tangkap .lempar { animation: bolaXo 3.2s linear forwards; }
.adegan.tangkap .ly { animation: bolaYo 3.2s forwards; }
.adegan.tangkap .lr { animation: bolaRo 3.2s linear forwards; }
.adegan.tangkap .kilau { animation: kilauOnce 3.2s ease forwards; }
.adegan.tangkap .pelari { animation: none; }
.adegan.tangkap .pelari .k1 { display: none; }
.adegan.tangkap .pelari .k2 { animation: none; opacity: 1; }
.adegan.tangkap .lapis, .adegan.tangkap .tanah::after { animation-play-state: paused; }
@keyframes bolaXo { 0% { left: 43%; opacity: 1; } 25%, 100% { left: 73%; opacity: 1; } }
@keyframes bolaYo { 0% { transform: translateY(0); animation-timing-function: ease-out; } 12% { transform: translateY(-62px); animation-timing-function: ease-in; } 25%, 100% { transform: translateY(12px); } }
@keyframes bolaRo { 0% { transform: rotate(0deg); } 25% { transform: rotate(720deg); } 32% { transform: rotate(698deg); } 40% { transform: rotate(740deg); } 48% { transform: rotate(706deg); } 56% { transform: rotate(730deg); } 62%, 100% { transform: rotate(720deg); } }
@keyframes hewanOnce { 0%, 22% { opacity: 1; transform: scale(1); } 27%, 100% { opacity: 0; transform: scale(0.1); } }
@keyframes kilauOnce { 0%, 60% { opacity: 0; transform: scale(0.4); } 68% { opacity: 1; transform: scale(1.3); } 85% { opacity: 0.9; transform: scale(1); } 100% { opacity: 0; transform: scale(1.6); } }

/* mode kabur (menyerah): hewan lari */
.adegan.kabur .hewan { animation: kabur 1.8s ease-in forwards; }
.adegan.kabur .lempar, .adegan.kabur .kilau { display: none; }
@keyframes kabur { 0% { left: 72%; opacity: 1; } 100% { left: 115%; opacity: 1; } }

/* ── Scene ending: pelepasan satwa + foto bersama ── */
.adegan.panggung { height: 262px; }
.panggung .lapis { animation: none !important; height: 110px; background-size: 275px 110px; }
.panggung .baris { position: absolute; left: 0; right: 0; display: flex; justify-content: center; align-items: flex-end; gap: 4px; z-index: 3; }
.panggung .belakang { bottom: 98px; }
.panggung .depan { bottom: 26px; }
.panggung .slot { position: relative; width: 40px; height: 40px; display: flex; align-items: flex-end; justify-content: center; }
.panggung .slot.kar { width: 64px; height: 76px; }
.panggung .slot.kar svg { image-rendering: pixelated; }
.panggung .sat { transform-origin: 50% 100%; animation: lepas 0.9s ease both; line-height: 0; }
.panggung .sat svg { width: 36px; height: auto; display: block; image-rendering: pixelated; }
.panggung .belakang .sat svg { width: 30px; }
.panggung .bola-s { position: absolute; bottom: 0; left: 50%; margin-left: -10px; opacity: 0; animation: bolaBuka 1s ease both; }
.panggung .bola-s svg { display: block; }
.panggung .cap {
    position: absolute; top: 10px; left: 0; right: 0; text-align: center; z-index: 6;
    font-weight: 600; font-size: 0.85rem; color: #e8f3ee; text-shadow: 0 2px 8px rgba(0, 0, 0, 0.6);
}
.panggung .cap1 { opacity: 0; animation: capHilang 0.4s ease both; }
.panggung .cap2 { opacity: 1; animation: capMuncul 0.6s ease both; }
.panggung .tq {
    position: absolute; top: 40px; left: 0; right: 0; text-align: center; z-index: 6; opacity: 0;
    font-family: 'Press Start 2P', monospace; font-size: clamp(0.5rem, 2.8vw, 0.8rem); color: #fde68a;
    text-shadow: 0 2px 0 #7c2d12, 0 4px 10px rgba(0, 0, 0, 0.6); animation: capMuncul 0.6s ease both;
}
.panggung .bingkai {
    position: absolute; inset: 8px; border: 3px solid rgba(253, 230, 138, 0.85); border-radius: 14px; z-index: 5;
    pointer-events: none; box-shadow: inset 0 0 30px rgba(0, 0, 0, 0.35); animation: capMuncul 0.6s ease both;
}
.panggung .flash-foto { position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 7; pointer-events: none; animation: kilatFoto 0.8s ease both; }
@keyframes lepas { 0%, 35% { opacity: 0; transform: scale(0.1) translateY(8px); } 70% { opacity: 1; transform: scale(1.3); } 100% { opacity: 1; transform: scale(1); } }
@keyframes bolaBuka { 0% { opacity: 1; transform: rotate(0) scale(1); } 20% { transform: rotate(-20deg); } 40% { transform: rotate(20deg); } 55% { opacity: 1; transform: rotate(0) scale(1.2); } 100% { opacity: 0; transform: scale(1.9); } }
@keyframes capHilang { from { opacity: 1; } to { opacity: 0; } }
@keyframes capMuncul { from { opacity: 0; } to { opacity: 1; } }
@keyframes kilatFoto { 0% { opacity: 0; } 12% { opacity: 0.95; } 100% { opacity: 0; } }

/* ── Rintangan di jalur lemparan ── */
.adegan .rintangan { position: absolute; bottom: 13px; z-index: 3; }
.adegan .rintangan svg { display: block; image-rendering: pixelated; }
.adegan .miss {
    position: absolute; left: 41%; bottom: 66px; z-index: 6; opacity: 0; white-space: nowrap;
    font-family: 'Press Start 2P', monospace; font-size: 0.5rem; color: #fca5a5; text-shadow: 2px 2px 0 #000;
}

/* ── Karakter bisa diklik: lompat + gelembung dialog pixel ── */
.adegan .pelari { cursor: pointer; -webkit-tap-highlight-color: transparent; }
.adegan .pelari.lompat { animation: lompatPelari 0.6s ease-out !important; }
.adegan .pelari.lompat .k1 { animation: none !important; opacity: 0; display: block; }
.adegan .pelari.lompat .k2 { animation: none !important; opacity: 1; }
@keyframes lompatPelari { 0% { transform: translateY(0); } 45% { transform: translateY(-38px); } 100% { transform: translateY(0); } }
.adegan .gelembung {
    position: absolute; bottom: 88px; z-index: 8; padding: 6px 9px; background: #ffffff; color: #000000;
    border: 3px solid #000; box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.45); white-space: nowrap;
    font-family: 'Press Start 2P', monospace; font-size: 0.5rem; line-height: 1.6; animation: gelPop 0.25s steps(3, end) both;
}
.adegan .gelembung::after { content: ""; position: absolute; left: 22px; bottom: -13px; border: 6px solid transparent; border-top: 8px solid #000; }
.adegan .piksel-emo {
    position: absolute; bottom: 80px; z-index: 8; font-family: 'Press Start 2P', monospace; font-size: 0.9rem;
    color: #fde047; text-shadow: 2px 2px 0 #000; animation: emoNaik 1.2s steps(6, end) forwards;
}
@keyframes gelPop { from { transform: scale(0.4); opacity: 0; } to { transform: scale(1); opacity: 1; } }
@keyframes emoNaik { from { transform: translateY(0); opacity: 1; } to { transform: translateY(-34px); opacity: 0; } }

/* ── Ending bagian 1: pembakar hutan & penyelundup satwa ditangkap sang penjelajah ── */
.adegan.api { height: 190px; animation: apiBuka 0.6s ease 0.1s both, apiTutup 0.7s ease 12.4s forwards; }
.api .lapis { animation: none !important; height: 110px; background-size: 275px 110px; }
.api .merah {
    position: absolute; inset: 0; z-index: 1; pointer-events: none; opacity: 0;
    background: radial-gradient(circle at 62% 95%, rgba(239, 68, 68, 0.85), transparent 70%);
    animation: merahMaster 12s linear 0.4s both;
}
.api .cap {
    position: absolute; top: 10px; left: 0; right: 0; padding: 0 8px; text-align: center; z-index: 6; opacity: 0;
    font-weight: 600; font-size: 0.85rem; color: #fff; text-shadow: 0 2px 8px rgba(0, 0, 0, 0.7);
}
.api .capA { animation: capA 12s linear 0.4s both; }
.api .capB { animation: capB 12s linear 0.4s both; }
.api .capC { opacity: 1; animation: capC 12s linear 0.4s both; }
.api .api-api { position: absolute; bottom: 13px; z-index: 3; opacity: 0; transform-origin: 50% 100%; animation: flameMaster 12s linear 0.4s both; }
.api .api-b { transform-origin: 50% 100%; animation: apiKedip 0.35s steps(2, end) infinite alternate; }
.api .api-b svg, .api .obor svg, .api .sangkar svg, .api .sb-b svg { display: block; image-rendering: pixelated; }
.api .org, .api .hero { position: absolute; bottom: 9px; width: 52px; height: 65px; z-index: 4; }
.api .org-b { position: relative; width: 52px; height: 65px; animation: pantul 0.36s steps(2, end) infinite; }
.api .org-b svg { position: absolute; left: 0; bottom: 0; image-rendering: pixelated; }
.api .org-b .k1 { animation: kaki1 0.36s steps(1, end) infinite; }
.api .org-b .k2 { animation: kaki2 0.36s steps(1, end) infinite; }
.api .flip { transform: scaleX(-1); }
.api .pembakar { left: 42%; animation: pbX 12s linear 0.4s both; }
.api .penyel { left: 18%; animation: pyX 12s linear 0.4s both; }
.api .hero { left: 58%; animation: heroX 12s linear 0.4s both, heroHop 12s linear 0.4s both; }
.api .obor { position: absolute; left: -12px; bottom: 26px; opacity: 0; animation: oborJatuh 12s linear 0.4s both; }
.api .obor .gagang { display: block; width: 4px; height: 14px; margin: 0 auto; background: #92400e; }
.api .sangkar {
    position: absolute; left: 46px; bottom: 6px; width: 32px; height: 28px; border: 2px solid #d1d5db; border-radius: 4px 4px 0 0;
    background: repeating-linear-gradient(90deg, transparent 0 5px, rgba(209, 213, 219, 0.85) 5px 7px);
    display: flex; align-items: flex-end; justify-content: center;
}
.api .sangkar .isi { animation: isiHilang 12s linear 0.4s both; opacity: 0; }
.api .satwa-bebas { position: absolute; bottom: 14px; left: 49%; z-index: 3; animation: bebas 12s linear 0.4s both; }
.api .sb-b { animation: pantul 0.36s steps(2, end) infinite; }
.api .balon {
    position: absolute; left: -10px; bottom: 74px; padding: 5px 8px; background: #fff; color: #000; border: 3px solid #000;
    white-space: nowrap; font-family: 'Press Start 2P', monospace; font-size: 0.5rem; opacity: 0; animation: ampun2 12s linear 0.4s both;
}
.api .balon.bh { left: 4px; animation: balonHero 12s linear 0.4s both; }
.api .tanda {
    position: absolute; left: 20px; bottom: 74px; font-family: 'Press Start 2P', monospace; font-size: 1rem; color: #fde047;
    text-shadow: 2px 2px 0 #000; opacity: 0; animation: tanda 12s linear 0.4s both;
}
@keyframes apiBuka { from { height: 0; opacity: 0; margin-bottom: 0; } to { height: 190px; opacity: 1; margin-bottom: 16px; } }
@keyframes apiTutup { from { height: 190px; opacity: 1; margin-bottom: 16px; } to { height: 0; opacity: 0; margin-bottom: 0; } }
@keyframes panggungBuka { from { height: 0; opacity: 0; margin-bottom: 0; } to { height: 262px; opacity: 1; margin-bottom: 16px; } }
@keyframes apiKedip { from { transform: scaleY(1); } to { transform: scaleY(0.86) scaleX(1.06); } }
@keyframes flameMaster { 0%, 15% { opacity: 0; transform: scaleY(0); } 19%, 58% { opacity: 1; transform: scaleY(1); } 66%, 100% { opacity: 0; transform: scaleY(0); } }
@keyframes merahMaster { 0%, 13% { opacity: 0; } 18%, 58% { opacity: 0.4; } 66%, 100% { opacity: 0; } }
@keyframes capA { 0% { opacity: 0; } 1%, 17% { opacity: 1; } 19%, 100% { opacity: 0; } }
@keyframes capB { 0%, 20% { opacity: 0; } 22%, 48% { opacity: 1; } 50%, 100% { opacity: 0; } }
@keyframes capC { 0%, 50% { opacity: 0; } 53%, 100% { opacity: 1; } }
@keyframes pbX { 0% { left: -22%; } 14%, 100% { left: 42%; } }
@keyframes pyX { 0% { left: -40%; } 14%, 100% { left: 18%; } }
@keyframes heroX { 0%, 24% { left: 84%; } 52%, 100% { left: 58%; } }
@keyframes heroHop { 0%, 22% { transform: translateY(0); } 25% { transform: translateY(-22px); } 28%, 100% { transform: translateY(0); } }
@keyframes tanda { 0%, 20% { opacity: 0; } 22%, 34% { opacity: 1; } 36%, 100% { opacity: 0; } }
@keyframes balonHero { 0%, 36% { opacity: 0; } 38%, 52% { opacity: 1; } 54%, 100% { opacity: 0; } }
@keyframes ampun2 { 0%, 53% { opacity: 0; } 55%, 75% { opacity: 1; } 77%, 100% { opacity: 0; } }
@keyframes oborJatuh { 0%, 50% { opacity: 1; transform: none; } 58%, 100% { opacity: 0; transform: translateY(34px) rotate(80deg); } }
@keyframes isiHilang { 0%, 62% { opacity: 1; } 64%, 100% { opacity: 0; } }
@keyframes bebas { 0%, 62% { left: calc(18% + 48px); opacity: 0; } 63% { left: calc(18% + 48px); opacity: 1; } 76%, 100% { left: 49%; opacity: 1; } }

/* ── Nyawa (hati) + vignette layar sekarat ── */
.nyawa { font-size: 0.95rem; letter-spacing: 3px; line-height: 1.3; margin-top: 2px; }
.element-container:has(.vignette), [data-testid="stElementContainer"]:has(.vignette) { position: absolute; height: 0; width: 0; overflow: visible; }
.vignette { position: fixed; inset: 0; z-index: 9980; pointer-events: none; }
.vignette.v1 { background: radial-gradient(ellipse at center, transparent 62%, rgba(127, 0, 0, 0.38) 100%); }
.vignette.v2 { background: radial-gradient(ellipse at center, transparent 45%, rgba(150, 0, 0, 0.55) 82%, rgba(25, 0, 0, 0.8) 100%); animation: denyutMerah 2.4s ease-in-out infinite; }
.vignette.v3 { background: radial-gradient(ellipse at center, transparent 25%, rgba(170, 0, 0, 0.7) 65%, rgba(0, 0, 0, 0.93) 100%); animation: denyutMerah 1.3s ease-in-out infinite; }
.kena-flash { position: fixed; inset: 0; z-index: 9985; pointer-events: none; background: rgba(220, 0, 0, 0.45); animation: kenaFlash 0.7s ease-out forwards; }
@keyframes denyutMerah { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; } }
@keyframes kenaFlash { from { opacity: 1; } to { opacity: 0; } }
@media (prefers-reduced-motion: reduce) { .kena-flash { display: none; } }

/* ── Kotak notifikasi & peringatan: HITAM PEKAT + teks PUTIH (termasuk toast Pixel Critter) ── */
[data-testid="stToast"], [data-testid="stToast"] > div {
    background: #000000 !important; border: 1px solid rgba(253, 230, 138, 0.8) !important; border-radius: 12px !important;
}
[data-testid="stToast"], [data-testid="stToast"] * { color: #ffffff !important; font-weight: 600; }
[data-testid="stAlert"] { background: #000000 !important; border: 1px solid rgba(253, 230, 138, 0.7) !important; border-radius: 12px; }
[data-testid="stAlert"], [data-testid="stAlert"] * { color: #ffffff !important; }
.stTextInput textarea, .stTextArea textarea, .stNumberInput input {
    background: #000000 !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important;
}

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
    display: block; margin: 10px 0 4px; line-height: 0;
    animation: melayang 3.6s ease-in-out infinite; filter: drop-shadow(0 10px 16px rgba(0, 0, 0, 0.45));
}
.kartu-hewan .ikon-besar svg { display: block; margin: 0 auto; width: clamp(130px, 44vw, 200px); height: auto; image-rendering: pixelated; }
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
.reaksi span { display: inline-block; vertical-align: middle; animation: loncat 0.9s ease-in-out infinite; }
.reaksi span + span { animation-delay: 0.18s; margin-left: 10px; }
.reaksi svg { display: block; width: 68px; height: auto; image-rendering: pixelated; }
.mini-hewan { display: inline-block; vertical-align: middle; margin-right: 6px; line-height: 0; }
.mini-hewan svg { width: 30px; height: auto; image-rendering: pixelated; }
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

/* Input: kotak HITAM PEKAT + teks PUTIH bersih (kontras maksimum). Pembungkus baseweb ikut dihitamkan. */
[data-baseweb="input"], [data-baseweb="base-input"], .stTextInput > div > div {
    background: #000000 !important; background-color: #000000 !important;
}
[data-baseweb="input"] {
    border: 1px solid rgba(167, 243, 208, 0.65) !important; border-radius: 14px !important;
}
[data-baseweb="input"]:focus-within { border-color: #6ee7b7 !important; box-shadow: 0 0 0 3px rgba(110, 231, 183, 0.30) !important; }
.stTextInput input {
    min-height: 3rem; font-size: 1.05rem; background: #000000 !important; background-color: #000000 !important;
    color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; caret-color: #6ee7b7;
}
.stTextInput input::placeholder { color: #a8bdb4 !important; -webkit-text-fill-color: #a8bdb4 !important; opacity: 1; }
.stTextInput input:-webkit-autofill, .stTextInput input:-webkit-autofill:hover, .stTextInput input:-webkit-autofill:focus {
    -webkit-box-shadow: 0 0 0 1000px #000000 inset !important; -webkit-text-fill-color: #ffffff !important;
    caret-color: #ffffff; transition: background-color 9999s ease-in-out 0s;
}
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

/* ── Easter egg 1: Pixel Critter (tombol Streamlit key="critter" disulap jadi hamster pixel di sudut) ── */
.st-key-critter { position: fixed; z-index: 9990; width: auto !important; margin: 0 !important; }
.st-key-critter button, .st-key-critter button:hover, .st-key-critter button:active, .st-key-critter button:focus {
    width: 46px; height: 38px; min-height: 0 !important; padding: 0 !important; border: none !important;
    box-shadow: none !important; outline: none !important; font-size: 0 !important; color: transparent !important;
    background: url("__CRITTER__") center / contain no-repeat !important; image-rendering: pixelated;
    opacity: 0.6; animation: ngintip 3s ease-in-out infinite; transition: opacity 0.2s ease;
}
.st-key-critter button:hover { opacity: 1; }
.st-key-critter button p { font-size: 0 !important; }
@keyframes ngintip { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-4px); } }

/* ── Easter egg 2: Secret Disco (kelas rf-disco dipasang di <html> oleh JS) ── */
.judul-museum { cursor: pointer; user-select: none; -webkit-user-select: none; touch-action: manipulation; margin: 4px 0 2px; }
html.rf-disco [data-testid="stAppViewContainer"] { position: relative; z-index: 1; }
html.rf-disco .stApp::before {
    content: ""; position: fixed; inset: 0; z-index: 0; pointer-events: none; opacity: 0.4; mix-blend-mode: screen;
    background: linear-gradient(120deg, #ff2bd6, #22d3ee, #fde047, #a3e635, #ff2bd6); background-size: 300% 300%;
    animation: geserLatar 6s linear infinite, putarHue 8s linear infinite;
}
html.rf-disco .stApp::after {
    content: ""; position: fixed; left: 0; right: 0; bottom: 0; height: 24vh; z-index: 0; pointer-events: none; opacity: 0.4;
    background-image:
        linear-gradient(45deg, #ff2bd6 25%, transparent 25%, transparent 75%, #ff2bd6 75%),
        linear-gradient(45deg, #22d3ee 25%, transparent 25%, transparent 75%, #22d3ee 75%);
    background-size: 60px 60px; background-position: 0 0, 30px 30px;
    -webkit-mask-image: linear-gradient(to top, #000, transparent); mask-image: linear-gradient(to top, #000, transparent);
    animation: lantaiGeser 1.2s linear infinite, putarHue 8s linear infinite;
}
html.rf-disco body::before {
    content: "🪩"; position: fixed; top: 2px; left: 50%; margin-left: -22px; font-size: 44px; line-height: 1;
    z-index: 99990; pointer-events: none; transform-origin: 50% 0; animation: ayun 2.4s ease-in-out infinite;
    filter: drop-shadow(0 0 12px rgba(255, 255, 255, 0.6));
}
html.rf-disco .glass, html.rf-disco [data-testid="stExpander"] { animation: neon 1.6s linear infinite; }
html.rf-disco .judul-museum {
    background: linear-gradient(90deg, #ff2bd6, #fde047, #22d3ee, #a3e635, #ff2bd6); background-size: 300% 100%;
    -webkit-background-clip: text; background-clip: text; color: transparent !important; animation: geserWarna 2s linear infinite;
}
@keyframes geserLatar { from { background-position: 0% 50%; } to { background-position: 300% 50%; } }
@keyframes geserWarna { from { background-position: 0% 0; } to { background-position: 300% 0; } }
@keyframes putarHue { from { filter: hue-rotate(0deg); } to { filter: hue-rotate(360deg); } }
@keyframes lantaiGeser { from { background-position: 0 0, 30px 30px; } to { background-position: 60px 0, 90px 30px; } }
@keyframes ayun { 0%, 100% { transform: rotate(-14deg); } 50% { transform: rotate(14deg); } }
@keyframes neon {
    0% { border-color: #ff2bd6; box-shadow: 0 0 18px rgba(255, 43, 214, 0.55); }
    25% { border-color: #22d3ee; box-shadow: 0 0 18px rgba(34, 211, 238, 0.55); }
    50% { border-color: #fde047; box-shadow: 0 0 18px rgba(253, 224, 71, 0.55); }
    75% { border-color: #a3e635; box-shadow: 0 0 18px rgba(163, 230, 53, 0.55); }
    100% { border-color: #ff2bd6; box-shadow: 0 0 18px rgba(255, 43, 214, 0.55); }
}

iframe[height="0"] { display: none; }

@media (max-width: 640px) {
    .block-container { padding-left: 0.9rem; padding-right: 0.9rem; }
    .glass { padding: 16px; border-radius: 18px; }
}
@media (prefers-reduced-motion: reduce) {
    .ikon-besar, .ikon-latar, .animasi, .clue, .pelari, .pelari svg, .lapis, .tanah::after,
    .reaksi span, .salah-baris .emo, .hasil-salah, .transisi *, .adegan *, .panggung *,
    .ikut, .ikut-b, .buru, .buru-b, .st-key-start button, .vignette,
    .st-key-critter button, html.rf-disco .stApp::before, html.rf-disco .stApp::after,
    html.rf-disco body::before, html.rf-disco .glass, html.rf-disco .judul-museum { animation: none !important; }
    .adegan .ikut.baru { opacity: 1; }
}
"""
CSS = (CSS.replace("__POHON_JAUH__", POHON_JAUH)
          .replace("__POHON_DEKAT__", POHON_DEKAT)
          .replace("__CRITTER__", uri_critter()))
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# AUDIO + INTERAKSI JS
# Mesin audio dipasang SEKALI di halaman induk (bukan di iframe), jadi musik dan
# timer-nya tidak ikut mati saat Streamlit me-rerun / iframe diganti.
# Isinya: efek suara, musik latar tegang, tombol musik, pemicu Secret Disco,
# unlock audio pada gesture pertama, dan tombol Enter untuk PRESS START.
# ─────────────────────────────────────────────────────────────
VERSI_ENGINE = "6"

ENGINE_JS = """
(function() {
  var W = window, D = document;
  W.__rfEngine = "__VERSI__";
  if (typeof W.__rfNext !== 'number') W.__rfNext = 0;
  if (typeof W.__rfStep !== 'number') W.__rfStep = 0;

  function ctx() {
    var AC = W.AudioContext || W.webkitAudioContext;
    if (!AC) return null;
    if (!W.__rfCtx) W.__rfCtx = new AC();
    if (W.__rfCtx.state === 'suspended') { try { W.__rfCtx.resume(); } catch (e) {} }
    return W.__rfCtx;
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
  function kick(t) {
    var c = ctx(); if (!c) return;
    var o = c.createOscillator(), g = c.createGain();
    o.type = 'sine';
    o.frequency.setValueAtTime(170, t);
    o.frequency.exponentialRampToValueAtTime(48, t + 0.12);
    g.gain.setValueAtTime(0.22, t);
    g.gain.exponentialRampToValueAtTime(0.0001, t + 0.18);
    o.connect(g); g.connect(c.destination);
    o.start(t); o.stop(t + 0.2);
  }

  // ── Toast kecil (untuk mode disko)
  W.__rfToast = function(teks) {
    var d = D.createElement('div');
    d.textContent = teks;
    d.style.cssText = 'position:fixed;left:50%;top:64px;transform:translateX(-50%);z-index:100000;padding:8px 16px;' +
      'border-radius:999px;background:#000;color:#fff;font:600 14px Poppins,sans-serif;' +
      'border:1px solid rgba(255,255,255,.3);box-shadow:0 6px 20px rgba(0,0,0,.4);white-space:nowrap;';
    D.body.appendChild(d);
    W.setTimeout(function() {
      d.style.transition = 'opacity .4s'; d.style.opacity = '0';
      W.setTimeout(function() { if (d.parentNode) d.parentNode.removeChild(d); }, 450);
    }, 2400);
  };

  // ── Efek suara
  W.__rfSfx = function(jenis) {
    if (jenis === 'klik')    { nada(660, 0, 0.08, 'triangle', 0.10); }
    if (jenis === 'lompat')  { nada(420, 0, 0.08, 'square', 0.08); nada(840, 0.07, 0.12, 'square', 0.08); }
    if (jenis === 'luka')    { nada(196, 0, 0.15, 'sawtooth', 0.10); nada(147, 0.14, 0.15, 'sawtooth', 0.10); nada(98, 0.28, 0.35, 'sawtooth', 0.12); }
    if (jenis === 'fanfare') { [523, 659, 784, 1047, 784, 1047, 1319].forEach(function(f, i) { nada(f, i * 0.12, 0.3, 'triangle', 0.18); }); }
    if (jenis === 'sirine')  { for (var q = 0; q < 4; q++) { nada(660, q * 0.5, 0.24, 'square', 0.05); nada(880, q * 0.5 + 0.25, 0.24, 'square', 0.05); } }
    if (jenis === 'benar')   { [523, 659, 784, 1047].forEach(function(f, i) { nada(f, i * 0.09, 0.22, 'triangle', 0.18); }); }
    if (jenis === 'salah')   { nada(220, 0, 0.18, 'sawtooth', 0.10); nada(150, 0.16, 0.3, 'sawtooth', 0.10); }
    if (jenis === 'lewat')   { nada(440, 0, 0.12, 'sine', 0.12); nada(330, 0.12, 0.2, 'sine', 0.12); }
    if (jenis === 'mulai')   { [392, 523, 659, 784, 1047].forEach(function(f, i) { nada(f, i * 0.11, 0.26, 'triangle', 0.18); }); }
    if (jenis === 'bonus')   { [880, 1175, 1568].forEach(function(f, i) { nada(f, i * 0.08, 0.16, 'square', 0.09); }); }
    if (jenis === 'disko')   { [523, 659, 784, 659, 784, 1047].forEach(function(f, i) { nada(f, i * 0.08, 0.14, 'sawtooth', 0.08); }); }
    if (jenis === 'foto')    { nada(1800, 0, 0.04, 'square', 0.10); nada(900, 0.06, 0.07, 'square', 0.08); }
    if (jenis === 'selesai') {
      W.setTimeout(function() { W.__rfSfx('sirine'); }, 2800);
      W.setTimeout(function() { W.__rfSfx('benar'); }, 7600);
      W.setTimeout(function() { W.__rfSfx('fanfare'); }, 12700);
      W.setTimeout(function() { W.__rfSfx('foto'); }, 18700);
    }
  };

  // ── Musik latar: mode tegang (default) dan mode disko
  var AKOR = [
    {b: 55.00, n: [220.00, 261.63, 329.63]},
    {b: 43.65, n: [174.61, 220.00, 261.63]},
    {b: 49.00, n: [196.00, 246.94, 293.66]},
    {b: 41.20, n: [164.81, 207.65, 246.94]}
  ];
  var BASD = [1,0,1,0,0,1,0,2,1,0,1,0,0,2,0,1];
  function langkahTegang(s, t) {
    var ak = AKOR[Math.floor(s / 8) % 4];
    nadaAt(s % 2 === 0 ? ak.b : ak.b * 2, t, 0.12, 'sawtooth', s % 4 === 0 ? 0.060 : 0.038);
    nadaAt(ak.n[s % 3], t, 0.09, 'square', 0.022);
    if (s % 8 === 7) nadaAt(ak.n[2] * 2, t, 0.10, 'square', 0.028);
  }
  function langkahDisko(s, t) {
    var k = s % 16, ak = AKOR[Math.floor(s / 16) % 4];
    if (k % 4 === 0) kick(t);
    if (k % 2 === 1) nadaAt(7000, t, 0.03, 'square', 0.010);
    if (BASD[k]) nadaAt(ak.b * (BASD[k] === 1 ? 2 : 3), t, 0.10, 'sawtooth', 0.05);
    if (k === 2 || k === 6 || k === 10 || k === 14) {
      ak.n.forEach(function(f) { nadaAt(f, t, 0.09, 'square', 0.012); });
    }
  }
  W.__rfTick = function() {
    if (!W.__rfMusikOn) return;
    var c = ctx(); if (!c) return;
    // jaga penjadwalan tetap sehat: kalau tertinggal atau melompat terlalu jauh, sinkronkan ulang
    if (W.__rfNext < c.currentTime || W.__rfNext > c.currentTime + 2) W.__rfNext = c.currentTime + 0.05;
    while (W.__rfNext < c.currentTime + 0.8) {
      var s = W.__rfStep, t = W.__rfNext;
      if (W.__rfDiscoOn) { langkahDisko(s, t); W.__rfNext += 0.125; }
      else               { langkahTegang(s, t); W.__rfNext += 0.14; }
      W.__rfStep++;
    }
  };
  if (W.__rfTimer) W.clearInterval(W.__rfTimer);
  W.__rfTimer = W.setInterval(function() { if (W.__rfTick) W.__rfTick(); }, 100);

  // ── Tombol musik minimalis (pojok kanan atas)
  function labelTombol() {
    var b = D.getElementById('rf-musik');
    if (b) { b.textContent = W.__rfMusikOn ? '🔊' : '🔇'; b.style.opacity = W.__rfMusikOn ? '1' : '0.7'; }
  }
  W.__rfToggleMusik = function() {
    var c = ctx(); if (!c) return;
    W.__rfMusikOn = !W.__rfMusikOn;
    if (W.__rfMusikOn) { W.__rfNext = c.currentTime + 0.05; W.__rfStep = 0; }
    labelTombol();
  };
  if (!D.getElementById('rf-musik')) {
    var b = D.createElement('button');
    b.id = 'rf-musik'; b.type = 'button'; b.setAttribute('aria-label', 'Musik on/off');
    b.style.cssText = 'position:fixed;top:12px;right:12px;z-index:99999;width:40px;height:40px;border-radius:50%;' +
      'border:1px solid rgba(255,255,255,.25);background:rgba(10,40,30,.55);color:#e8f3ee;font-size:18px;cursor:pointer;' +
      'backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);display:flex;align-items:center;justify-content:center;padding:0;';
    b.addEventListener('click', function() { if (W.__rfToggleMusik) W.__rfToggleMusik(); });
    D.body.appendChild(b);
  }
  labelTombol();

  // ── Easter egg: Secret Disco
  W.__rfDisco = function(on) {
    D.documentElement.classList.toggle('rf-disco', on);
    W.__rfDiscoOn = on;
    if (W.__rfMusikOn) { var c = ctx(); if (c) { W.__rfNext = c.currentTime + 0.05; W.__rfStep = 0; } }
    W.__rfSfx(on ? 'disko' : 'klik');
    W.__rfToast(on ? '🪩 Mode Disko ON! Klik judul 3× lagi untuk mematikan' : 'Mode Disko OFF');
  };

  // ── Karakter pixel bisa diklik: lompat + dialog
  var DIALOG = ['Aduh susahnya...', 'Hmm, hewan apa ya?', 'Buka petunjuk dong!', 'Aku pasti bisa!',
                'Perutku lapar...', 'Ayo semangat!', 'Kakiku pegal...', 'Hampir ketemu!', 'La la la ~'];
  var DIALOG_SAKIT = ['Aduh sakit...', 'Nyawaku tinggal sedikit!', 'Jangan salah lagi!', 'Pusing...', 'Tolong dong...'];
  var PIKSEL = ['♥', '★', '?!', '♪', '!!', '✦'];
  W.__rfPelari = function(pel) {
    var adg = pel.closest('.adegan'); if (!adg) return;
    pel.classList.remove('lompat'); void pel.offsetWidth; pel.classList.add('lompat');
    W.setTimeout(function() { pel.classList.remove('lompat'); }, 700);
    var lama = adg.querySelector('.gelembung'); if (lama && lama.parentNode) lama.parentNode.removeChild(lama);
    var g = D.createElement('div'); g.className = 'gelembung';
    var sakit = D.querySelector('.vignette.v2, .vignette.v3');
    var daftar = sakit ? DIALOG_SAKIT : DIALOG;
    g.textContent = daftar[Math.floor(Math.random() * daftar.length)];
    adg.appendChild(g);
    g.style.left = Math.max(6, Math.min(pel.offsetLeft - 10, adg.clientWidth - g.offsetWidth - 6)) + 'px';
    var p = D.createElement('div'); p.className = 'piksel-emo';
    p.textContent = PIKSEL[Math.floor(Math.random() * PIKSEL.length)];
    p.style.left = (pel.offsetLeft + 18) + 'px';
    adg.appendChild(p);
    W.setTimeout(function() { if (g.parentNode) g.parentNode.removeChild(g); }, 2200);
    W.setTimeout(function() { if (p.parentNode) p.parentNode.removeChild(p); }, 1300);
    W.__rfSfx('lompat');
  };

  // ── Klik global: suara klik di tombol + hitung 3 klik berturut-turut pada judul museum
  var hitung = 0, terakhir = 0;
  if (W.__rfClickH) D.removeEventListener('click', W.__rfClickH, true);
  W.__rfClickH = function(e) {
    var t = e.target;
    if (!t || !t.closest) return;
    var pel = t.closest('.pelari');
    if (pel && W.__rfPelari) W.__rfPelari(pel);
    var btn = t.closest('button');
    if (btn && btn.id !== 'rf-musik' && W.__rfSfx) W.__rfSfx('klik');
    if (t.closest('.judul-museum')) {
      var now = Date.now();
      hitung = (now - terakhir < 1200) ? hitung + 1 : 1;
      terakhir = now;
      if (hitung >= 3) { hitung = 0; W.__rfDisco(!D.documentElement.classList.contains('rf-disco')); }
    } else {
      hitung = 0;
    }
  };
  D.addEventListener('click', W.__rfClickH, true);

  // ── Unlock audio pada gesture pertama (klik / sentuh / tombol keyboard)
  if (W.__rfUnlockH) {
    ['pointerdown', 'touchend', 'keydown'].forEach(function(n) { D.removeEventListener(n, W.__rfUnlockH, true); });
  }
  W.__rfUnlockH = function() { ctx(); };
  ['pointerdown', 'touchend', 'keydown'].forEach(function(n) { D.addEventListener(n, W.__rfUnlockH, true); });

  // ── Layar judul: tekan Enter = tekan tombol PRESS START
  if (W.__rfKeyH) D.removeEventListener('keydown', W.__rfKeyH, true);
  W.__rfKeyH = function(e) {
    if (e.key !== 'Enter' || e.repeat) return;
    var btn = D.querySelector('.st-key-start button');
    if (btn) { e.preventDefault(); btn.click(); }
  };
  D.addEventListener('keydown', W.__rfKeyH, true);

  // ── Kembali aktif setelah tab/layar kembali terlihat
  if (W.__rfVisH) D.removeEventListener('visibilitychange', W.__rfVisH);
  W.__rfVisH = function() { if (!D.hidden && W.__rfMusikOn) ctx(); };
  D.addEventListener('visibilitychange', W.__rfVisH);
})();
"""

LOADER_JS = """
<script>
(function() {
  var P = window.parent;
  var KODE = __ENGINE__;
  try {
    if (P.__rfEngine !== "__VERSI__") {
      var s = P.document.createElement('script');
      s.textContent = KODE;
      P.document.head.appendChild(s);
    }
  } catch (e) {
    try { if (P.__rfEngine !== "__VERSI__") new P.Function(KODE)(); } catch (e2) {}
  }
  var jenis = "__JENIS__";   // nonce: __NONCE__
  if (jenis) P.setTimeout(function() { if (P.__rfSfx) P.__rfSfx(jenis); }, 120);
})();
</script>
"""


def mainkan_sfx(jenis: str):
    """Jadwalkan efek suara; dibunyikan di akhir run lewat render_sfx()."""
    st.session_state.sfx = jenis


def render_sfx():
    jenis = st.session_state.pop("sfx", "")
    if jenis:
        st.session_state.nonce = st.session_state.get("nonce", 0) + 1
    nonce = str(st.session_state.get("nonce", 0)) if jenis else "0"
    mesin = json.dumps(ENGINE_JS.replace("__VERSI__", VERSI_ENGINE))
    kode = (LOADER_JS.replace("__VERSI__", VERSI_ENGINE)
                     .replace("__JENIS__", jenis)
                     .replace("__NONCE__", nonce)
                     .replace("__ENGINE__", mesin))
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


def total_poin() -> int:
    return st.session_state.skor + st.session_state.bonus


def pengikut_html(nama_list, baru: bool = False) -> str:
    """Hewan yang sudah tertangkap berbaris di belakang penjelajah (yang pertama paling dekat)."""
    n = len(nama_list)
    bagian = []
    for i in reversed(range(n)):          # yang terdekat digambar terakhir (di atas)
        h = HEWAN_BY_NAMA[nama_list[i]]
        kelas = "ikut baru" if (baru and i == n - 1) else "ikut"
        bagian.append(
            f'<div class="{kelas}" style="left:calc(34% - 26px - {i} * var(--st))">'
            f'<div class="ikut-b" style="animation-delay:{i * 0.07:.2f}s">{hewan_svg(h, 32)}</div></div>'
        )
    return "".join(bagian)


def adegan(kunci: str, hewan=None, mode: str = "polos", pengikut=()) -> str:
    """
    Adegan penjelajah di hutan pinus.
    mode: polos (hanya lari) | loop (menangkap berulang) | tangkap (berhasil) | kabur (hewan lolos)
    pengikut: daftar nama hewan yang sudah tertangkap (ikut berbaris di belakang karakter)
    """
    info = KARAKTER[kunci]
    tambahan = pengikut_html(list(pengikut), baru=(mode == "tangkap")) if pengikut else ""
    if hewan:
        tambahan += f'<div class="hewan"><span>{hewan_svg(hewan, 48)}</span></div>'
        tambahan += rintangan_html()
        if mode != "kabur":
            tambahan += (f'<div class="lempar"><div class="ly"><div class="lr">{pokeball_svg(info["bola"], 20)}</div></div></div>'
                         + ('<div class="kilau">✨</div>' if mode == "tangkap" else ""))
        if mode == "loop":
            tambahan += '<div class="miss">MELESET!</div>'
        if mode == "tangkap":
            tambahan += '<div class="tag">✨ Tertangkap!</div>'
        if mode == "kabur":
            tambahan += '<div class="tag oren">💨 Kabur!</div>'
    return rapat(f"""
        <div class="adegan {mode}">
            <div class="bulan"></div>
            <div class="lapis jauh"></div>
            <div class="lapis dekat"></div>
            <div class="tanah"></div>
            <div class="pelari">
                {sprite_svg(kunci, 52, 0, "k1")}
                {sprite_svg(kunci, 52, 1, "k2")}
            </div>
            {tambahan}
        </div>
    """)


def adegan_kejar(kunci: str) -> str:
    """Layar judul: penjelajah pixel berlari mengejar tiga hewan yang kabur."""
    buruan = [("komodo", 36, "0s"), ("harimau sumatera", 55, "0.12s"), ("maleo", 74, "0.24s")]
    hewan_html = "".join(
        f'<div class="buru" style="left:{x}%;animation-delay:{d}"><div class="buru-b" style="animation-delay:{d}">'
        f'{hewan_svg(HEWAN_BY_NAMA[nm], 46)}</div></div>'
        for nm, x, d in buruan
    )
    return rapat(f"""
        <div class="adegan kejar">
            <div class="bulan"></div>
            <div class="lapis jauh"></div>
            <div class="lapis dekat"></div>
            <div class="tanah"></div>
            <div class="pelari">
                {sprite_svg(kunci, 52, 0, "k1")}
                {sprite_svg(kunci, 52, 1, "k2")}
            </div>
            <div class="seru">!!</div>
            {hewan_html}
        </div>
    """)


def adegan_ending(kunci: str, tertangkap, offset: float = 0.0) -> str:
    """
    Pelepasan satwa (bola terbuka satu per satu) lalu foto bersama berbaris rapi.
    HANYA hewan yang berhasil ditangkap (jawaban benar) yang muncul di sini.
    """
    info = KARAKTER[kunci]
    jeda_foto = 6.0 + offset
    daftar = list(tertangkap)

    def slot(i: int, h: dict) -> str:
        d = f"{0.6 + i * 0.45 + offset:.2f}s"
        bola = pokeball_svg(info["bola"], 20)
        return (f'<div class="slot"><span class="bola-s" style="animation-delay:{d}">{bola}</span>'
                f'<span class="sat" style="animation-delay:{d}">{hewan_svg(h, 36)}</span></div>')

    n = len(daftar)
    n_depan = min(4, n // 2)
    belakang_list = daftar[: n - n_depan]
    depan_list = daftar[n - n_depan:]
    separuh = n_depan // 2

    belakang = "".join(slot(i, h) for i, h in enumerate(belakang_list))
    kiri = "".join(slot(len(belakang_list) + i, h) for i, h in enumerate(depan_list[:separuh]))
    kanan = "".join(slot(len(belakang_list) + separuh + i, h) for i, h in enumerate(depan_list[separuh:]))
    penjelajah = sprite_svg(kunci, 56, 1)

    if n:
        cap1 = f"🌿 Melepas {n} satwa kembali ke alam…"
        cap2 = "📸 Foto bersama penjaga alam!"
    else:
        cap1 = "🌿 Belum ada satwa yang tertangkap…"
        cap2 = "📸 Foto sendirian dulu, coba lagi ya!"

    return rapat(f"""
        <div class="adegan panggung" style="animation:panggungBuka 0.7s ease {offset}s both">
            <div class="bulan"></div>
            <div class="lapis jauh"></div>
            <div class="lapis dekat"></div>
            <div class="tanah"></div>
            <div class="cap cap1" style="animation-delay:{jeda_foto - 0.4:.1f}s">{cap1}</div>
            <div class="cap cap2" style="animation-delay:{jeda_foto:.1f}s">{cap2}</div>
            <div class="tq" style="animation-delay:{jeda_foto + 0.3:.1f}s">THANK YOU FOR PLAYING!</div>
            <div class="baris belakang">{belakang}</div>
            <div class="baris depan">{kiri}<div class="slot kar">{penjelajah}</div>{kanan}</div>
            <div class="bingkai" style="animation-delay:{jeda_foto:.1f}s"></div>
            <div class="flash-foto" style="animation-delay:{jeda_foto:.1f}s"></div>
        </div>
    """)


def rintangan_html() -> str:
    """Batang kayu & batu di jalur lemparan: Pokéball hanya bisa menembus kalau jawabannya benar."""
    return rapat(
        f'<div class="rintangan log" style="left:54%">{grid_svg(GRID_BATANG, PALET_BATANG, 44)}</div>'
        f'<div class="rintangan" style="left:63%">{grid_svg(GRID_BATU, PALET_BATU, 32)}</div>'
    )


def adegan_api(kunci: str, tertangkap) -> str:
    """
    Ending bagian 1 (sebelum foto): oknum nakal + temannya (penjual satwa) datang dari kiri,
    pohon-pohon terbakar; sang penjelajah melihat, mengejar, lalu menangkap keduanya.
    """
    def orang(pal=None):
        return (f'<div class="org-b">{sprite_svg(kunci, 52, 0, "k1", pal)}'
                f'{sprite_svg(kunci, 52, 1, "k2", pal)}</div>')

    h_sel = HEWAN_BY_NAMA[tertangkap[0]] if tertangkap else HEWAN_BY_NAMA["jalak bali"]
    api = "".join(
        f'<div class="api-api" style="left:{x}%"><div class="api-b">{grid_svg(GRID_API, PALET_API, 34)}</div></div>'
        for x in (52, 60, 68, 76)
    ) + "".join(
        f'<div class="api-api" style="left:{x}%;bottom:56px"><div class="api-b">{grid_svg(GRID_API, PALET_API, 22)}</div></div>'
        for x in (56, 64, 72)
    )
    return rapat(f"""
        <div class="adegan api">
            <div class="bulan"></div>
            <div class="lapis jauh"></div>
            <div class="lapis dekat"></div>
            <div class="tanah"></div>
            <div class="merah"></div>
            <div class="cap capA">🔥 Oknum nakal mau membakar hutan &amp; menjual satwa!</div>
            <div class="cap capB">👀 Sang penjelajah melihatnya… beraksi!</div>
            <div class="cap capC">🚨 Kedua pelaku tertangkap! Api padam, satwa selamat!</div>
            {api}
            <div class="penyel org">{orang(PAL_PENYEL)}
                <div class="sangkar"><div class="isi">{hewan_svg(h_sel, 22)}</div></div>
                <div class="balon">Ampun!</div>
            </div>
            <div class="pembakar org">{orang(PAL_PEMBAKAR)}
                <div class="obor">{grid_svg(GRID_API, PALET_API, 16)}<i class="gagang"></i></div>
                <div class="balon">Ampun!</div>
            </div>
            <div class="satwa-bebas"><div class="sb-b">{hewan_svg(h_sel, 40)}</div></div>
            <div class="hero">
                <div class="flip">{orang()}</div>
                <div class="tanda">!</div>
                <div class="balon bh">Berhenti!</div>
            </div>
        </div>
    """)


def bar_profil() -> str:
    kunci = st.session_state.karakter
    info = KARAKTER[kunci]
    nomor = min(st.session_state.no_soal + 1, TOTAL_SOAL)
    jantung = "".join("❤️" if i < st.session_state.nyawa else "🖤" for i in range(MAX_NYAWA))
    return rapat(f"""
        <div class="profil animasi">
            <div class="ava">{sprite_svg(kunci, 34, 1)}</div>
            <div class="info">
                <div class="nama-profil">{html.escape(st.session_state.nama_pemain)}</div>
                <div class="meta">{pokeball_svg(info['bola'], 16)} {info['nama']} · Soal {nomor}/{TOTAL_SOAL} · 🐾 {len(st.session_state.tertangkap)}</div><div class="nyawa">{jantung}</div>
            </div>
            <div class="skor">⭐ {total_poin()}</div>
        </div>
    """)


def mulai_ulang():
    """Reset kuis; nama dan karakter tetap dipertahankan."""
    st.session_state.skor = 0
    st.session_state.bonus = 0
    st.session_state.no_soal = 0
    st.session_state.status = None          # None | "benar" | "lewat" | "habis"
    st.session_state.nyawa = MAX_NYAWA
    st.session_state.clue_buka = 0
    st.session_state.salah_kali = 0
    st.session_state.emoji = "😄"
    st.session_state.balon = False
    st.session_state.tertangkap = []        # nama hewan yang dijawab benar (urut tangkap)
    st.session_state.soal_acak = random.sample(daftar_hewan, len(daftar_hewan))
    st.session_state.critter_soal = set(random.sample(range(TOTAL_SOAL), min(JUMLAH_CRITTER, TOTAL_SOAL)))
    st.session_state.critter_ketemu = set()


st.session_state.setdefault("nama_pemain", "")
st.session_state.setdefault("karakter", "red")
st.session_state.setdefault("judul_lewat", False)
if "soal_acak" not in st.session_state:
    mulai_ulang()

pesan_toast = st.session_state.pop("toast", None)
if pesan_toast:
    st.toast(pesan_toast, icon="🐹")


# ─────────────────────────────────────────────────────────────
# LAYAR JUDUL: PRESS START (tombol atau Enter)
# ─────────────────────────────────────────────────────────────
if not st.session_state.judul_lewat:
    st.markdown(
        rapat("""
        <div class="judul-layar animasi">
            <div class="jl-atas">★ FAUNA ADVENTURE ★</div>
            <div class="jl-logo">FAURARE<br>QUIZ</div>
        </div>
        """),
        unsafe_allow_html=True,
    )
    st.markdown(adegan_kejar(st.session_state.karakter), unsafe_allow_html=True)
    st.markdown(
        '<div class="judul-layar"><div class="jl-hint">TANGKAP SEMUA SATWA NUSANTARA!<br>TEKAN ENTER ATAU TOMBOL DI BAWAH</div></div>',
        unsafe_allow_html=True,
    )
    if st.button("▶ PRESS START", key="start", type="primary", use_container_width=True):
        st.session_state.judul_lewat = True
        mainkan_sfx("mulai")
        st.rerun()
    st.markdown('<div class="jl-hak">© FAURARE QUIZ · NUSANTARA</div>', unsafe_allow_html=True)
    render_sfx()
    st.stop()


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
    st.markdown(adegan(st.session_state.karakter), unsafe_allow_html=True)

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
3. Jawaban benar = **+{POIN_PER_SOAL} poin**, hewannya tertangkap dan **ikut berbaris di belakangmu**.
4. Soal selalu **diacak**: {TOTAL_SOAL} soal, skor maksimal {SKOR_MAKS}.
5. Di akhir, hanya hewan yang **berhasil kamu tangkap** yang ikut berfoto bersamamu.
6. Kamu punya **3 nyawa ❤️**: salah menjawab = nyawa berkurang dan layar makin gelap kemerahan. Nyawa habis = ekspedisi berakhir.

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
    status = st.session_state.status
    mode_adegan = {None: "loop", "benar": "tangkap", "lewat": "kabur", "habis": "kabur"}[status]
    hilang = max(0, MAX_NYAWA - st.session_state.nyawa)
    kena = st.session_state.pop("baru_kena", False)
    st.markdown(f'<div class="vignette v{hilang}"></div>' + ('<div class="kena-flash"></div>' if kena else ""),
                unsafe_allow_html=True)

    st.markdown(bar_profil(), unsafe_allow_html=True)
    st.markdown(adegan(st.session_state.karakter, h, mode_adegan, st.session_state.tertangkap),
                unsafe_allow_html=True)

    # Easter egg: Pixel Critter (hanya muncul di soal tertentu, saat masih menebak)
    idx = st.session_state.no_soal
    if status is None and idx in st.session_state.critter_soal and idx not in st.session_state.critter_ketemu:
        posisi = SUDUT_CRITTER[idx % len(SUDUT_CRITTER)]
        st.markdown(f"<style>.st-key-critter{{{posisi}}}</style>", unsafe_allow_html=True)
        if st.button("🐹", key="critter"):
            st.session_state.bonus += BONUS_CRITTER
            st.session_state.critter_ketemu.add(idx)
            st.session_state.toast = f"Pixel Critter ditemukan! +{BONUS_CRITTER} bonus poin"
            mainkan_sfx("bonus")
            st.rerun()

    if h.get("gambar"):
        kartu_visual = f"<img src='{html.escape(h['gambar'])}' style='max-width:100%; border-radius:16px; margin:10px 0;'>"
    else:
        kartu_visual = f"<span class='ikon-besar'>{hewan_svg(h, 200)}</span>"

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
    if status in ("benar", "lewat", "habis"):
        terakhir = nomor == TOTAL_SOAL
        nama_hewan = html.escape(h["nama"].title())
        fakta = html.escape(h["fakta"])
        if status == "benar":
            st.markdown(
                rapat(f"""
                <div class="glass hasil-benar animasi">
                    <div class="reaksi"><span>{st.session_state.emoji}</span><span>{hewan_svg(h, 68)}</span></div>
                    <h3 style="margin:0 0 6px 0; text-align:center;">Benar! +{POIN_PER_SOAL} poin</h3>
                    <div style="text-align:center; font-size:0.85rem; opacity:0.85; margin-bottom:6px;">
                        🐾 {nama_hewan} ikut berbaris di belakangmu!
                    </div>
                    <span>💡 <b>Fakta Unik:</b> {fakta}</span>
                </div>
                """),
                unsafe_allow_html=True,
            )
        elif status == "lewat":
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
        if status == "habis":
            st.markdown(
                rapat(f"""
                <div class="glass hasil-salah animasi">
                    <div class="reaksi"><span>💔</span></div>
                    <h3 style="margin:0 0 6px 0; text-align:center;">Nyawa habis! Ekspedisi berakhir</h3>
                    <b>🐾 Jawabannya: {nama_hewan}</b><br>
                    <span>💡 <b>Fakta Unik:</b> {fakta}</span>
                </div>
                """),
                unsafe_allow_html=True,
            )
        label = "🏁 Lihat Hasil Akhir" if (terakhir or status == "habis") else "➡️ Lanjut ke Soal Berikutnya"
        if st.button(label, use_container_width=True, type="primary"):
            st.session_state.status = None
            st.session_state.clue_buka = 0
            st.session_state.salah_kali = 0
            st.session_state.no_soal = TOTAL_SOAL if status == "habis" else st.session_state.no_soal + 1
            if terakhir or status == "habis":
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
                # Hewan tertangkap → ikut berbaris & ikut foto bersama di ending
                if h["nama"] not in st.session_state.tertangkap:
                    st.session_state.tertangkap.append(h["nama"])
                mainkan_sfx("benar")
                st.rerun()
            else:
                st.session_state.salah_kali += 1
                st.session_state.nyawa -= 1
                st.session_state.baru_kena = True
                mainkan_sfx("luka")
                if st.session_state.nyawa <= 0:
                    st.session_state.status = "habis"
                else:
                    st.session_state.salah_info = random.choice(EMOJI_SALAH)
                st.rerun()

        info_salah = st.session_state.pop("salah_info", None)
        if info_salah:
            saran = "Coba buka petunjuk di atas!" if st.session_state.clue_buka < len(h["clues"]) else "Baca petunjuknya sekali lagi."
            st.markdown(
                rapat(f"""
                <div class="glass hasil-salah">
                    <div class="salah-baris">
                        <span class="emo">{info_salah}</span>
                        <div><b>Yah, belum tepat!</b> Nyawa berkurang 💔 (sisa {st.session_state.nyawa} dari {MAX_NYAWA})<br>
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
    bonus = st.session_state.bonus
    total = skor + bonus
    gelar, predikat, ikon_gelar = gelar_dari_skor(total)
    kunci = st.session_state.karakter
    tangkapan = [HEWAN_BY_NAMA[n] for n in st.session_state.tertangkap]

    if not st.session_state.balon:
        st.session_state.balon = True
        st.balloons()

    # Scene ending: pelepasan satwa → foto bersama (hanya hewan yang tertangkap)
    st.markdown(adegan_api(kunci, st.session_state.tertangkap), unsafe_allow_html=True)
    st.markdown(adegan_ending(kunci, tangkapan, OFFSET_FOTO), unsafe_allow_html=True)

    rincian = (f"<div style='opacity:0.8; font-size:0.85rem;'>🐾 {len(tangkapan)} / {TOTAL_SOAL} satwa tertangkap"
               + (f" · {skor} poin soal + {bonus} bonus 🐹" if bonus else "") + "</div>")
    st.markdown(
        rapat(f"""
        <div class="glass animasi" style="text-align:center;">
            <div class="subjudul">🎉 Ujian &amp; Ekspedisi Nusantara Selesai 🎉</div>
            <h2 style="margin:6px 0 0 0;">Sidang Kelulusan: {nama_aman}</h2>
            <div style="font-size:2.6rem; margin-top:6px;">{ikon_gelar}</div>
            <div class="gelar">{html.escape(gelar)}</div>
            <div style="font-weight:600;">{html.escape(predikat)}</div>
            <div style="margin-top:12px; font-size:1.15rem;">
                Total Nilai Akhir: <b>{total}</b> poin
            </div>
            {rincian}
        </div>
        """),
        unsafe_allow_html=True,
    )

    # Judul rahasia: klik 3x berturut-turut untuk Mode Disko (ditangani JS di halaman induk)
    st.markdown('<h3 class="judul-museum">🏛️ Museum Mini ni bosz</h3>', unsafe_allow_html=True)
    st.caption(f"Pelajari kembali fakta unik dari ke-{TOTAL_SOAL} hewan endemik:")
    for i, item in enumerate(daftar_hewan, start=1):
        with st.expander(f"{i}. {item['nama'].title()} — {item['kategori']}"):
            st.markdown(f"<span class='mini-hewan'>{hewan_svg(item, 30)}</span>", unsafe_allow_html=True)
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
