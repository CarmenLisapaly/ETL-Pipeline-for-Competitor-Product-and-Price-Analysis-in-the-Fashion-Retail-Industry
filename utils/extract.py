import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

def fetching_content(url):
    """Mengambil konten HTML dari URL yang diberikan."""
    session = requests.Session()
    try:
        response = session.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Gagal mengambil konten dari {url}: {e}")
        return None
    finally:
        session.close()

def extract_product_data(article):
    """Mengambil data fashion berupa Title, Price, Rating, Colors, Size, Gender (element html)."""
    title_tag = article.find('h3', class_='product-title')
    title = title_tag.text.strip() if title_tag else 'Unknown Title'

    price_tag = article.find('div', class_='price-container')
    price = price_tag.text.strip() if price_tag else 'Price Unavailable'

    rating_tag = article.find('p', string=lambda text: text and 'Rating' in text)
    rating = rating_tag.text.strip() if rating_tag else 'No Rating'

    colors_tag = article.find('p', string=lambda text: text and 'Colors' in text)
    colors = colors_tag.text.strip() if colors_tag else 'No Color Info'

    size_tag = article.find('p', string=lambda text: text and 'Size' in text)
    size = size_tag.text.strip() if size_tag else 'No Size Info'

    gender_tag = article.find('p', string=lambda text: text and 'Gender' in text)
    gender = gender_tag.text.strip() if gender_tag else 'No Gender Info'

    products= {
        'title': title,
        'price': price,
        'rating': rating,
        'colors': colors,
        'size': size,
        'gender': gender
    }

    return products


def scrape_products(base_url):
    """
    Fungsi utama untuk mengambil keseluruhan data dari halaman produk.
    Mengembalikan list of dict berisi detail produk.
    """
    data = []

    content = fetching_content(base_url)
    if content:
        soup = BeautifulSoup(content, "html.parser")
        div_elements = soup.find_all('div', class_='collection-card')
        for div in div_elements:
            product = extract_product_data(div)
            if product:  # Hindari menyimpan data kosong/None
                data.append(product)

    return data