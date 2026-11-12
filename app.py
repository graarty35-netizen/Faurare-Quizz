import base64
import html
import random
import re
import streamlit as st

# ─────────────────────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RareFauna Retro Quiz",
    page_icon="🌲",
    layout="centered",
    initial_sidebar_state="collapsed",
)

POIN_PER_SOAL = 10

# ─────────────────────────────────────────────────────────────
# DATABASE 3 KARAKTER & 10 HEWAN ENDEMIK
# ─────────────────────────────────────────────────────────────
daftar_karakter = {
    "Red (Ranger Hutan)": {
        "deskripsi": "Ahli bertahan hidup di rimba belantara, ditemani bola penangkap hijau.",
        "avatar": "🧑‍🌾",
        "warna_badge": "#22c55e",
        "item": "🟢 Poké-Ball Hijau"
    },
    "Blue (Peneliti Satwa)": {
        "deskripsi": "Ilmuwan muda pengamat burung dan primata langka Nusantara.",
        "avatar": "🧑‍🔬",
        "warna_badge": "#3b82f6",
        "item": "🔵 Poké-Ball Biru"
    },
    "Leaf (Penjelajah Rimba)": {
        "deskripsi": "Pencinta reptil purba dan penjelajah gua misterius.",
        "avatar": "🧝‍♀️",
        "warna_badge": "#eab308",
        "item": "🔴 Poké-Ball Merah"
    }
}

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
     "fakta": "Badak jawa menyukai kubangan lumpur di hutan hujan untuk mendinginkan tubuh mereka."},
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

RATAPAN = [
    "Waduh, karakter pixel-mu tersandung akar pohon!",
    "Salah! Ada suara aneh dari semak-semak...",
    "Aduh! Kamu salah jalan di tengah hutan gelap!",
    "Bukan itu! Hewannya mengintip dan menggeleng...",
    "Yah, tebakanmu meleset! Coba buka petunjuk dulu.",
]

# ─────────────────────────────────────────────────────────────
# CSS KUSTOM — ELEGAN DAN BERSIH
# ─────────────────────────────────────────────────────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');

html, body, .stApp, p, label, li, span, div, input, textarea, button {
    font-family: 'VT323', monospace;
}
.stApp p, .stApp li, .stApp label, [data-testid="stMarkdownContainer"] { font-size: 1.4rem; line-height: 1.3; }
h1, h2, h3, .judul, .stButton button, [data-testid="stFormSubmitButton"] button {
    font-family: 'Press Start 2P', monospace !important;
}

