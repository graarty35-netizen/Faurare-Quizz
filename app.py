import streamlit as st
import time

# Konfigurasi Halaman Web
st.set_page_config(page_title="RareFauna Quiz: Endemik Indonesia", page_icon="🇮🇩", layout="centered")

# 1. Database 10 Hewan Endemik Asli Indonesia
hewan_langka = [
    {
        "nama": "komodo", 
        "kategori": "Reptil Purba / NTT", 
        "ikon": "🦖🏝️", 
        "clues": ["✨ Clue 1: Reptil terbesar di dunia yang masih hidup.", "🇮🇩 Clue 2: Air liur saya mengandung bakteri dan racun kuat.", "🏝️ Clue 3: Habitat asli hanya di pulau-pulau wilayah Nusa Tenggara Timur."],
        "fakta": "Komodo adalah kadal terbesar di bumi yang panjangnya bisa mencapai 3 meter dengan berat hingga lebih dari 70 kg!"
    },
    {
        "nama": "orangutan", 
        "kategori": "Primata Hutan / Sumatera & Kalimantan", 
        "ikon": "🦧🌴", 
        "clues": ["✨ Clue 1: Nama saya berarti 'manusia hutan' dalam bahasa lokal.", "🟠 Clue 2: Bulu tubuh saya berwarna jingga kecoklatan yang khas.", "🌴 Clue 3: Hewan arboreal yang menghabiskan sebagian besar hidup di atas pohon."],
        "fakta": "Orangutan memiliki tingkat kecerdasan yang tinggi dan mampu menggunakan alat-alat sederhana untuk mencari makan di alam liar."
    },
    {
        "nama": "badak jawa", 
        "kategori": "Mamalia Bercula Satu / Ujung Kulon", 
        "ikon": "🦏🌿", 
        "clues": ["✨ Clue 1: Salah satu mamalia paling langka dan terancam punah di bumi.", "🦄 Clue 2: Hanya memiliki satu cula di bagian hidungnya.", "🌊 Clue 3: Suaka terakhir perlindungan kami ada di Taman Nasional Ujung Kulon."],
        "fakta": "Badak Jawa sangat menyukai kubangan lumpur untuk menjaga suhu tubuh mereka tetap dingin dan melindungi kulit dari sengatan matahari."
    },
    {
        "nama": "harimau sumatera", 
        "kategori": "Karnivora / Pulau Sumatera", 
        "ikon": "🐅🍂", 
        "clues": ["✨ Clue 1: Subspesies harimau terkecil yang masih bertahan hidup.", "🖤 Clue 2: Garis-garis loreng di tubuh saya lebih rapat dan gelap.", "🇮🇩 Clue 3: Merupakan kucing besar satu-satunya yang tersisa di Indonesia."],
        "fakta": "Harimau sumatera adalah perenang yang sangat handal dan sering sengaja berendam di sungai untuk mendinginkan tubuh."
    },
    {
        "nama": "anoa", 
        "kategori": "Mamalia / Sulawesi", 
        "ikon": "🐃⛰️", 
        "clues": ["✨ Clue 1: Sering dijuluki sebagai 'kerbau kerdil' karena ukurannya.", "🛡️ Clue 2: Memiliki sepasang tanduk lurus dan tajam untuk pertahanan diri.", "🇮🇩 Clue 3: Merupakan hewan endemik asli dari pulau Sulawesi."],
        "fakta": "Anoa sangat suka berendam di lumpur layaknya kerbau dan memiliki sifat yang cenderung pemalu serta soliter (menyendiri) di dalam hutan."
    },
    {
        "nama": "cendrawasih", 
        "kategori": "Burung Eksotis / Papua", 
        "ikon": "🦜✨", 
        "clues": ["✨ Clue 1: Terkenal dengan sebutan 'Burung Surga' karena keindahannya.", "🎨 Clue 2: Memiliki bulu ekor panjang yang sangat berwarna-warni dan megah.", "🇮🇩 Clue 3: Habitat utama burung ini berada di hutan hujan Papua."],
        "fakta": "Keindahan bulu burung cendrawasih membuat mereka sering menjadi simbol budaya khas masyarakat tanah Papua."
    },
    {
        "nama": "babirusa", 
        "kategori": "Mamalia Unik / Sulawesi", 
        "ikon": "🐗🦷", 
        "clues": ["✨ Clue 1: Namanya gabungan dari babi dan rusa karena bentuk gigi.", "🦷 Clue 2: Taring atas jantan tumbuh melengkung menembus kulit moncongnya.", "🇮🇩 Clue 3: Habitat aslinya dapat ditemukan di hutan hujan pulau Sulawesi."],
        "fakta": "Taring melengkung pada babirusa jantan bisa terus tumbuh melingkar hingga hampir menyentuh bagian mata mereka jika tidak diasah."
    },
    {
        "nama": "maleo", 
        "kategori": "Burung Unik / Sulawesi", 
        "ikon": "🥚🔥", 
        "clues": ["✨ Clue 1: Burung darat berukuran sedang dengan benjolan khas di kepala.", "🌋 Clue 2: Tidak mengerami telurnya sendiri, melainkan ditimbun di pasir panas.", "🔥 Clue 3: Memanfaatkan panas bumi atau pasir pantai vulkanik untuk menetaskan telur."],
        "fakta": "Anak burung maleo bisa langsung terbang mencari makan sendiri sesaat setelah menetas tanpa harus disuapi oleh induknya."
    },
    {
        "nama": "tarsius", 
        "kategori": "Primata Mungil / Sulawesi", 
        "ikon": "👀🌿", 
        "clues": ["✨ Clue 1: Salah satu primata terkecil di dunia dengan mata besar.", "🔄 Clue 2: Mampu memutar kepalanya hingga 180 derajat ke belakang.", "🇮🇩 Clue 3: Banyak ditemukan melompat di pepohonan hutan Sulawesi."],
        "fakta": "Meskipun bertubuh sangat mungil, tarsius adalah karnivora murni yang memakan serangga kecil hingga kadal pohon."
    },
    {
        "nama": "jalak bali", 
        "kategori": "Burung Khas / Bali", 
        "ikon": "🕊️🌺", 
        "clues": ["✨ Clue 1: Burung pengicau berbulu putih bersih dengan bercak biru di mata.", " crest Clue 2: Memiliki jambul indah di bagian belakang kepalanya.", "🏝️ Clue 3: Merupakan maskot fauna resmi dari pulau Bali."],
        "fakta": "Jalak bali adalah salah satu burung paling dilindungi di dunia karena populasinya di alam liar yang sempat sangat kritis."
    }
]

