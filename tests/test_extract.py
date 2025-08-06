import unittest
import sys
import os
from bs4 import BeautifulSoup
from utils import extract

# Tambahkan path ke direktori saat ini agar bisa impor modul utils
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

class TestExtract(unittest.TestCase):

    def test_fetching_content_invalid_url(self):
        """Test jika URL tidak valid, harus mengembalikan None"""
        content = extract.fetching_content("http://invalid-url.test")
        self.assertIsNone(content)

    def test_extract_product_data_complete_info(self):
        """Test ekstraksi data produk dari HTML lengkap"""
        html = """
        <div class='collection-card'>
            <h3 class='product-title'>Sample Product</h3>
            <div class='price-container'>$29.99</div>
            <p>Rating: 4.5</p>
            <p>Colors: 3</p>
            <p>Size: M</p>
            <p>Gender: Unisex</p>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.find('div', class_='collection-card')
        result = extract.extract_product_data(article)

        self.assertIsInstance(result, dict)
        self.assertEqual(result['title'], 'Sample Product')
        self.assertEqual(result['price'], '$29.99')
        self.assertEqual(result['rating'], 'Rating: 4.5')
        self.assertEqual(result['colors'], 'Colors: 3')
        self.assertEqual(result['size'], 'Size: M')
        self.assertEqual(result['gender'], 'Gender: Unisex')

    def test_extract_product_data_missing_fields(self):
        """Test jika beberapa field HTML hilang, maka fallback value harus digunakan"""
        html = """
        <div class='collection-card'>
            <h3 class='product-title'>Incomplete Product</h3>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.find('div', class_='collection-card')
        result = extract.extract_product_data(article)

        self.assertEqual(result['price'], 'Price Unavailable')
        self.assertEqual(result['rating'], 'No Rating')
        self.assertEqual(result['colors'], 'No Color Info')
        self.assertEqual(result['size'], 'No Size Info')
        self.assertEqual(result['gender'], 'No Gender Info')

    def test_scrape_products_with_invalid_url(self):
        """Test scrape_products dengan URL tidak valid harus mengembalikan list kosong"""
        data = extract.scrape_products("http://invalid-url.test")
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)


if __name__ == '__main__':
    unittest.main()
