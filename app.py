import streamlit as st
import pandas as pd
import plotly.express as px

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Laporan Keuangan Biro Koperasi", layout="wide")

# --- LINK GOOGLE SHEETS ANDA ---
# Link ini sudah diformat agar Python bisa membaca data Excel-nya secara langsung
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS0yN69J6fYV0xDUKC919aVKP5WuN7d0A7GZn0QsIQzdG_MFGBRcnae4DjogoUIOW4ioJ1HdqPQHtO4/pub?output=csv"

# --- FUNGSI AMBIL DATA ---
@st.cache_data(ttl=300) # Data diperbarui setiap 5 menit jika halaman direfresh
def get_data():
    try:
        df = pd.read_csv(SHEET_URL)
        # Memastikan kolom Tanggal terbaca sebagai format tanggal
        if 'Tanggal' in df.columns:
            df['Tanggal'] = pd.to_datetime(df['Tanggal'])
        return df
    except Exception as e:
        st.error(f"Koneksi ke data Excel gagal: {e}")
        return pd.DataFrame()

# --- SISTEM LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Akses Laporan Koperasi")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    if st.button("Masuk"):
        if user == "admin" and pw == "koperasi123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Username atau password salah")
else:
    # --- TAMPILAN DASHBOARD ---
    df = get_data()

    # Sidebar Menu
    st.sidebar.title("Menu Laporan")
    st.sidebar.info("Data tersinkronisasi otomatis dengan Google Sheets.")
    if st.sidebar.button("🔄 Segarkan Data"):
        st.cache_data.clear()
        st.rerun()
    if st.sidebar.button("🚪 Keluar"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("📊 Laporan Keuangan Biro Koperasi")
    st.markdown("---")

    if not df.empty:
        # 1. Ringkasan (Metrics)
        # Menjumlahkan kolom 'Masuk' dan 'Keluar' dari file Excel Anda
        masuk = df['Masuk'].sum() if 'Masuk' in df.columns else 0
        keluar = df['Keluar'].sum() if 'Keluar' in df.columns else 0
        saldo = masuk - keluar

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Pemasukan", f"Rp {masuk:,.0f}")
        c2.metric("Total Pengeluaran", f"Rp {keluar:,.0f}")
        c3.metric("Saldo Akhir", f"Rp {saldo:,.0f}")

        st.markdown("---")

        # 2. Grafik & Tabel
        col_table, col_chart = st.columns([2, 1])

        with col_table:
            st.subheader("📝 Rincian Transaksi (Format Excel)")
            # Menampilkan tabel seperti di Excel tapi lebih interaktif
            st.dataframe(df, use_container_width=True, height=500)
