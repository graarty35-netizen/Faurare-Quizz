import streamlit as st
import time

# Konfigurasi Halaman Web
st.set_page_config(page_title="RareFauna Quiz & Museum", page_icon="🌍", layout="centered")

# 1. Database 10 Hewan Langka Lengkap dengan Foto, Fakta, & Clue
hewan_langka = [
    {
        "nama": "axolotl", 
        "kategori": "Amfibi / Salamander Meksiko", 
        "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Axolotl_ticla.jpg/800px-Axolotl_ticla.jpg",
        "clues": ["✨ Clue 1: Saya sering dijuluki 'ikan berjalan', padahal amfibi.", "🌸 Clue 2: Punya insang luar bentuk bulu merah muda di kepala.", "🇲🇽 Clue 3: Endemik dari danau dekat Kota Meksiko."],
        "fakta": "Axolotl memiliki kemampuan regenerasi tubuh yang luar biasa; mereka bisa menumbuhkan kembali kaki, tulang ekor, hingga bagian jantung yang rusak!"
    },
    {
        "nama": "quokka", 
        "kategori": "Mamalia Berkantung (Marsupial)", 
        "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Quokka_%28Setonix_brachyurus%29%2C_Rottnest_Island%2C_Western_Australia.jpg/800px-Quokka_%28Setonix_brachyurus%29%2C_Rottnest_Island%2C_Western_Australia.jpg",
        "clues": ["🌿 Clue 1: Mamalia herbivora kecil dari keluarga kanguru.", "📸 Clue 2: Wajah saya selalu terlihat tersenyum.", "🏝️ Clue 3: Ditemukan di Pulau Rottnest, Australia."],
        "fakta": "Quokka dikenal sebagai 'hewan paling bahagia di dunia' karena bentuk mulutnya yang natural selalu menyerupai senyuman ramah."
    },
    {
        "nama": "pangolin", 
        "kategori": "Mamalia Bersisik", 
        "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Pangolin_%28Manis_javanica%29_by_David_Baskin.jpg/800px-Pangolin_%28Manis_javanica%29_by_David_Baskin.jpg",
        "clues": ["🛡️ Clue 1: Tubuh saya diselimuti sisik keras dari keratin.", "🐜 Clue 2: Lidah saya sangat panjang dan lengket.", "⚠️ Clue 3: Hewan paling banyak diperdagangkan ilegal di dunia."],
        "fakta": "Saat merasa terancam, pangolin akan menggulungkan tubuhnya menjadi bola sisik yang sangat keras seperti buah pinus berduri."
    },
    {
        "nama": "narwhal", 
        "kategori": "Mamalia Laut Kutub", 
        "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Narwhal_breaching.jpg/800px-Narwhal_breaching.jpg",
        "clues": ["🦄 Clue 1: Sering dijuluki sebagai 'unicorn laut'.", "❄️ Clue 2: Hidup di perairan dingin Arktik / Kutub Utara.", "🦷 Clue 3: 'Tanduk' saya sebenarnya adalah gigi taring kiri."],
        "fakta": "Gigi taring panjang narwhal bisa tumbuh hingga sepanjang 3 meter dan dipenuhi oleh jutaan ujung saraf sensorik untuk mendeteksi perubahan air."
    },
    {
        "nama": "aye-aye", 
        "kategori": "Primata / Lemur Langka", 
        "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Aye-aye_%28Daubentonia_madagascariensis%29_Zoo_Londres.jpg/800px-Aye-aye_%28Daubentonia_madagascariensis%29_Zoo_Londres.jpg",
        "clues": ["🌙 Clue 1: Primata nokturnal berkerabat dengan lemur.", "🦇 Clue 2: Telinga besar seperti kelelawar.", "🇲🇬 Clue 3: Jari tengah sangat panjang, berasal dari Madagaskar."],
        "fakta": "Aye-aye mencari makan menggunakan teknik 'echolocation' mengetuk kayu pohon dengan jari tengahnya yang panjang untuk mendengarkan larva serangga di dalam."
    },
    {
        "nama": "tarsius", 
        "kategori": "Primata Mungil", 
        "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Tarsius_tarsier_Yaki.jpg/800px-Tarsius_tarsier_Yaki.jpg",
        "clues": ["👀 Clue 1: Primata terkecil, matanya lebih besar dari otaknya.", "🔄 Clue 2: Bisa memutar kepala hingga 180 derajat.", "🇮🇩 Clue 3: Spesiesnya ada di hutan Sulawesi, Indonesia."],
        "fakta": "Karena bola matanya yang besar dan menetap di tempat, tarsius harus memutar seluruh kepalanya untuk melihat ke arah samping atau belakang."
    },
    {
        "nama": "saola", 
        "kategori": "Mamalia Terancam Punah", 
        "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Saola_%28Pseudoryx_nghetinhensis%29_drawing.jpg/800px-Saola_%28Pseudoryx_nghetinhensis%29_drawing.jpg",
        "clues": ["🌲 Clue 1: Dijuluki sebagai 'Unicorn Asia' karena misterius.", "🦌 Clue 2: Mirip gabungan kambing dan antelop dengan 2 tanduk.", "🇻🇳 Clue 3: Habitat di Pegunungan Annamite (Vietnam-Laos)."],
        "fakta": "Saola adalah salah satu mamalia besar yang paling langka dan jarang sekali terlihat langsung oleh manusia di alam liar sejak pertama kali ditemukan."
    },
    {
        "nama": "kakapo", 
        "kategori": "Burung Nuri Unik", 
        "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Strigops_habroptilus_CC0.jpg/800px-Strigops_habroptilus_CC0.jpg",
        "clues": ["🦉 Clue 1: Satu-satunya burung nuri yang tidak bisa terbang.", "💤 Clue 2: Aktif malam hari dan tubuhnya harum.", "🇳🇿 Clue 3: Terancam punah, endemik Selandia Baru."],
        "fakta": "Kakapo adalah burung nuri terberat di dunia, berumur sangat panjang (bisa puluhan tahun), dan mengeluarkan aroma tubuh harum seperti wangi madu/lumut."
    },
    {
        "nama": "fossa", 
        "kategori": "Karnivora Unik", 
        "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Fossa_%28Cryptoprocta_ferox%29_%2810842211993%29.jpg/800px-Fossa_%28Cryptoprocta_ferox%29_%2810842211993%29.jpg",
        "clues": ["🐈 Clue 1: Mirip perpaduan kucing besar, musang, dan anjing.", "🌳 Clue 2: Punya ekor panjang untuk lompat antar pohon.", "🇲🇬 Clue 3: Predator utama lemur di Madagaskar."],
        "fakta": "Fossa memiliki telapak kaki semi-retraktil yang fleksibel, membuat mereka sangat ahli memanjat pohon dan melompat di hutan Madagaskar."
    },
    {
        "nama": "blobfish", 
        "kategori": "Ikan Laut Dalam", 
        "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Psychrolutes_marcidus.png/800px-Psychrolutes_marcidus.png",
        "clues": ["🌊 Clue 1: Hidup di laut dalam yang sangat gelap dan tekanan tinggi.", "🍮 Clue 2: Tubuhnya seperti massa agar-agar.", "🏆 Clue 3: Pernah dinobatkan sebagai hewan paling jelek."],
        "fakta": "Tubuh blobfish tidak memiliki otot padat dan lebih ringan dari air, sehingga ia bisa melayang pasif di dasar laut dalam tanpa mengeluarkan banyak energi."
    }
]

