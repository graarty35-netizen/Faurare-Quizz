import base64
import html
import os
import random
import re

import streamlit as st
import streamlit.components.v1 as components

# ─────────────────────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RareFauna Quiz Indonesia",
    page_icon="🇮🇩",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Backsound: taruh file "backsound.mp3" di folder yang sama dengan app.py
# untuk hasil paling stabil. Jika tidak ada, dipakai link online di bawah.
BACKSOUND_URL = (
    "https://cdn.pixabay.com/download/audio/2022/05/16/"
    "audio_db32c41793.mp3?filename=forest-with-birds-and-wind-111158.mp3"
)
BACKSOUND_LOKAL = "backsound.mp3"

POIN_PER_SOAL = 10

# ─────────────────────────────────────────────────────────────
# DATABASE HEWAN
# "gambar" opsional: isi dengan link foto / nama file lokal jika ingin foto asli.
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

# Catatan: daftar di atas berisi 9 hewan; tambahan ke-10 ada di bawah.
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


# ─────────────────────────────────────────────────────────────
# GAYA TAMPILAN (CSS) — glassmorphism, font Google, responsif HP/iPad
# ─────────────────────────────────────────────────────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Poppins:wght@400;500;600&display=swap');

html, body, [class*="css"], .stApp, p, label, li, span, div {
    font-family: 'Poppins', sans-serif;
}
h1, h2, h3, .judul-game {
    font-family: 'Fredoka', sans-serif !important;
    letter-spacing: 0.3px;
}

/* Latar sinematik: gradasi hutan malam + cahaya lembut */
.stApp {
    background:
        radial-gradient(circle at 15% 10%, rgba(255, 214, 102, 0.22), transparent 35%),
        radial-gradient(circle at 85% 20%, rgba(94, 234, 212, 0.18), transparent 40%),
        radial-gradient(circle at 50% 100%, rgba(34, 197, 94, 0.25), transparent 50%),
        linear-gradient(160deg, #04200f 0%, #0b3b2a 45%, #08283a 100%);
    background-attachment: fixed;
    color: #f1f5f9;
}
[data-testid="stHeader"] { background: transparent; }
footer, #MainMenu { visibility: hidden; }

.block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 760px; }

