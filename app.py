import streamlit as st
import time

# Konfigurasi Halaman Web
st.set_page_config(page_title="RareFauna Quiz & Museum", page_icon="🌍", layout="centered")

# 1. Database 10 Hewan Langka Lengkap dengan Fakta Ensiklopedia
hewan_langka = [
    {
        "nama": "axolotl", 
        "kategori": "Amfibi / Salamander Meksiko", 
        "clues": ["✨ Clue 1: Saya sering dijuluki 'ikan berjalan', padahal amfibi.", "🌸 Clue 2: Punya insang luar bentuk bulu merah muda di kepala.", "🇲🇽 Clue 3: Endemik dari danau dekat Kota Meksiko."],
        "fakta": "Axolotl memiliki kemampuan regenerasi tubuh yang luar biasa; mereka bisa menumbuhkan kembali kaki, tulang ekor, hingga bagian jantung yang rusak!"
    },
    {
        "nama": "quokka", 
        "kategori": "Mamalia Berkantung (Marsupial)", 
        "clues": ["🌿 Clue 1: Mamalia herbivora kecil dari keluarga kanguru.", "📸 Clue 2: Wajah saya selalu terlihat tersenyum.", "🏝️ Clue 3: Ditemukan di Pulau Rottnest, Australia."],
        "fakta": "Quokka dikenal sebagai 'hewan paling bahagia di dunia' karena bentuk mulutnya yang natural selalu menyerupai senyuman ramah."
    },
    {
        "nama": "pangolin", 
        "kategori": "Mamalia Bersisik", 
        "clues": ["🛡️ Clue 1: Tubuh saya diselimuti sisik keras dari keratin.", "🐜 Clue 2: Lidah saya sangat panjang dan lengket.", "⚠️ Clue 3: Hewan paling banyak diperdagangkan ilegal di dunia."],
        "fakta": "Saat merasa terancam, pangolin akan menggulungkan tubuhnya menjadi bola sisik yang sangat keras seperti buah pinus berduri."
    },
    {
        "nama": "narwhal", 
        "kategori": "Mamalia Laut Kutub", 
        "clues": ["🦄 Clue 1: Sering dijuluki sebagai 'unicorn laut'.", "❄️ Clue 2: Hidup di perairan dingin Arktik / Kutub Utara.", "🦷 Clue 3: 'Tanduk' saya sebenarnya adalah gigi taring kiri."],
        "fakta": "Gigi taring panjang narwhal bisa tumbuh hingga sepanjang 3 meter dan dipenuhi oleh jutaan ujung saraf sensorik untuk mendeteksi perubahan air."
    },
    {
        "nama": "aye-aye", 
        "kategori": "Primata / Lemur Langka", 
        "clues": ["🌙 Clue 1: Primata nokturnal berkerabat dengan lemur.", "🦇 Clue 2: Telinga besar seperti kelelawar.", "🇲🇬 Clue 3: Jari tengah sangat panjang, berasal dari Madagaskar."],
        "fakta": "Aye-aye mencari makan menggunakan teknik 'echolocation' mengetuk kayu pohon dengan jari tengahnya yang panjang untuk mendengarkan larva serangga di dalam."
    },
    {
        "nama": "tarsius", 
        "kategori": "Primata Mungil", 
        "clues": ["👀 Clue 1: Primata terkecil, matanya lebih besar dari otaknya.", "🔄 Clue 2: Bisa memutar kepala hingga 180 derajat.", "🇮🇩 Clue 3: Spesiesnya ada di hutan Sulawesi, Indonesia."],
        "fakta": "Karena bola matanya yang besar dan menetap di tempat, tarsius harus memutar seluruh kepalanya untuk melihat ke arah samping atau belakang."
    },
    {
        "nama": "saola", 
        "kategori": "Mamalia Terancam Punah", 
        "clues": ["🌲 Clue 1: Dijuluki sebagai 'Unicorn Asia' karena misterius.", "🦌 Clue 2: Mirip gabungan kambing dan antelop dengan 2 tanduk.", "🇻🇳 Clue 3: Habitat di Pegunungan Annamite (Vietnam-Laos)."],
        "fakta": "Saola adalah salah satu mamalia besar yang paling langka dan jarang sekali terlihat langsung oleh manusia di alam liar sejak pertama kali ditemukan."
    },
    {
        "nama": "kakapo", 
        "kategori": "Burung Nuri Unik", 
        "clues": ["🦉 Clue 1: Satu-satunya burung nuri yang tidak bisa terbang.", "💤 Clue 2: Aktif malam hari dan tubuhnya harum.", "🇳🇿 Clue 3: Terancam punah, endemik Selandia Baru."],
        "fakta": "Kakapo adalah burung nuri terberat di dunia, berumur sangat panjang (bisa puluhan tahun), dan mengeluarkan aroma tubuh harum seperti wangi madu/lumut."
    },
    {
        "nama": "fossa", 
        "kategori": "Karnivora Unik", 
        "clues": ["🐈 Clue 1: Mirip perpaduan kucing besar, musang, dan anjing.", "🌳 Clue 2: Punya ekor panjang untuk lompat antar pohon.", "🇲🇬 Clue 3: Predator utama lemur di Madagaskar."],
        "fakta": "Fossa memiliki telapak kaki semi-retraktil yang fleksibel, membuat mereka sangat ahli memanjat pohon dan melompat di hutan Madagaskar."
    },
    {
        "nama": "blobfish", 
        "kategori": "Ikan Laut Dalam", 
        "clues": ["🌊 Clue 1: Hidup di laut dalam yang sangat gelap dan tekanan tinggi.", "🍮 Clue 2: Tubuhnya seperti massa agar-agar.", "🏆 Clue 3: Pernah dinobatkan sebagai hewan paling jelek."],
        "fakta": "Tubuh blobfish tidak memiliki otot padat dan lebih ringan dari air, sehingga ia bisa melayang pasif di dasar laut dalam tanpa mengeluarkan banyak energi."
    }
]

