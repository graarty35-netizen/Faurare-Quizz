import streamlit as st
import time
import random

st.set_page_config(page_title="RareFauna Quiz Indonesia", page_icon="🇮🇩", layout="centered")

# Database 10 Hewan Endemik Indonesia
daftar_hewan = [
    {"nama": "komodo", "kategori": "Reptil Purba / NTT", "ikon": "🦖🏝️", "clues": ["✨ Clue 1: Reptil terbesar di dunia.", "🇮🇩 Clue 2: Air liur beracun.", "🏝️ Clue 3: Endemik NTT."], "fakta": "Komodo adalah kadal terbesar di bumi yang panjangnya bisa mencapai 3 meter!"},
    {"nama": "orangutan", "kategori": "Primata / Sumatera & Kalimantan", "ikon": "🦧🌴", "clues": ["✨ Clue 1: Berarti 'manusia hutan'.", "🟠 Clue 2: Berbulu jingga.", "🌴 Clue 3: Hidup di atas pohon."], "fakta": "Orangutan sangat cerdas dan mampu menggunakan alat."},
    {"nama": "badak jawa", "kategori": "Mamalia / Ujung Kulon", "ikon": "🦏🌿", "clues": ["✨ Clue 1: Salah satu mamalia paling langka.", "🦄 Clue 2: Bercula satu.", "🌊 Clue 3: Di Ujung Kulon."], "fakta": "Badak jawa menyukai kubangan lumpur untuk mendinginkan tubuh."},
    {"nama": "harimau sumatera", "kategori": "Karnivora / Sumatera", "ikon": "🐅🍂", "clues": ["✨ Clue 1: Harimau terkecil tersisa.", "🖤 Clue 2: Loreng sangat rapat.", "🇮🇩 Clue 3: Kucing besar khas Indonesia."], "fakta": "Harimau sumatera adalah perenang yang sangat handal."},
    {"nama": "anoa", "kategori": "Mamalia / Sulawesi", "ikon": "🐃⛰️", "clues": ["✨ Clue 1: Dijuluki kerbau kerdil.", "🛡️ Clue 2: Bertanduk lurus tajam.", "🇮🇩 Clue 3: Endemik Sulawesi."], "fakta": "Anoa bersifat soliter dan suka berendam di lumpur."},
    {"nama": "cendrawasih", "kategori": "Burung / Papua", "ikon": "🦜✨", "clues": ["✨ Clue 1: Dijuluki Burung Surga.", "🎨 Clue 2: Bulu ekor sangat megah.", "🇮🇩 Clue 3: Habitat di hutan Papua."], "fakta": "Keindahan bulunya menjadi simbol budaya khas Papua."},
    {"nama": "babirusa", "kategori": "Mamalia / Sulawesi", "ikon": "🐗🦷", "clues": ["✨ Clue 1: Gabungan babi dan rusa.", "🦷 Clue 2: Taring menembus moncong.", "🇮🇩 Clue 3: Asli Sulawesi."], "fakta": "Taring jantan bisa melingkar hampir menyentuh mata."},
    {"nama": "maleo", "kategori": "Burung / Sulawesi", "ikon": "🥚🔥", "clues": ["✨ Clue 1: Ada benjolan di kepala.", "🌋 Clue 2: Telur ditimbun pasir panas.", "🔥 Clue 3: Memanfaatkan panas vulkanik."], "fakta": "Anak maleo bisa langsung terbang setelah menetas."},
    {"nama": "tarsius", "kategori": "Primata / Sulawesi", "ikon": "👀🌿", "clues": ["✨ Clue 1: Primata bermata sangat besar.", "🔄 Clue 2: Kepala bisa putar 180 derajat.", "🇮🇩 Clue 3: Lompat di pohon Sulawesi."], "fakta": "Matanya lebih besar daripada ukuran otaknya."},
    {"nama": "jalak bali", "kategori": "Burung / Bali", "ikon": "🕊️🌺", "clues": ["✨ Clue 1: Bulu putih bersih bermata biru.", "🌸 Clue 2: Memiliki jambul indah.", "🏝️ Clue 3: Maskot fauna resmi Bali."], "fakta": "Jalak bali termasuk burung paling dilindungi di dunia."}
]

# Inisialisasi Session State
if 'skor' not in st.session_state: st.session_state.skor = 0
if 'no_soal' not in st.session_state: st.session_state.no_soal = 0
if 'nama_pemain' not in st.session_state: st.session_state.nama_pemain = ""
if 'soal_acak' not in st.session_state: 
    st.session_state.soal_acak = random.sample(daftar_hewan, len(daftar_hewan))

