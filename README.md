# SignLanguageDetectionBISINDO

Sistem Deteksi Bahasa Isyarat BISINDO berbasis AI yang mampu mengenali gerakan tangan secara real-time melalui kamera, menggunakan model deep learning dan MediaPipe. Proyek ini dirancang untuk membantu komunikasi penyandang tuli/bisu dengan menerjemahkan bahasa isyarat ke dalam bentuk teks secara langsung.

## Fitur Utama

- Deteksi bahasa isyarat BISINDO secara real-time melalui webcam.
- Tampilan prediksi huruf/kalimat dan tingkat kepercayaan (confidence).
- Riwayat hasil deteksi dapat diekspor ke file teks.
- Statistik jumlah deteksi dan rata-rata confidence.
- UI modern dan responsif.

## Cara Penggunaan

1. **Instalasi Dependensi**
   
   Pastikan Python dan pip sudah terpasang. Install library yang dibutuhkan:
   ```bash
   pip install -r requirements.txt
   ```

2. **Menyiapkan Model**
   
   Pastikan file model (`models/sign_language_model_75.h5`) dan label encoder (`models/label_encoder_75.pkl`) sudah tersedia di folder `models/`.

3. **Menjalankan Server**
   
   Jalankan server Flask:
   ```bash
   python server.py
   ```
   Server akan berjalan di `localhost:5000` secara default.

4. **Akses Antarmuka Web**
   
   Buka browser dan akses `http://localhost:5000`. Sistem akan otomatis mengaktifkan webcam dan melakukan deteksi bahasa isyarat secara real-time.

5. **Melihat Hasil dan Statistik**
   
   - Prediksi ditampilkan di bagian “Current Prediction”.
   - Persentase confidence ditampilkan di “Confidence Level”.
   - Riwayat deteksi dapat diekspor dengan tombol “Export History”.
   - Statistik jumlah deteksi dan rata-rata confidence tersedia di panel hasil.

6. **Ekspor Riwayat Deteksi**
   
   Klik tombol `💾 Export History` untuk menyimpan hasil deteksi ke file `.txt`.

## Struktur Utama Project

- `server.py` : Backend Flask yang menangani streaming video dan prediksi.
- `templates/index.html` : Frontend utama berbasis HTML.
- `static/ap.js` : Script frontend untuk fetch prediksi, update UI, dan ekspor riwayat.
- `static/st.css` : Style untuk tampilan web.

## Catatan

- Pastikan webcam berfungsi dengan baik.
- Model yang digunakan adalah hasil training pada dataset BISINDO.
- Untuk performa optimal, jalankan pada perangkat dengan GPU.

---

Kontribusi, pertanyaan, dan masukan sangat diterima!

**##LINK DATASET**
https://drive.google.com/file/d/18vjPXAkxnm2AUoNbmAdHIlpAKNkOoeSX/view?usp=sharing
