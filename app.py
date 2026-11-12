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

# ─────────────────────────────────────────────────────────────
# CSS KUSTOM — TAMPILAN LEBIH BERSIH, RAPI, & ELEGAN
# ─────────────────────────────────────────────────────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');

html, body, .stApp, p, label, li, span, div, input, textarea, button {
    font-family: 'VT323', monospace;
}
.stApp p, .stApp li, .stApp label, [data-testid="stMarkdownContainer"] { font-size: 1.4rem; line-height: 1.3; }
h1, h2, h3, .judul, .pixel-font, .stButton button, [data-testid="stFormSubmitButton"] button {
    font-family: 'Press Start 2P', monospace !important;
}

.stApp {
    background: linear-gradient(135deg, #03080f 0%, #081424 50%, #030f0b 100%);
    color: #e2f8ec;
}
[data-testid="stHeader"] { background: transparent; }
footer, #MainMenu { visibility: hidden; }
.block-container { position: relative; z-index: 2; max-width: 720px; padding-top: 2rem; padding-bottom: 90px; }

/* Pemutar Musik Minimalis Melayang di Pojok Kanan Atas */
.floating-audio {
    position: fixed;
    top: 12px;
    right: 15px;
    z-index: 9999;
    background: rgba(4, 18, 12, 0.85);
    backdrop-filter: blur(6px);
    border: 2px solid #22c55e;
    padding: 4px 8px;
    border-radius: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.6);
}
.floating-audio audio {
    height: 28px;
    width: 125px;
}

/* Sidebar Rapi */
[data-testid="stSidebar"] {
    background: rgba(3, 12, 8, 0.95);
    border-right: 3px solid #22c55e;
}