# 2. Pengaturan Memori Sesi
if 'skor' not in st.session_state: st.session_state.skor = 0
if 'no_soal' not in st.session_state: st.session_state.no_soal = 0
if 'nama_pemain' not in st.session_state: st.session_state.nama_pemain = ""

# 3. Halaman Login
if st.session_state.nama_pemain == "":
    st.title("🌍 RAREFAUNA QUIZ & MUSEUM 🌍")
    st.write("Selamat datang di Ekspedisi Pelindung Alam!")
    st.info("💡 Tebak hewan langka, lihat fotonya, dan buka ensiklopedianya!")
    
    nama = st.text_input("Siapa nama panggilanmu, Explorer?")
    if st.button("Mulai Petualangan!", use_container_width=True):
        if nama:
            st.session_state.nama_pemain = nama
            st.rerun()
        else:
            st.warning("Tulis namamu dulu ya!")

# 4. Halaman Kuis Utama
else:
    # --- SIDEBAR (Panel Samping + Backsound Audio) ---
    with st.sidebar:
        st.header(f"Halo, {st.session_state.nama_pemain}! 🤠")
        st.metric("Skor Saat Ini", f"{st.session_state.skor} Poin")
        
        st.write("Progres Ekspedisi:")
        progress_bar = st.session_state.no_soal / len(hewan_langka)
        st.progress(progress_bar)
        st.caption(f"Soal ke-{st.session_state.no_soal + 1} dari {len(hewan_langka)}")
        
        st.divider()
        st.subheader("🎵 Backsound Suasana Alam")
        # Pemutar Musik Latar (Audio Bebas Hak Cipta / Musik Santai)
        st.audio("https://actions.google.com/sounds/v1/ambiences/forest_birds.ogg", format="audio/ogg")
        st.caption("Putar audio di atas untuk menemani penjelajahanmu!")

    # --- KONTEN SOAL ---
    if st.session_state.no_soal < len(hewan_langka):
        hewan = hewan_langka[st.session_state.no_soal]
        
        st.title(f"Soal No. {st.session_state.no_soal + 1}")
        st.subheader(f"Kategori: {hewan['kategori']}")
        
        # Menampilkan Foto Asli Hewan
        st.image(hewan['foto'], caption=f"Kira-kira hewan apa ini?", use_column_width=True)
        st.divider()
        
        # Fitur Clue Buka-Tutup
        st.write("🔍 **Buka petunjuk di bawah ini jika butuh bantuan:**")
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
                    st.error("❌ Kurang tepat! Coba pikirkan lagi.")
                    
        with kolom2:
            if st.button("Nyerah & Lewati 🏳️", use_container_width=True):
                st.warning(f"Sayang sekali! Hewan ini adalah **{hewan['nama'].capitalize()}**.")
                st.session_state.no_soal += 1
                time.sleep(1.8)
                st.rerun()

    # --- HALAMAN SELESAI & GALERI ENSIKLOPEDIA ---
    else:
        st.balloons()
        st.success("🎉 SELAMAT! EKSPEDISI SELESAI 🎉")
        st.header(f"Kerja hebat, {st.session_state.nama_pemain}!")
        st.subheader(f"Total Skormu: {st.session_state.skor} dari 100 Poin")
        
        # Sistem Gelar / Badge
        if st.session_state.skor >= 90:
            st.markdown("### 🏆 Gelar: **Master Fauna Nusantara & Dunia** (Luar Biasa!)")
        elif st.session_state.skor >= 60:
            st.markdown("### 🥈 Gelar: **Penjelajah Alam Senior** (Hebat & Berwawasan!)")
        elif st.session_state.skor >= 30:
            st.markdown("### 🥉 Gelar: **Pengamat Margasatwa Pemula** (Bagus!)")
        else:
            st.markdown("### 🧭 Gelar: **Turis Hutan Tersesat** (Ayo coba lagi!)")
            
        st.divider()
        st.header("🏛️ Galeri Museum Mini (Ensiklopedia Hewan)")
        st.write("Kenali bentuk dan fakta unik dari ke-10 hewan langka:")
        
        # Galeri Ensiklopedia dengan Gambar & Fakta
        for idx, item in enumerate(hewan_langka):
            with st.expander(f"🐾 {idx+1}. {item['nama'].capitalize()} ({item['kategori']})"):
                st.image(item['foto'], width=300)
                st.write(f"**Fakta Unik:** {item['fakta']}")
                st.markdown(f"*Clue Utama:* {item['clues'][2]}")
        
        st.divider()
        if st.button("Main Lagi dari Awal", use_container_width=True):
            st.session_state.skor = 0
            st.session_state.no_soal = 0
            st.session_state.nama_pemain = ""
            st.rerun()
