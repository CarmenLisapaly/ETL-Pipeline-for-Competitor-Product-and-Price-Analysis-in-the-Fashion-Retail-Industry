import unittest
from utils import load  
import pandas as pd
import os

class TestLoad(unittest.TestCase):

    def setUp(self):
        # Setup data dummy (DataFrame) yang akan digunakan untuk semua test
        self.df = pd.DataFrame({
            'title': ['Test Product'],
            'price': [100000.0],
            'rating': [4.5],
            'colors': [2],
            'size': ['L'],
            'gender': ['Male'],
            'timestamp': ['2025-06-06 10:00:00']
        })
        self.csv_filename = 'test_output.csv'

    def test_load_to_csv(self):
        """Menguji apakah data disimpan ke file CSV dengan benar"""
        load.load_to_csv(self.df, self.csv_filename)
        self.assertTrue(os.path.exists(self.csv_filename))  # Pastikan file dibuat

        # Baca ulang dan bandingkan dengan data asli
        loaded_df = pd.read_csv(self.csv_filename)
        pd.testing.assert_frame_equal(self.df, loaded_df)

        # Clean-up
        os.remove(self.csv_filename)

    def test_load_to_postgresql(self):
        """Menguji apakah data berhasil di-insert ke PostgreSQL"""
        try:
            load.load_to_postgresql(self.df, table_name='test_products')
        except Exception as e:
            self.fail(f"Gagal menyimpan ke PostgreSQL: {e}")

    def test_load_to_google_sheets(self):
        """Tes dummy: hanya memeriksa fungsi dipanggil tanpa error (tidak menyimpan sungguhan)"""
        try:
            # Simulasi panggilan (kecuali kamu punya kredensial dan spreadsheet aktif)
            load.load_to_google_sheets(
                self.df,
                range_name='Sheet1!A1',
                spreadsheet_id='1oIxZtCuPFbzuYMxkOWabo4xSjc5FTdrJ5erN122FZY4',
                service_account_file='client_secret.json'
            )
        except Exception as e:
            self.fail(f"Gagal menyimpan ke Google Sheets: {e}")

if __name__ == '__main__':
    unittest.main()
