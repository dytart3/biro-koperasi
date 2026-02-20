import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Editor Laporan Koperasi", layout="wide")

# --- SISTEM LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🔐 Akses Editor Koperasi")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    if st.button("Masuk"):
        if user == "admin" and pw == "koperasi123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Username atau password salah")

# --- TAMPILAN UTAMA ---
if not st.session_state.logged_in:
    login()
else:
    # Sidebar untuk Logout
    st.sidebar.title("Menu")
    if st.sidebar.button("🚪 Keluar"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("📝 Edit Laporan Keuangan Langsung")
    st.info("Anda bisa menambah, menghapus, atau mengubah data langsung di bawah ini. Perubahan akan tersimpan otomatis ke Google Sheets.")

    # --- MENAMPILKAN GOOGLE SHEETS (MODE EDIT) ---
    # Menggunakan link dasar spreadsheet Anda agar bisa diedit
    sheet_editor_url = "