/* Kotak Kartu Estetik */
.pixel-box {
    background: rgba(5, 20, 14, 0.85);
    backdrop-filter: blur(6px);
    border: 3px solid #22c55e;
    box-shadow: 6px 6px 0px rgba(0, 0, 0, 0.6);
    padding: 22px 18px;
    margin: 8px 4px 20px;
    text-align: center;
    border-radius: 6px;
}
.pixel-box.emas { border-color: #facc15; }
.pixel-box.hijau { border-color: #4ade80; background: rgba(20, 83, 45, 0.25); }
.pixel-box.merah { border-color: #f87171; background: rgba(127, 29, 29, 0.3); }

.judul {
    text-align: center; color: #4ade80 !important; line-height: 1.6;
    font-size: clamp(1rem, 4vw, 1.45rem); text-shadow: 2px 2px 0 #022c14;
    margin: 0 0 10px 0;
}
.judul .emas { color: #facc15; }

.hud { display: flex; justify-content: space-between; gap: 8px; margin: 4px 4px 14px; }
.hud span {
    flex: 1; text-align: center; padding: 8px 4px; font-family: 'Press Start 2P', monospace;
    font-size: clamp(0.5rem, 2.3vw, 0.7rem); background: rgba(3, 12, 8, 0.9);
    border: 2px solid #facc15; color: #fde68a; border-radius: 4px;
}
.bar { height: 14px; margin: 0 4px 16px; background: #020a06; border: 2px solid #22c55e; padding: 1px; border-radius: 3px; }
.bar > i { display: block; height: 100%; background: #4ade80; border-radius: 1px; }

.ikon-besar {
    display: block; font-size: clamp(70px, 18vw, 105px); line-height: 1.1; margin: 8px 0;
    filter: drop-shadow(4px 4px 0 rgba(0, 0, 0, 0.5));
}
.bisik { font-size: 1.35rem; font-style: italic; color: #bef264; margin-top: 4px; }

.clue {
    background: rgba(250, 204, 21, 0.08); border-left: 5px solid #facc15;
    padding: 8px 12px; margin: 8px 4px; font-size: 1.35rem;
}

.reaksi { font-size: clamp(2.2rem, 10vw, 3.5rem); letter-spacing: 4px; margin-bottom: 4px; }
.teks-reaksi { font-family: 'Press Start 2P', monospace; font-size: clamp(0.55rem, 2.5vw, 0.75rem); line-height: 1.6; margin-bottom: 8px; }

.gelar {
    text-align: center; font-family: 'Press Start 2P', monospace; color: #facc15;
    font-size: clamp(1.1rem, 5.5vw, 2.2rem); text-shadow: 3px 3px 0 #78350f; margin: 10px 0; line-height: 1.4;
}

/* Tombol Konsisten */
.stButton > button, [data-testid="stFormSubmitButton"] > button {
    min-height: 3rem; border-radius: 6px; border: 3px solid #022c14; color: #052e16;
    font-size: clamp(0.55rem, 2.5vw, 0.72rem); line-height: 1.4; padding: 8px 12px;
    background: #4ade80; box-shadow: 0 4px 0 #166534;
    transition: all 0.1s ease; margin-bottom: 6px; width: 100%;
}
.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover { background: #86efac; border-color: #022c14; }
.stButton > button:active, [data-testid="stFormSubmitButton"] > button:active { transform: translateY(3px); box-shadow: 0 1px 0 #166534; }
.stButton > button[kind="primary"], [data-testid="stFormSubmitButton"] > button[kind="primary"] {
    background: #facc15; box-shadow: 0 4px 0 #a16207; color: #422006;
}
.stButton > button[kind="primary"]:hover { background: #fde047; }

/* Input */
.stTextInput input {
    min-height: 3.1rem; border-radius: 6px !important; font-size: 1.5rem;
    background: #020a06 !important; color: #f0fdf4 !important; border: 3px solid #22c55e !important;
}
.stTextInput input::placeholder { color: #6ee7b7 !important; opacity: 0.6; }
.stTextInput input:focus { border-color: #facc15 !important; box-shadow: 0 0 8px rgba(250,204,21,0.4) !important; }
[data-testid="stForm"] { background: rgba(3, 15, 10, 0.85); border: 3px solid #22c55e; border-radius: 8px; padding: 12px; }
[data-testid="stExpander"] { background: rgba(3, 15, 10, 0.85); border: 2px solid #22c55e; border-radius: 6px; }
[data-testid="stMetricValue"] { font-family: 'Press Start 2P', monospace; color: #facc15; font-size: 1.2rem; }
[data-testid="stMetricLabel"] p { color: #86efac; }
hr { border-color: rgba(74, 222, 128, 0.25) !important; }
"""

# ─────────────────────────────────────────────────────────────
# STATE AWAL & LOGIKA APLIKASI
# ─────────────────────────────────────────────────────────────
if 'skor' not in st.session_state: st.session_state.skor = 0
if 'no_soal' not in st.session_state: st.session_state.no_soal = 0
if 'nama_pemain' not in st.session_state: st.session_state.nama_pemain = ""
if 'status_jawab' not in st.session_state: st.session_state.status_jawab = None
if 'fakta_sekarang' not in st.session_state: st.session_state.fakta_sekarang = ""
if 'soal_acak' not in st.session_state: 
    st.session_state.soal_acak = random.sample(daftar_hewan, len(daftar_hewan))

st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

# Pemutar Musik Minimalis di Pojok Kanan Atas (Tidak Mengganggu)
st.markdown("""
    <div class="floating-audio">
        <audio controls loop preload="auto">
            <source src="https://cdn.pixabay.com/download/audio/2022/03/15/audio_c8c325e648.mp3?filename=game-level-music-143026.mp3" type="audio/mpeg">
        </audio>
    </div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# HALAMAN DEPAN (LOGIN)
# ─────────────────────────────────────────────────────────────
if st.session_state.nama_pemain == "":
    st.markdown("<h1 class='judul'>🌲 RAREFAUNA RETRO QUIZ 🌲</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #86efac;'>Ekspedisi Menjelajah Hutan Endemik Indonesia</p>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class='pixel-box'>
            <span style='font-size: 55px;'>🧭✨</span>
            <p style='margin-top: 8px;'>Selamat datang, Explorer! Masukkan namamu untuk memulai ujian lapangan dan buktikan kamu layak menjadi Sarjana Satwa.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        nama = st.text_input("Nama Panggilanmu:", placeholder="Ketik namamu di sini...")
        if st.button("🕹️ MULAI EKSPEDISI", type="primary", use_container_width=True):
            if nama.strip():
                st.session_state.nama_pemain = nama.strip()
                st.session_state.status_jawab = None
                st.session_state.soal_acak = random.sample(daftar_hewan, len(daftar_hewan))
                st.rerun()
            else:
                st.warning("⚠️ Masukkan namamu dulu, Explorer!")
else:
    # ─────────────────────────────────────────────────────────────
    # SIDEBAR RINGKAS
    # ─────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown(f"### 🌲 {st.session_state.nama_pemain}")
        st.metric("Skor Sementara", f"{st.session_state.skor} Poin")
        st.progress(st.session_state.no_soal / TOTAL_SOAL)
        st.caption(f"Posisi: Soal {st.session_state.no_soal + 1} dari {TOTAL_SOAL}")
        st.divider()
        st.caption("🎵 Musik latar tegang aktif di pojok kanan atas layar.")
        if st.button("🔄 Reset / Keluar", use_container_width=True):
            st.session_state.nama_pemain = ""
            st.session_state.skor = 0
            st.session_state.no_soal = 0
            st.session_state.status_jawab = None
            st.rerun()

    # ─────────────────────────────────────────────────────────────
    # AREA PERMAINAN UTAMA
    # ─────────────────────────────────────────────────────────────
    if st.session_state.no_soal < TOTAL_SOAL:
        h = st.session_state.soal_acak[st.session_state.no_soal]
        
        # HUD Progress Atas
        st.markdown(f"""
            <div class='hud'>
                <span>SOAL {st.session_state.no_soal + 1}/{TOTAL_SOAL}</span>
                <span>WILAYAH: {h['kategori']}</span>
            </div>
            <div class='bar'><i style='width: {((st.session_state.no_soal + 1) / TOTAL_SOAL) * 100}%;'></i></div>
        """, unsafe_allow_html=True)
        
        # Kotak Soal & Kartu Ikon
        st.markdown(f"""
            <div class='pixel-box kartu'>
                <span class='ikon-latar'>{h['latar']}</span>
                <span class='ikon-besar'>{h['ikon']}</span>
                <div class='bisik'>'Seekor hewan langka terpantau di area ini...'</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Tampilan Hasil Jawab (Benar / Salah dengan Reaksi Emoji)
        if st.session_state.status_jawab == 'benar':
            st.markdown("""
                <div class='pixel-box hijau'>
                    <div class='reaksi'>🎉😃🎉</div>
                    <div class='teks-reaksi'>JAWABAN BENAR! LUAR BIASA!</div>
                </div>
            """, unsafe_allow_html=True)
            st.success(f"**Fakta Unik Hutan:** {st.session_state.fakta_sekarang}")
            if st.button("➡️ Lanjut ke Soal Berikutnya", type="primary", use_container_width=True):
                st.session_state.status_jawab = None
                st.session_state.no_soal += 1
                st.rerun()
                
        elif st.session_state.status_jawab == 'salah':
            st.markdown("""
                <div class='pixel-box merah'>
                    <div class='reaksi'>😭👎❌</div>
                    <div class='teks-reaksi'>KURANG TEPAT, EXPLORER!</div>
                </div>
            """, unsafe_allow_html=True)
            st.error(random.choice(RATAPAN))
            if st.button("🔄 Coba Tebak Lagi", type="primary", use_container_width=True):
                st.session_state.status_jawab = None
                st.rerun()
        else:
            # Petunjuk (Clue) Bertahap
            with st.expander("🔍 Buka Petunjuk 1"):
                st.markdown(f"<div class='clue'>✨ {h['clues'][0]}</div>", unsafe_allow_html=True)
            with st.expander("🔍 Buka Petunjuk 2"):
                st.markdown(f"<div class='clue'>🌿 {h['clues'][1]}</div>", unsafe_allow_html=True)
            with st.expander("🎯 Buka Petunjuk Spesifik Wilayah"):
                st.markdown(f"<div class='clue'>🗺️ {h['clues'][2]}</div>", unsafe_allow_html=True)
                
            # Form Input Tebakan
            with st.form(key=f"form_soal_{st.session_state.no_soal}", clear_on_submit=False):
                jawaban = st.text_input("Ketik tebakan nama hewan:", placeholder="Contoh: komodo, anoa...")
                col1, col2 = st.columns(2)
                with col1:
                    submit = st.form_submit_button("⚔️ Konfirmasi", type="primary", use_container_width=True)
                with col2:
                    lewat = st.form_submit_button("🏳️ Lewati", use_container_width=True)
                
                if submit:
                    tebakan_bersih = re.sub(r'[^a-z0-9\s]', '', jawaban.lower().strip())
                    nama_bersih = re.sub(r'[^a-z0-9\s]', '', h['nama'].lower())
                    alias_bersih = [re.sub(r'[^a-z0-9\s]', '', a.lower()) for a in h['alias']]
                    
                    if tebakan_bersih == nama_bersih or tebakan_bersih in alias_bersih:
                        st.session_state.skor += POIN_PER_SOAL
                        st.session_state.status_jawab = 'benar'
                        st.session_state.fakta_sekarang = h['fakta']
                        st.rerun()
                    else:
                        st.session_state.status_jawab = 'salah'
                        st.rerun()
                        
                if lewat:
                    st.warning(f"Kamu melewatkan soal ini! Jawabannya adalah **{h['nama'].capitalize()}**.")
                    st.session_state.no_soal += 1
                    st.rerun()
    else:
        # ─────────────────────────────────────────────────────────────
        # HALAMAN AKHIR & MUSEUM MINI
        # ─────────────────────────────────────────────────────────────
        st.balloons()
        st.markdown("<h2 class='judul'>🏆 EKSPEDISI HUTAN SELESAI 🏆</h2>", unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class='pixel-box emas'>
                <p style='margin: 0; font-size: 1.3rem;'>Total Perolehan Nilai Akhir:</p>
                <div style='font-family: "Press Start 2P"; font-size: 2.2rem; color: #facc15; margin: 8px 0;'>{st.session_state.skor} / {SKOR_MAKS}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Penentuan Gelar Kustom Sesuai Permintaanmu
        if st.session_state.skor >= 90:
            st.markdown("<div class='gelar'>S.Hwn</div>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #86efac;'>Predikat: Ahli Zoologi Nusantara Sejati (Luar Biasa!)</p>", unsafe_allow_html=True)
        elif st.session_state.skor >= 60:
            st.markdown("<div class='gelar'>S.k</div>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #86efac;'>Predikat: Penjelajah Margasatwa Indonesia (Hebat!)</p>", unsafe_allow_html=True)
        elif st.session_state.skor >= 30:
            st.markdown("<div class='gelar'>S.Tda</div>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #86efac;'>Predikat: Pengamat Alam Pemula (Cukup)</p>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='gelar' style='color: #f87171;'>ADOHHHHH, heran</div>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #fca5a5;'>Predikat: Tersesat di Hutan (Ayo Ujian Ulang!)</p>", unsafe_allow_html=True)
            
        st.divider()
        st.markdown("<h3 style='text-align: center;'>🏛️ Museum Mini Ensiklopedia Fauna</h3>", unsafe_allow_html=True)
        st.write("Pelajari kembali fakta unik dari ke-10 hewan endemik:")
        
        for i, item in enumerate(daftar_hewan):
            with st.expander(f"🌲 {i+1}. {item['nama'].capitalize()} ({item['kategori']})"):
                st.markdown(f"### {item['ikon']} {item['nama'].capitalize()}")
                st.write(f"**Fakta Unik:** {item['fakta']}")
                
        st.divider()
        if st.button("🔄 Ujian Ulang (Acak Soal Baru)", type="primary", use_container_width=True):
            st.session_state.skor = 0
            st.session_state.no_soal = 0
            st.session_state.status_jawab = None
            st.session_state.soal_acak = random.sample(daftar_hewan, len(daftar_hewan))
            st.rerun()