# Halaman Login
if st.session_state.nama_pemain == "":
    st.title("🇮🇩 KUIS ENDEMIK FAUNA INDONESIA 🇮🇩")
    st.write("Selamat datang di Ujian Sidang Ekspedisi Nusantara!")
    nama = st.text_input("Siapa nama lengkap/panggilan calon Sarjana Hewan?")
    if st.button("🚀 Mulai Ujian Ekspedisi!", use_container_width=True):
        if nama:
            st.session_state.nama_pemain = nama
            st.session_state.soal_acak = random.sample(daftar_hewan, len(daftar_hewan))
            st.rerun()
        else:
            st.warning("Tulis namamu dulu ya!")
else:
    # Sidebar dengan Audio player HTML agar tombol Play/Pause responsif di perangkat seluler/iPad
    with st.sidebar:
        st.header(f"Explorer: {st.session_state.nama_pemain} 🇮🇩")
        st.metric("Skor Sementara", f"{st.session_state.skor} Poin")
        st.progress(st.session_state.no_soal / len(st.session_state.soal_acak))
        st.caption(f"Soal {st.session_state.no_soal + 1} dari {len(st.session_state.soal_acak)}")
        
        st.divider()
        st.subheader("🎵 Backsound Alam")
        # Menggunakan pemutar audio HTML bawaan agar tombol play langsung bisa diklik di Safari/HP
        st.markdown("""
            <audio controls loop style="width: 100%;">
                <source src="https://actions.google.com/sounds/v1/ambiences/forest_birds.ogg" type="audio/ogg">
                Browser kamu tidak Mendukung pemutar audio.
            </audio>
        """, unsafe_allow_html=True)

    # Ambil soal berdasarkan urutan acak
    if st.session_state.no_soal < len(st.session_state.soal_acak):
        h = st.session_state.soal_acak[st.session_state.no_soal]
        
        st.title(f"Soal No. {st.session_state.no_soal + 1}")
        st.subheader(f"Kategori: {h['kategori']}")
        
        st.markdown(f"<h1 style='text-align: center; font-size: 90px;'>{h['ikon']}</h1>", unsafe_allow_html=True)
        st.info("💡 Analisis wilayah dan ikon di atas, lalu buka petunjuk jika diperlukan!")
        st.divider()
        
        with st.expander("✨ Buka Clue 1"):
            st.write(h['clues'][0])
        with st.expander("🇮🇩 Buka Clue 2"):
            st.write(h['clues'][1])
        with st.expander("🗺️ Buka Clue 3 (Spesifik)"):
            st.write(h['clues'][2])
        
        jawaban = st.text_input("Ketik tebakan nama hewan:", key=f"j_{st.session_state.no_soal}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Kirim Jawaban", use_container_width=True):
                if jawaban.lower().strip() == h['nama']:
                    st.success(f"✅ BENAR! Hebat, ini faktanya: *{h['fakta']}*")
                    st.session_state.skor += 10
                    st.session_state.no_soal += 1
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("❌ Kurang tepat! Coba pikirkan lagi atau buka clue tambahan.")
        with col2:
            if st.button("Nyerah & Lewati 🏳️", use_container_width=True):
                st.warning(f"Jawabannya adalah: **{h['nama'].capitalize()}**")
                st.session_state.no_soal += 1
                time.sleep(1.8)
                st.rerun()
    else:
        # Halaman Selesai & Museum Mini dengan Gelar Kustom
        st.balloons()
        st.success("🎉 SELAMAT! UJIAN & EKSPEDISI NUSANTARA SELESAI 🎉")
        st.header(f"Sidang Kelulusan: {st.session_state.nama_pemain}")
        st.metric("Total Nilai Akhir", f"{st.session_state.skor} / 100 Poin")
        
        # Sistem Gelar Kustom Sesuai Permintaanmu
        if st.session_state.skor >= 90:
            st.markdown("🎓 **Gelar Kelulusan:** `S.Hwn` — **Predikat: Luar Biasa!** 🏆")
        elif st.session_state.skor >= 60:
            st.markdown("📜 **Gelar Kelulusan:** `S.k` — **Predikat: Hebat!** 🥈")
        elif st.session_state.skor >= 30:
            st.markdown("🥉 **Gelar Kelulusan:** `S.Tda` — **Predikat: Cukup**")
        else:
            st.markdown("🤦‍♂️ **Gelar Kelulusan:** `ADOHHHHH, heran` — **Ayo Ujian Ulang!** 😅")
            
        st.divider()
        st.header("🏛️ Museum Mini Ensiklopedia Fauna Indonesia")
        st.write("Pelajari kembali fakta unik dari ke-10 hewan endemik:")
        
        for i, item in enumerate(daftar_hewan):
            with st.expander(f"🇮🇩 {i+1}. {item['nama'].capitalize()} ({item['kategori']})"):
                st.markdown(f"### {item['ikon']}")
                st.write(f"**Fakta Unik:** {item['fakta']}")
                
        st.divider()
        if st.button("🔄 Ujian Ulang (Soal Diacak)", use_container_width=True):
            st.session_state.skor = 0
            st.session_state.no_soal = 0
            st.session_state.soal_acak = random.sample(daftar_hewan, len(daftar_hewan))
            st.rerun()