# 2. Pengaturan Memori Sesi (Session State)
if 'skor' not in st.session_state: st.session_state.skor = 0
if 'no_soal' not in st.session_state: st.session_state.no_soal = 0
if 'nama_pemain' not in st.session_state: st.session_state.nama_pemain = ""

# 3. Halaman Login / Pendaftaran Pemain
if st.session_state.nama_pemain == "":
    st.title("🌍 RAREFAUNA QUIZ & MUSEUM 🌍")
    st.write("Selamat datang di Ekspedisi Pelindung Alam!")
    st.info("💡 Uji wawasanmu menebak hewan-hewan paling unik dan langka di bumi.")
    
    nama = st.text_input("Siapa nama panggilanmu, Explorer?")
    if st.button("Mulai Petualangan!", use_container_width=True):
        if nama:
            st.session_state.nama_pemain = nama
            st.rerun()
        else:
            st.warning("Tulis namamu dulu ya sebelum mulai penjelajahan!")

# 4. Halaman Kuis Utama
else:
    # --- SIDEBAR (Panel Samping Progres) ---
    with st.sidebar:
        st.header(f"Halo, {st.session_state.nama_pemain}! 🤠")
        st.metric("Skor Saat Ini", f"{st.session_state.skor} Poin")
        
        st.write("Progres Ekspedisi:")
        progress_bar = st.session_state.no_soal / len(hewan_langka)
        st.progress(progress_bar)
        st.caption(f"Soal ke-{st.session_state.no_soal + 1} dari {len(hewan_langka)}")

    # --- KONTEN SOAL ---
    if st.session_state.no_soal < len(hewan_langka):
        hewan = hewan_langka[st.session_state.no_soal]
        
        st.title(f"Soal No. {st.session_state.no_soal + 1}")
        st.subheader(f"Kategori: {hewan['kategori']}")
        st.divider()
        
        # Fitur Clue Buka-Tutup Interaktif
        st.write("🔍 **Buka petunjuk di bawah ini jika kamu butuh bantuan:**")
        with st.expander("✨ Buka Clue 1"): st.info(hewan['clues'][0])
        with st.expander("🌸 Buka Clue 2"): st.info(hewan['clues'][1])
        with st.expander("🗺️ Buka Clue 3 (Paling Spesifik)"): st.info(hewan['clues'][2])
        
        jawaban = st.text_input("Ketik tebakan nama hewan di sini:", key=f"jawab_{st.session_state.no_soal}")
        
        kolom1, kolom2 = st.columns(2)
        with kolom1:
            if st.button("Kirim Jawaban", use_container_width=True):
                if jawaban.lower().strip() == hewan['nama']:
                    st.success(f"✅ BENAR! Jawabannya adalah **{hewan['nama'].capitalize()}**.")
                    st.session_state.skor += 10
                    st.session_state.no_soal += 1
                    time.sleep(1.2)
                    st.rerun()
                else:
                    st.error("❌ Kurang tepat! Coba pikirkan lagi atau buka clue tambahan.")
                    
        with kolom2:
            if st.button("Nyerah & Lewati 🏳️", use_container_width=True):
                st.warning(f"Sayang sekali! Hewan di soal ini adalah **{hewan['nama'].capitalize()}**.")
                st.session_state.no_soal += 1
                time.sleep(1.8)
                st.rerun()

    # --- HALAMAN SELESAI & GALERI ENSIKLOPEDIA ---
    else:
        st.balloons()
        st.success("🎉 SELAMAT! EKSPEDISI SELESAI 🎉")
        st.header(f"Kerja hebat, {st.session_state.nama_pemain}!")
        st.subheader(f"Total Skormu: {st.session_state.skor} dari 100 Poin")
        
        # Sistem Penilaian Gelar / Badge Explorer
        if st.
