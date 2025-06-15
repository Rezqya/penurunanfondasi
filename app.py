import streamlit as st
import pandas as pd
import joblib
import os

# Judul Aplikasi
st.title("Prediksi Penurunan Fondasi - SVR")

# Load model dan scaler
model = joblib.load("svr_model_terbaik.pkl")
scaler = joblib.load("scaler_svr.pkl")

# =========================
# Form Input Manual
# =========================
st.header("1️⃣ Prediksi Data Manual")

L = st.number_input("Panjang tiang (L)", min_value=0.0)
Qp = st.number_input("Daya dukung ujung (Qp)", min_value=0.0)
Qs = st.number_input("Daya dukung geser (Qs)", min_value=0.0)
D = st.number_input("Diameter tiang (D)", min_value=0.0)
Q_beban = st.number_input("Beban kerja (Q)", min_value=0.0)

if st.button("Prediksi Manual"):
    data_input = pd.DataFrame([{
        'L': L, 'Qp': Qp, 'Qs': Qs, 'D': D, 'Q(beban)': Q_beban
    }])
    data_scaled = scaler.transform(data_input)
    hasil = model.predict(data_scaled)[0]
    st.success(f"Hasil prediksi penurunan: {hasil:.4f} mm")

    hasil_dict = {
        "L": L, "Qp": Qp, "Qs": Qs, "D": D, "Q(beban)": Q_beban,
        "Prediksi Penurunan (mm)": hasil
    }

    file_excel = "hasil_prediksi.xlsx"
    if os.path.exists(file_excel):
        df_existing = pd.read_excel(file_excel)
        df_new = df_existing.append(hasil_dict, ignore_index=True)
    else:
        df_new = pd.DataFrame([hasil_dict])

    df_new.to_excel(file_excel, index=False)
    st.info(f"Hasil disimpan ke: {file_excel}")

# =========================
# Upload File Excel
# =========================
st.header("2️⃣ Prediksi Banyak Data dari Excel")

uploaded_file = st.file_uploader("Upload file Excel (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        required_cols = ['L', 'Qp', 'Qs', 'D', 'Q(beban)']
        if not all(col in df.columns for col in required_cols):
            st.error("Format kolom salah. Harus ada kolom: L, Qp, Qs, D, Q(beban)")
        else:
            data_scaled = scaler.transform(df[required_cols])
            predictions = model.predict(data_scaled)
            df['Prediksi Penurunan (mm)'] = predictions
            st.success("Prediksi berhasil!")

            st.dataframe(df)

            hasil_batch = "hasil_prediksi_batch.xlsx"
            df.to_excel(hasil_batch, index=False)
            st.info(f"Hasil batch disimpan ke: {hasil_batch}")
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