/* Warna teks bawaan Streamlit supaya terbaca di latar gelap */
.stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label,
.stApp li, [data-testid="stMarkdownContainer"] { color: #f1f5f9; }
[data-testid="stCaptionContainer"] { color: #cbd5e1; }

/* Sidebar kaca */
[data-testid="stSidebar"] {
    background: rgba(6, 30, 20, 0.72);
    backdrop-filter: blur(14px);
    border-right: 1px solid rgba(255, 255, 255, 0.10);
}

/* Kontainer kaca (glassmorphism) */
.glass {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35);
    margin-bottom: 18px;
}

.judul-game {
    text-align: center; font-size: clamp(1.7rem, 6vw, 2.6rem); font-weight: 700;
    background: linear-gradient(90deg, #fde68a, #86efac, #67e8f9);
    -webkit-background-clip: text; background-clip: text; color: transparent !important;
    margin: 0 0 6px 0;
}
.subjudul { text-align: center; opacity: 0.85; margin-bottom: 14px; }

/* Kartu indeks hewan */
.kartu-hewan {
    position: relative; text-align: center; overflow: hidden;
    padding: 26px 16px 20px;
}
.kartu-hewan .lencana {
    display: inline-block; padding: 5px 14px; border-radius: 999px; font-size: 0.82rem; font-weight: 600;
    background: rgba(253, 230, 138, 0.18); border: 1px solid rgba(253, 230, 138, 0.45); color: #fde68a;
}
.kartu-hewan .ikon-besar {
    font-size: clamp(80px, 24vw, 130px); line-height: 1.15; display: block; margin: 10px 0 2px;
    animation: melayang 3.6s ease-in-out infinite;
    filter: drop-shadow(0 10px 18px rgba(0, 0, 0, 0.45));
}
.kartu-hewan .ikon-latar {
    position: absolute; right: 14px; top: 10px; font-size: 2rem; opacity: 0.55;
    animation: melayang 5s ease-in-out infinite reverse;
}
.kartu-hewan .nomor { font-family: 'Fredoka', sans-serif; font-size: 1.05rem; opacity: 0.85; }
.kartu-hewan .tanya { font-weight: 600; font-size: 1.05rem; margin-top: 6px; }

@keyframes melayang {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}
@keyframes muncul {
    from { opacity: 0; transform: translateY(14px) scale(0.98); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}
.animasi { animation: muncul 0.55s ease both; }

/* Kotak clue */
.clue {
    background: rgba(255, 255, 255, 0.07); border-left: 4px solid #fde68a;
    border-radius: 12px; padding: 10px 14px; margin: 8px 0; animation: muncul 0.4s ease both;
}

/* Kotak hasil */
.hasil-benar { border-color: rgba(134, 239, 172, 0.6); background: rgba(34, 197, 94, 0.16); }
.hasil-lewat { border-color: rgba(253, 186, 116, 0.6); background: rgba(249, 115, 22, 0.14); }

/* Lencana gelar */
.gelar {
    text-align: center; font-family: 'Fredoka', sans-serif; font-weight: 700;
    font-size: clamp(2rem, 9vw, 3.4rem); margin: 4px 0;
    background: linear-gradient(90deg, #fde68a, #fb923c);
    -webkit-background-clip: text; background-clip: text; color: transparent !important;
}

/* Tombol: besar & mudah disentuh di HP/iPad */
.stButton > button, [data-testid="stFormSubmitButton"] > button {
    min-height: 3rem; border-radius: 14px; font-weight: 600; font-size: 1rem;
    color: #052e16; border: none;
    background: linear-gradient(135deg, #fde68a, #86efac);
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.3);
    transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease;
}
.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-2px); filter: brightness(1.06); color: #052e16;
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.4);
}
.stButton > button:active, [data-testid="stFormSubmitButton"] > button:active { transform: scale(0.97); }

/* Input teks */
.stTextInput input {
    min-height: 3rem; font-size: 1.05rem; border-radius: 14px;
    background: rgba(255, 255, 255, 0.10) !important; color: #f8fafc !important;
    border: 1px solid rgba(255, 255, 255, 0.28) !important;
}
.stTextInput input::placeholder { color: #cbd5e1 !important; opacity: 0.8; }

/* Expander, metric, form */
[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.07); border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 16px; backdrop-filter: blur(10px);
}
[data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.16);
    border-radius: 18px; backdrop-filter: blur(10px);
}
[data-testid="stMetricValue"] { font-family: 'Fredoka', sans-serif; color: #fde68a; }
[data-testid="stMetricLabel"] { color: #cbd5e1; }
.stProgress > div > div > div > div { background: linear-gradient(90deg, #fde68a, #86efac); }
hr { border-color: rgba(255, 255, 255, 0.15) !important; }

/* Komponen iframe tinggi 0 (efek suara) jangan memakan ruang */
iframe[height="0"] { display: none; }

/* Responsif HP kecil */
@media (max-width: 640px) {
    .block-container { padding-left: 0.9rem; padding-right: 0.9rem; padding-top: 1rem; }
    .glass { padding: 16px; border-radius: 18px; }
}
@media (prefers-reduced-motion: reduce) {
    .ikon-besar, .ikon-latar, .animasi, .clue { animation: none !important; }
}
"""
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# FUNGSI BANTU
# ─────────────────────────────────────────────────────────────
def normalisasi(teks: str) -> str:
    """Huruf kecil, buang simbol, rapikan spasi."""
    teks = re.sub(r"[^a-z0-9\s]", " ", teks.lower())
    return re.sub(r"\s+", " ", teks).strip()


def cek_jawaban(jawaban: str, hewan: dict) -> bool:
    kunci = {normalisasi(hewan["nama"])} | {normalisasi(a) for a in hewan.get("alias", [])}
    return normalisasi(jawaban) in kunci


def gelar_dari_skor(skor: int):
    """Sistem gelar kustom. Mengembalikan (gelar, predikat, ikon)."""
    if skor >= 90:
        return "S.Hwn", "Luar Biasa! Sarjana Hewan sejati!", "🏆"
    if skor >= 60:
        return "S.k", "Hebat! Wawasan faunamu keren!", "🥈"
    if skor >= 30:
        return "S.Tda", "Cukup! Masih bisa lebih baik lagi!", "🥉"
    return "ADOHHHHH, heran", "Yuk ujian ulang dan baca petunjuknya!", "🤦"


def mainkan_sfx(jenis: str):
    """Jadwalkan efek suara; dimainkan di akhir run lewat render_sfx()."""
    st.session_state.sfx = jenis


def render_sfx():
    """
    Efek suara dibuat dengan WebAudio (tanpa file). Komponen ini juga memasang
    suara 'klik' otomatis ke semua tombol di halaman (hanya sekali).
    """
    jenis = st.session_state.pop("sfx", "")
    st.session_state.setdefault("nonce", 0)
    st.session_state.nonce += 1
    components.html(
        f"""
<script>
(function() {{
  var P = window.parent;
  function ctx() {{
    var AC = P.AudioContext || P.webkitAudioContext;
    if (!AC) return null;
    if (!P.__rfCtx) P.__rfCtx = new AC();
    if (P.__rfCtx.state === 'suspended') P.__rfCtx.resume();
    return P.__rfCtx;
  }}
  function nada(f, mulai, dur, tipe, vol) {{
    var c = ctx(); if (!c) return;
    var o = c.createOscillator(), g = c.createGain();
    o.type = tipe || 'sine'; o.frequency.value = f;
    var t = c.currentTime + mulai;
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol || 0.18, t + 0.02);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    o.connect(g); g.connect(c.destination);
    o.start(t); o.stop(t + dur + 0.05);
  }}
  P.__rfSfx = function(jenis) {{
    if (jenis === 'klik')   {{ nada(660, 0, 0.08, 'triangle', 0.12); }}
    if (jenis === 'benar')  {{ [523, 659, 784, 1047].forEach(function(f, i) {{ nada(f, i * 0.09, 0.22, 'triangle', 0.2); }}); }}
    if (jenis === 'salah')  {{ nada(220, 0, 0.18, 'sawtooth', 0.12); nada(150, 0.16, 0.3, 'sawtooth', 0.12); }}
    if (jenis === 'lewat')  {{ nada(440, 0, 0.12, 'sine', 0.14); nada(330, 0.12, 0.2, 'sine', 0.14); }}
    if (jenis === 'selesai'){{ [523, 659, 784, 1047, 784, 1047, 1319].forEach(function(f, i) {{ nada(f, i * 0.12, 0.3, 'triangle', 0.2); }}); }}
  }};
  if (!P.__rfBound) {{
    P.__rfBound = true;
    P.document.addEventListener('click', function(e) {{
      if (e.target && e.target.closest && e.target.closest('button')) P.__rfSfx('klik');
    }}, true);
  }}
  var jenis = "{jenis}";   // nonce: {st.session_state.nonce}
  if (jenis) setTimeout(function() {{ P.__rfSfx(jenis); }}, 120);
}})();
</script>
""",
        height=0,
    )


def tampilkan_backsound():
    """Pemutar audio di dalam iframe sendiri agar tidak putus saat halaman rerun."""
    if os.path.exists(BACKSOUND_LOKAL):
        with open(BACKSOUND_LOKAL, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        sumber = f"data:audio/mpeg;base64,{b64}"
    else:
        sumber = BACKSOUND_URL
    components.html(
        f"""
<style>
  body {{ margin: 0; font-family: sans-serif; }}
  audio {{ width: 100%; height: 40px; }}
</style>
<audio id="bgm" controls loop preload="auto">
  <source src="{sumber}" type="audio/mpeg">
  Browser kamu tidak mendukung pemutar audio.
</audio>
<script>
  var a = document.getElementById('bgm');
  a.volume = 0.45;
</script>
""",
        height=52,
    )


def mulai_ulang(pertahankan_nama: bool = True):
    nama = st.session_state.get("nama_pemain", "") if pertahankan_nama else ""
    st.session_state.skor = 0
    st.session_state.no_soal = 0
    st.session_state.status = None          # None | "benar" | "lewat"
    st.session_state.clue_buka = 0
    st.session_state.salah_kali = 0
    st.session_state.nama_pemain = nama
    st.session_state.soal_acak = random.sample(daftar_hewan, len(daftar_hewan))


if "soal_acak" not in st.session_state:
    mulai_ulang(pertahankan_nama=False)


# ─────────────────────────────────────────────────────────────
# HALAMAN AWAL (PENDAFTARAN)
# ─────────────────────────────────────────────────────────────
if st.session_state.nama_pemain == "":
    st.markdown(
        """
        <div class="glass animasi">
            <div class="judul-game">🇮🇩 RareFauna Quiz Indonesia 🇮🇩</div>
            <div class="subjudul">Kuis Endemik Fauna Nusantara — raih gelar Sarjana Hewan!</div>
            <div style="text-align:center; font-size: 3rem;">🦧 🐅 🦏 🦜 🐘</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="glass animasi">
            <b>📖 Cara Bermain</b>
            <ol style="margin: 8px 0 0 0; padding-left: 1.2rem;">
                <li>Lihat <b>kartu hewan</b> dan wilayah asalnya.</li>
                <li>Tebak nama hewannya, lalu tekan <b>Kirim</b> (atau Enter).</li>
                <li>Bingung? Buka <b>petunjuk</b> satu per satu (maks. 3).</li>
                <li>Jawaban benar = <b>+10 poin</b> dan kamu bisa baca fakta uniknya.</li>
                <li>Soal selalu <b>diacak</b>. Total 10 soal, skor maksimal 100.</li>
            </ol>
            <div style="margin-top:10px; opacity:0.9;">
                🎓 <b>Gelar:</b> 90–100 <code>S.Hwn</code> · 60–80 <code>S.k</code> ·
                30–50 <code>S.Tda</code> · di bawah 30 <code>ADOHHHHH, heran</code>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("form_daftar", clear_on_submit=False):
        nama = st.text_input("Siapa nama calon Sarjana Hewan?", placeholder="Ketik namamu di sini...")
        masuk = st.form_submit_button("🚀 Mulai Ujian Ekspedisi!", use_container_width=True)
    if masuk:
        if nama.strip():
            mulai_ulang(pertahankan_nama=False)
            st.session_state.nama_pemain = nama.strip()
            mainkan_sfx("benar")
            st.rerun()
        else:
            st.warning("Tulis namamu dulu ya!")
            mainkan_sfx("salah")

    render_sfx()
    st.stop()


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
nama_aman = html.escape(st.session_state.nama_pemain)
with st.sidebar:
    st.header(f"Explorer: {st.session_state.nama_pemain} 🇮🇩")
    st.metric("Skor Sementara", f"{st.session_state.skor} Poin")
    kemajuan = min(st.session_state.no_soal / TOTAL_SOAL, 1.0)
    st.progress(kemajuan)
    st.caption(f"Soal {min(st.session_state.no_soal + 1, TOTAL_SOAL)} dari {TOTAL_SOAL}")

    st.divider()
    st.subheader("🎵 Backsound Alam")
    tampilkan_backsound()
    st.caption("Tekan ▶ untuk memutar. Di HP/iPad, browser butuh satu sentuhan dulu.")

    st.divider()
    if st.button("🔄 Mulai Ulang Kuis", use_container_width=True):
        mulai_ulang()
        st.rerun()


# ─────────────────────────────────────────────────────────────
# PERMAINAN
# ─────────────────────────────────────────────────────────────
if st.session_state.no_soal < TOTAL_SOAL:
    h = st.session_state.soal_acak[st.session_state.no_soal]
    nomor = st.session_state.no_soal + 1

    # Kartu indeks visual
    if h.get("gambar"):
        kartu_visual = f"<img src='{html.escape(h['gambar'])}' style='max-width:100%; border-radius:16px; margin:10px 0;'>"
    else:
        kartu_visual = f"<span class='ikon-besar'>{h['ikon']}</span>"

    st.markdown(
        f"""
        <div class="glass kartu-hewan animasi">
            <span class="ikon-latar">{h['latar']}</span>
            <div class="nomor">Soal {nomor} / {TOTAL_SOAL}</div>
            <span class="lencana">📍 {html.escape(h['kategori'])}</span>
            {kartu_visual}
            <div class="tanya">Hewan endemik apakah ini?</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Setelah menjawab benar / menyerah: tampilkan fakta + tombol lanjut
    if st.session_state.status in ("benar", "lewat"):
        terakhir = nomor == TOTAL_SOAL
        if st.session_state.status == "benar":
            st.markdown(
                f"""
                <div class="glass hasil-benar animasi">
                    <h3 style="margin:0 0 6px 0;">✅ Jawaban Benar! +{POIN_PER_SOAL} poin</h3>
                    <b>🐾 {html.escape(h['nama'].title())}</b><br>
                    <span>💡 <b>Fakta Unik:</b> {html.escape(h['fakta'])}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="glass hasil-lewat animasi">
                    <h3 style="margin:0 0 6px 0;">🏳️ Tidak apa-apa, kita belajar!</h3>
                    <b>🐾 Jawabannya: {html.escape(h['nama'].title())}</b><br>
                    <span>💡 <b>Fakta Unik:</b> {html.escape(h['fakta'])}</span>
                </div>
                """,
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
        # Petunjuk bertahap
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

        # Form jawaban (Enter = kirim, nyaman di HP)
        with st.form(key=f"form_{st.session_state.no_soal}", clear_on_submit=True):
            jawaban = st.text_input("Ketik tebakan nama hewan:", placeholder="contoh: komodo")
            kirim = st.form_submit_button("🎯 Kirim Jawaban", use_container_width=True)

        if kirim:
            if not jawaban.strip():
                st.warning("Ketik jawabanmu dulu ya!")
            elif cek_jawaban(jawaban, h):
                st.session_state.skor += POIN_PER_SOAL
                st.session_state.status = "benar"
                mainkan_sfx("benar")
                st.rerun()
            else:
                st.session_state.salah_kali += 1
                mainkan_sfx("salah")
                saran = " Coba buka petunjuk di atas!" if st.session_state.clue_buka < len(h["clues"]) else ""
                st.error(f"❌ Kurang tepat (percobaan salah: {st.session_state.salah_kali}).{saran}")

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
    st.balloons()

    st.markdown(
        f"""
        <div class="glass animasi" style="text-align:center;">
            <div class="subjudul">🎉 Ujian &amp; Ekspedisi Nusantara Selesai 🎉</div>
            <h2 style="margin:0;">Sidang Kelulusan: {nama_aman}</h2>
            <div style="font-size:3rem; margin-top:8px;">{ikon_gelar}</div>
            <div class="gelar">{html.escape(gelar)}</div>
            <div style="font-weight:600;">{html.escape(predikat)}</div>
            <div style="margin-top:12px; font-size:1.2rem;">
                Total Nilai Akhir: <b>{skor} / {SKOR_MAKS}</b> poin
            </div>
        </div>
        """,
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
        st.rerun()

render_sfx()
