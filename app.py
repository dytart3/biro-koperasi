import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Editor Laporan Koperasi", layout="wide")

# --- SISTEM LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🔐 Biro Koperasi")
    # Bagian tengah layar
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
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
    st.sidebar.title("Menu Utama")
    st.sidebar.success("Status: Terhubung ke Google Sheets")
    if st.sidebar.button("🚪 Log Out"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("📝 Biro Koperasi ")
    st.write("Silakan edit tabel di bawah. Perubahan tersimpan secara otomatis.")

    # --- LINK GOOGLE SHEETS TERBARU ANDA ---
    # Saya sudah mengambil ID unik dari link yang Anda berikan
    sheet_id = "1w0nUXKqoAc3UhzFdlO7yxwvz5Grfy5rS"
    sheet_editor_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit?usp=sharing"
    
    # Menampilkan Spreadsheet dalam bingkai (Iframe)
    st.components.v1.iframe(sheet_editor_url, height=800, scrolling=True)

