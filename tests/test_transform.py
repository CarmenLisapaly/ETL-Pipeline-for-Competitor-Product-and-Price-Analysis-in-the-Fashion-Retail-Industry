import unittest
import pandas as pd
from utils import transform  

class TestTransform(unittest.TestCase):

    def setUp(self):
        # Data mentah sebagai contoh input
        self.sample_data = [
            {
                'title': 'Sample Product',
                'price': '$25.99',
                'rating': 'Rating: 4.2',
                'colors': 'Colors: 3',
                'size': 'Size: M',
                'gender': 'Gender: Male'
            },
            {
                'title': 'Unknown Product',
                'price': '$0.00',
                'rating': 'Rating: 0',
                'colors': 'Colors: 0',
                'size': 'Size: L',
                'gender': 'Gender: Female'
            }
        ]

    def test_transform_data_output(self):
        """Test transform_data menghasilkan DataFrame yang valid"""
        df = transform.transform_data(self.sample_data)

        # Output harus berupa DataFrame
        self.assertIsInstance(df, pd.DataFrame)

        # Produk 'Unknown Product' harus terfilter
        self.assertNotIn('unknown product', df['title'].str.lower().values)

        # Kolom penting harus tersedia
        for col in ['price', 'rating', 'colors', 'size', 'gender', 'timestamp']:
            self.assertIn(col, df.columns)

    def test_price_conversion(self):
        """Harga harus dikonversi menjadi float > 0 dan dikali kurs (16.000)"""
        df = transform.transform_data(self.sample_data)

        # Semua harga harus float dan > 0
        self.assertTrue((df['price'] > 0).all())
        self.assertEqual(df['price'].dtype, float)

        # Contoh perhitungan harga: $25.99 * 16.000 = 415.840
        expected_price = 25.99 * 16000
        self.assertAlmostEqual(df.iloc[0]['price'], expected_price, places=1)

    def test_rating_and_colors_conversion(self):
        """Kolom rating dan colors dikonversi ke numerik"""
        df = transform.transform_data(self.sample_data)

        self.assertEqual(df['rating'].dtype, float)
        self.assertEqual(df['colors'].dtype, int)

    def test_timestamp_column_format(self):
        """Kolom timestamp harus dalam format string datetime"""
        df = transform.transform_data(self.sample_data)
        timestamp = df.iloc[0]['timestamp']

        # Cek apakah timestamp merupakan string dalam format 'YYYY-MM-DD HH:MM:SS'
        self.assertRegex(timestamp, r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')


if __name__ == '__main__':
    unittest.main()
