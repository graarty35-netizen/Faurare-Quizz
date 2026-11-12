import streamlit as st

# 1. Database 10 Hewan Langka
hewan_langka = [
    {"nama": "axolotl", "kategori": "Amfibi / Salamander Meksiko", "clues": ["✨ Clue 1: Saya sering dijuluki 'ikan berjalan', padahal amfibi.", "🌸 Clue 2: Punya insang luar bentuk bulu merah muda di kepala.", "🇲🇽 Clue 3: Endemik dari danau dekat Kota Meksiko."]},
    {"nama": "quokka", "kategori": "Mamalia Berkantung (Marsupial)", "clues": ["🌿 Clue 1: Mamalia herbivora kecil dari keluarga kanguru.", "📸 Clue 2: Wajah saya selalu terlihat tersenyum.", "🏝️ Clue 3: Ditemukan di Pulau Rottnest, Australia."]},
    {"nama": "pangolin", "kategori": "Mamalia Bersisik", "clues": ["🛡️ Clue 1: Tubuh saya diselimuti sisik keras dari keratin.", "🐜 Clue 2: Lidah saya sangat panjang dan lengket.", "⚠️ Clue 3: Hewan paling banyak diperdagangkan ilegal di dunia."]},
    {"nama": "narwhal", "kategori": "Mamalia Laut Kutub", "clues": ["🦄 Clue 1: Sering dijuluki sebagai 'unicorn laut'.", "❄️ Clue 2: Hidup di perairan dingin Arktik / Kutub Utara.", "🦷 Clue 3: 'Tanduk' saya sebenarnya adalah gigi taring kiri."]},
    {"nama": "aye-aye", "kategori": "Primata / Lemur Langka", "clues": ["🌙 Clue 1: Primata nokturnal berkerabat dengan lemur.", "🦇 Clue 2: Telinga besar seperti kelelawar.", "🇲🇬 Clue 3: Jari tengah sangat panjang, berasal dari Madagaskar."]},
    {"nama": "tarsius", "kategori": "Primata Mungil", "clues": ["👀 Clue 1: Primata terkecil, matanya lebih besar dari otaknya.", "🔄 Clue 2: Bisa memutar kepala hingga 180 derajat.", "🇮🇩 Clue 3: Spesiesnya ada di hutan Sulawesi, Indonesia."]},
    {"nama": "saola", "kategori": "Mamalia Terancam Punah", "clues": ["🌲 Clue 1: Dijuluki sebagai 'Unicorn Asia' karena misterius.", "🦌 Clue 2: Mirip gabungan kambing dan antelop dengan 2 tanduk.", "🇻🇳 Clue 3: Habitat di Pegunungan Annamite (Vietnam-Laos)."]},
    {"nama": "kakapo", "kategori": "Burung Nuri Unik", "clues": ["🦉 Clue 1: Satu-satunya burung nuri yang tidak bisa terbang.", "💤 Clue 2: Aktif malam hari dan tubuhnya harum.", "🇳🇿 Clue 3: Terancam punah, endemik Selandia Baru."]},
    {"nama": "fossa", "kategori": "Karnivora Unik", "clues": ["🐈 Clue 1: Mirip perpaduan kucing besar, musang, dan anjing.", "🌳 Clue 2: Punya ekor panjang untuk lompat antar pohon.", "🇲🇬 Clue 3: Predator utama lemur di Madagaskar."]},
    {"nama": "blobfish", "kategori": "Ikan Laut Dalam", "clues": ["🌊 Clue 1: Hidup di laut dalam yang sangat gelap dan tekanan tinggi.", "🍮 Clue 2: Tubuhnya seperti massa agar-agar.", "🏆 Clue 3: Pernah dinobatkan sebagai hewan paling jelek."]}
]

# 2. Pengaturan Variabel Memori Web (Session State)
if 'skor' not in st.session_state:
    st.session_state.skor = 0
if 'no_soal' not in st.session_state:
    st.session_state.no_soal = 0

# 3. Tampilan Halaman Web
st.title("🌍 RAREFAUNA QUIZ 🌍")
st.write("Tebak 10 Hewan Langka di Dunia!")
st.divider()

# Jika kuis masih berlangsung
if st.session_state.no_soal < len(hewan_langka):
    hewan = hewan_langka[st.session_state.no_soal]
    
    st.subheader(f"Soal {st.session_state.no_soal + 1}: {hewan['kategori']}")
    
    # Menampilkan Clue
    st.info(hewan['clues'][0])
    st.info(hewan['clues'][1])
    st.info(hewan['clues'][2])
    
    # Input Jawaban
    jawaban = st.text_input("Ketik tebakanmu di sini:", key=f"jawab_{st.session_state.no_soal}")
    
    if st.button("Kirim Jawaban"):
        # Validasi jawaban (huruf kecil semua)
        if jawaban.lower().strip() == hewan['nama']:
            st.success(f"✅ BENAR! Jawabannya adalah {hewan['nama'].capitalize()}.")
            st.session_state.skor += 10
            st.session_state.no_soal += 1
            st.rerun()
        else:
            st.error("❌ Salah! Coba tebak lagi ya.")

# Jika kuis selesai
else:
    st.balloons()
    st.success("🎉 SELAMAT! Kamu telah menyelesaikan kuis. 🎉")
    st.header(f"Total Skormu: {st.session_state.skor} Poin")
    
    if st.button("Main Lagi"):
        st.session_state.skor = 0
        st.session_state.no_soal = 0
        st.rerun()