# 2. Pengaturan Memori Sesi
if 'skor' not in st.session_state: st.session_state.skor = 0
if 'no_soal' not in st.session_state: st.session_state.no_soal = 0
if 'nama_pemain' not in st.session_state: st.session_state.nama_pemain = ""

# 3. Halaman Login
if st.session_state.nama_pemain == "":
    st.title("🇮🇩 KUIS ENDEMIK FAUNA INDONESIA 🇮🇩")
    st.write("Selamat datang di Ekspedisi Kekayaan Satwa Nusantara!")
    st.info("💡 Tebak nama hewan endemik asli Indonesia, buka clue, dan jelajahi museum nusantaranya!")
    
    nama = st.text_input("Siapa nama panggilanmu, Explorer?")
    if st.button("Mulai Ekspedisi Nusantara!", use_container_width=True):
        if nama:
            st.session_state.nama_pemain = nama
            st.rerun()
        else:
            st.warning("Tulis namamu dulu ya!")

# 4. Halaman Kuis Utama
else:
    # --- SIDEBAR (Panel Samping + Backsound) ---
    with st.sidebar:
        st.header(f"Halo, {st.session_state.nama_pemain}! 🇮🇩")
        st.metric("Skor Saat Ini", f"{st.session_state.skor} Poin")
        
        st.write("Progres Ekspedisi:")
        progress_bar = st.session_state.no_soal / len(hewan_langka)
        st.progress(progress_bar)
        st.caption(f"Soal ke-{st.session_state.no_soal + 1} dari {len(hewan_langka)}")
        
        st.divider()
        st.subheader("🎵 Backsound Suasana Alam")
        st.audio("https://actions.google.com/sounds/v1/ambiences/forest_birds.ogg", format="audio/ogg")

    # --- KONTEN SOAL ---
    if st.session_state.no_soal < len(hewan_langka):
        hewan = hewan_langka[st.session_state.no_soal]
        
        st.title(f"Soal No. {st.session_state.no_soal + 1}")
        st.subheader(f"Kategori: {hewan['kategori']}")
        
        # Kotak Visual Ikon Emoji Hewan
        st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{hewan['ikon']}</h1>", unsafe_allow_html=True)
        st.info("👆 Perhatikan kategori wilayah dan ikon di atas, lalu buka clue di bawah jika butuh petunjuk!")
        st.divider()
        
        # Fitur Clue Buka-Tutup
        st.write("🔍 **Buka petunjuk di bawah ini:**")
        with st.expander("✨ Buka Clue 1"): st.write(hewan['clues'][0])
        with st.expander("🇮🇩 Buka Clue 2"): st.write(hewan['clues'][1])
        with st.expander("🗺️ Buka Clue 3 (Paling Spesifik)"): st.write(hewan['clues'][2])
        
        jawaban = st.text_input("Ketik tebakan nama hewan di sini (huruf kecil):", key=f"jawab_{st.session_state.no_soal}")
        
        kolom1, kolom2 = st.columns(2)
        with kolom1:
            if
