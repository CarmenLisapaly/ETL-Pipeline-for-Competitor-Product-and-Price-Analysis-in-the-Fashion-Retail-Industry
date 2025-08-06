
import pandas as pd
from utils.extract import scrape_products
from utils.transform import transform_data
from utils.load import load_to_postgresql
from utils.load import load_to_csv
from utils.load import load_to_google_sheets


def main():
    """Fungsi utama untuk keseluruhan proses scraping hingga menyimpannya."""
    
    all_products = []

    """Page utama"""
    BASE_URL_MAIN = 'https://fashion-studio.dicoding.dev/'
    print(f"Scraping main page: {BASE_URL_MAIN}")
    try:
        products = scrape_products(BASE_URL_MAIN)
        all_products.extend(products)
    except Exception as e:
        print(f"❌ Failed to scrape main page: {e}")

    """Page 2 sampai 50"""
    for page in range(2, 51):
        BASE_URL = f'https://fashion-studio.dicoding.dev/page{page}'
        print(f"Scraping page {page}: {BASE_URL}")
        try:
            products = scrape_products(BASE_URL)
            all_products.extend(products)
        except Exception as e:
            print(f"❌ Failed to scrape main page: {e}")
    
    transform = transform_data(all_products)

    df = pd.DataFrame(transform)
    print(df)

    load_to_postgresql(df)
    load_to_csv(df, "product.csv")
    load_to_google_sheets(df, "Sheet1!A1")


if __name__ == '__main__':
    main()