.stApp {
    background: linear-gradient(135deg, #03080f 0%, #081424 50%, #030f0b 100%);
    color: #e2f8ec;
}

[data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu, footer {
    display: none !important;
}

.block-container { position: relative; z-index: 2; max-width: 620px; padding-top: 1.5rem; padding-bottom: 60px; }

/* Tombol Musik Minimalis di Pojok Kanan Atas */
.music-toggle {
    position: fixed;
    top: 12px;
    right: 12px;
    z-index: 99999;
    background: rgba(10, 25, 18, 0.95);
    border: 2px solid #22c55e;
    padding: 4px 8px;
    border-radius: 4px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.6);
}
.music-toggle audio { height: 24px; width: 105px; }

.game-header {
    background: rgba(4, 16, 11, 0.9);
    border: 3px solid #22c55e;
    border-radius: 6px;
    padding: 10px;
    text-align: center;
    margin-bottom: 16px;
    box-shadow: 4px 4px 0px rgba(0,0,0,0.5);
}

.pixel-box {
    background: rgba(5, 20, 14, 0.85);
    backdrop-filter: blur(6px);
    border: 3px solid #22c55e;
    box-shadow: 5px 5px 0px rgba(0, 0, 0, 0.6);
    padding: 20px 16px;
    margin: 6px 0 16px;
    text-align: center;
    border-radius: 6px;
}
.pixel-box.emas { border-color: #facc15; }
.pixel-box.hijau { border-color: #4ade80; background: rgba(20, 83, 45, 0.25); }
.pixel-box.merah { border-color: #f87171; background: rgba(127, 29, 29, 0.3); }

.judul {
    text-align: center; color: #facc15 !important; line-height: 1.5;
    font-size: clamp(1.1rem, 4.5vw, 1.5rem); text-shadow: 2px 2px 0 #78350f;
    margin: 0 0 8px 0;
}

.ikon-besar {
    display: block; font-size: clamp(65px, 18vw, 95px); line-height: 1.1; margin: 6px 0;
    filter: drop-shadow(3px 3px 0 rgba(0, 0, 0, 0.5));
}
.bisik { font-size: 1.3rem; font-style: italic; color: #bef264; margin-top: 4px; }

.clue {
    background: rgba(250, 204, 21, 0.08); border-left: 4px solid #facc15;
    padding: 6px 10px; margin: 6px 0; font-size: 1.3rem;
}

.reaksi { font-size: clamp(2rem, 9vw, 3.2rem); letter-spacing: 4px; margin-bottom: 4px; }
.teks-reaksi { font-family: 'Press Start 2P', monospace; font-size: clamp(0.5rem, 2.2vw, 0.7rem); line-height: 1.5; margin-bottom: 6px; }

.gelar {
    text-align: center; font-family: 'Press Start 2P', monospace; color: #facc15;
    font-size: clamp(1rem, 5vw, 2rem); text-shadow: 3px 3px 0 #78350f; margin: 8px 0; line-height: 1.4;
}

.stButton > button, [data-testid="stFormSubmitButton"] > button {
    min-height: 3rem; border-radius: 4px; border: 3px solid #022c14; color: #052e16;
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

.stTextInput input {
    min-height: 3rem; border-radius: 4px !important; font-size: 1.5rem;
    background: #020a06 !important; color: #f0fdf4 !important; border: 3px solid #22c55e !important;
}
.stTextInput input::placeholder { color: #6ee7b7 !important; opacity: 0.6; }
.stTextInput input:focus { border-color: #facc15 !important; box-shadow: 0 0 6px rgba(250,204,21,0.4) !important; }
[data-testid="stForm"] { background: rgba(3, 15, 10, 0.85); border: 3px solid #22c55e; border-radius: 6px; padding: 10px; }
[data-testid="stExpander"] { background: rgba(3, 15, 10, 0.85); border: 2px solid #22c55e; border-radius: 4px; }
hr { border-color: rgba(74, 222, 128, 0.25) !important; }
"""

# ─────────────────────────────────────────────────────────────
# STATE AWAL & LOGIKA APLIKASI
# ─────────────────────────────────────────────────────────────
if 'skor' not in st.session_state: st.session_state.skor = 0
if 'no_soal' not in st.session_state: st.session_state.no_soal = 0
if 'nama_pemain' not in st.session_state: st.session_state.nama_pemain = ""
if 'karakter_pilihan' not in st.session_state: st.session_state.karakter_pilihan = None
if 'status_jawab' not in st.session_state: st.session_state.status_jawab = None
if 'fakta_sekarang' not in st.session_state: st.session_state.fakta_sekarang = ""
if 'soal_acak' not in st.session_state: 
    st.session_state.soal_acak = random.sample(daftar_hewan, len(daftar_hewan))

st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

# Pemutar Musik Minimalis di Pojok Kanan Atas
st.markdown("""
    <div class="music-toggle">
        <audio controls loop preload="auto">
            <source src="https://cdn.pixabay.com/download/audio/2022/03/15/audio_c8c325e648.mp3?filename=game-level-music-143026.mp3" type="audio/mpeg">
        </audio>
    </div>
""", unsafe_allow_html=True)

# Header Game Bersih
st.markdown("""
    <div class="game-header">
        <span style="font-size: 24px;">🌲 🇮🇩 🌲</span>
        <div style="font-family: 'Press Start 2P'; font-size: 0.75rem; color: #4ade80; margin-top: 4px;">RAREFAUNA RETRO QUIZ</div>
    </div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# TAHAP 1: HALAMAN LOGIN & PEMILIHAN KARAKTER (3 PILIHAN)
# ─────────────────────────────────────────────────────────────
if st.session_state.nama_pemain == "" or st.session_state.karakter_pilihan is None:
    st.markdown("<h1 class='judul'>PILIH KARAKTERMU!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #a7d7b5; font-size: 1.15rem; margin-bottom: 14px;'>Pilih jagoan petualangmu sebelum masuk ke dalam hutan rimba.</p>", unsafe_allow_html=True)
    
    nama_input = st.text_input("Nama Panggilan Explorer:", placeholder="Ketik namamu...")
    
    st.markdown("### 👥 Pilih Trainer & Partner Satwa:")
    
    # Menampilkan 3 pilihan karakter berdampingan (ala pemilihan hero/karakter game)
    c1, c2, c3 = st.columns(3)
    
    pilihan = None
    with c1:
        st.markdown(f"""
            <div style="background: rgba(4,16,11,0.9); border: 2px solid #22c55e; border-radius: 6px; padding: 12px; text-align: center;">
                <div style="font-size: 50px;">🧑‍🌾</div>
                <div style="font-family: 'Press Start 2P'; font-size: 0.55rem; color: #4ade80; margin: 6px 0;">Red</div>
                <div style="font-size: 0.95rem; color: #cbd5e1;">Ranger Hutan<br>🟢 Poké-Ball Hijau</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Pilih Red", key="btn_red", use_container_width=True):
            pilihan = "Red (Ranger Hutan)"
            
    with c2:
        st.markdown(f"""
            <div style="background: rgba(4,16,11,0.9); border: 2px solid #3b82f6; border-radius: 6px; padding: 12px; text-align: center;">
                <div style="font-size: 50px;">🧑‍🔬</div>
                <div style="font-family: 'Press Start 2P'; font-size: 0.55rem; color: #3b82f6; margin: 6px 0;">Blue</div>
                <div style="font-size: 0.95rem; color: #cbd5e1;">Peneliti<br>🔵 Poké-Ball Biru</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Pilih Blue", key="btn_blue", use_container_width=True):
            pilihan = "Blue (Peneliti Satwa)"
            
    with c3:
        st.markdown(f"""
            <div style="background: rgba(4,16,11,0.9); border: 2px solid #eab308; border-radius: 6px; padding: 12px; text-align: center;">
                <div style="font-size: 50px;">🧝‍♀️</div>
                <div style="font-family: 'Press Start 2P'; font-size: 0.55rem; color: #eab308; margin: 6px 0;">Leaf</div>
                <div style="font-size: 0.95rem; color: #cbd5e1;">Penjelajah<br>🔴 Poké-Ball Merah</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Pilih Leaf", key="btn_leaf", use_container_width=True):
            pilihan = "Leaf (Penjelajah Rimba)"

    if pilihan:
        if nama_input.strip():
            st.session_state.nama_pemain = nama_input.strip()
            st.session_state.karakter_pilihan = pilihan
            st.session_state.status_jawab = None
            st.session_state.soal_acak = random.sample(daftar_hewan, len(daftar_hewan))
            st.rerun()
        else:
            st.warning("⚠️ Masukkan nama panggilanmu terlebih dahulu di atas sebelum memilih karakter!")

else:
    # ─────────────────────────────────────────────────────────────
    # TAHAP 2: AREA PERMAINAN UTAMA (MENAMPILKAN KARAKTER TERPILIH)
    # ─────────────────────────────────────────────────────────────
    char_info = daftar_karakter[st.session_state.karakter_pilihan]
    
    if st.session_state.no_soal < TOTAL_SOAL:
        h = st.session_state.soal_acak[st.session_state.no_soal]
        
        # Bar Informasi Profil Karakter & Progress Soal di Atas
        st.markdown(f"""
            <div style="background: rgba(5,20,14,0.7); border: 2px solid {char_info['warna_badge']}; border-radius: 6px; padding: 8px 12px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="font-size: 24px; vertical-align: middle;">{char_info['avatar']}</span>
                    <span style="font-family: 'Press Start 2P'; font-size: 0.55rem; color: {char_info['warna_badge']}; margin-left: 6px;">{st.session_state.nama_pemain} ({st.session_state.karakter_pilihan.split()[0]})</span>
                </div>
                <div style="text-align: right; font-size: 0.95rem;">
                    🎯 <b>{st.session_state.no_soal + 1}/{TOTAL_SOAL}</b> | 🏆 <b>{st.session_state.skor} Poin</b>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Kotak Soal & Kartu Ikon Hewan
        st.markdown(f"""
            <div class='pixel-box'>
                <div style='font-family: "Press Start 2P"; font-size: 0.6rem; color: #facc15; margin-bottom: 6px;'>WILAYAH: {h['kategori']}</div>
                <span style='font-size: 35px; position: absolute; right: 18px; top: 16px;'>{h['latar']}</span>
                <span class='ikon-besar'>{h['ikon']}</span>
                <div class='bisik'>'{char_info['item']} bersiap! Hewan misterius mengintip di dekatmu...'</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Tampilan Hasil Jawab (Benar / Salah)
        if st.session_state.status_jawab == 'benar':
            st.markdown(f"""
                <div class='pixel-box hijau'>
                    <div class='reaksi'>🎉 {char_info['avatar']} 😃 🎉</div>
                    <div class='teks-reaksi'>BERHASIL DITANGKAP & DIKENALI! LUAR BIASA!</div>
                </div>
            """, unsafe_allow_html=True)
            st.success(f"**Fakta Unik Hutan:** {st.session_state.fakta_sekarang}")
            if st.button("➡️ Lanjut ke Soal Berikutnya", type="primary", use_container_width=True):
                st.session_state.status_jawab = None
                st.session_state.no_soal += 1
                st.rerun()
                
        elif st.session_state.status_jawab == 'salah':
            st.markdown(f"""
                <div class='pixel-box merah'>
                    <div class='reaksi'>😭 {char_info['avatar']} 👎 ❌</div>
                    <div class='teks-reaksi'>MELARIKAN DIRI! TEBAKANMU SALAH.</div>
                </div>
            """, unsafe_allow_html=True)
            st.error(random.choice(RATAPAN))
            if st.button("🔄 Coba Tebak Lagi", type="primary", use_container_width=True):
                st.session_state.status_jawab = None
                st.rerun()
        else:
            with st.expander("🔍 Buka Petunjuk 1"):
                st.markdown(f"<div class='clue'>✨ {h['clues'][0]}</div>", unsafe_allow_html=True)
            with st.expander("🔍 Buka Petunjuk 2"):
                st.markdown(f"<div class='clue'>🌿 {h['clues'][1]}</div>", unsafe_allow_html=True)
            with st.expander("🎯 Buka Petunjuk Spesifik Wilayah"):
                st.markdown(f"<div class='clue'>🗺️ {h['clues'][2]}</div>", unsafe_allow_html=True)
                
            with st.form(key=f"form_soal_{st.session_state.no_soal}", clear_on_submit=False):
                jawaban = st.text_input("Ketik tebakan nama hewan:", placeholder="Contoh: komodo, anoa...")
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    submit = st.form_submit_button(f"⚔️ Tangkap / Tebak", type="primary", use_container_width=True)
                with col_btn2:
                    lewat = st.form_submit_button("🏳️ Kabur", use_container_width=True)
                
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
                    st.warning(f"Kamu kabur! Jawabannya adalah **{h['nama'].capitalize()}**.")
                    st.session_state.no_soal += 1
                    st.rerun()
    else:
        # ─────────────────────────────────────────────────────────────
        # HALAMAN AKHIR & MUSEUM MINI
        # ─────────────────────────────────────────────────────────────
        st.balloons()
        st.markdown(f"<h2 class='judul'>🏆 EKSPEDISI {st.session_state.karakter_pilihan.split()[0].upper()} SELESAI 🏆</h2>", unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class='pixel-box emas'>
                <p style='margin: 0; font-size: 1.2rem;'>Total Perolehan Nilai Akhir ({st.session_state.nama_pemain}):</p>
                <div style='font-family: "Press Start 2P"; font-size: 2rem; color: #facc15; margin: 6px 0;'>{st.session_state.skor} / {SKOR_MAKS}</div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.skor >= 90:
            st.markdown("<div class='gelar'>S.Hwn</div>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #86efac;'>Predikat: Master Trainer & Ahli Zoologi Nusantara (Luar Biasa!)</p>", unsafe_allow_html=True)
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
        st.markdown("<h3 style='text-align: center;'>🏛️ Museum Mini Ensiklopedia</h3>", unsafe_allow_html=True)
        
        for i, item in enumerate(daftar_hewan):
            with st.expander(f"🌲 {i+1}. {item['nama'].capitalize()} ({item['kategori']})"):
                st.markdown(f"### {item['ikon']} {item['nama'].capitalize()}")
                st.write(f"**Fakta Unik:** {item['fakta']}")
                
        st.divider()
        if st.button("🔄 Ganti Karakter & Ujian Ulang", type="primary", use_container_width=True):
            st.session_state.skor = 0
            st.session_state.no_soal = 0
            st.session_state.nama_pemain = ""
            st.session_state.karakter_pilihan = None
            st.session_state.status_jawab = None
            st.session_state.soal_acak = random.sample(daftar_hewan, len(daftar_hewan))
            st.rerun()
