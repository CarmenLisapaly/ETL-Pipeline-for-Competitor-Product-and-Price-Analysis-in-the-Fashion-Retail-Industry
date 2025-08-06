import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
# Mengaktifkan pengaturan baru sesuai peringatan
pd.set_option('future.no_silent_downcasting', True)

def transform_data(products):
    #Definisikan harga rupiah
    rupiah = 16000

    # Membuat DataFrame dari data produk
    df = pd.DataFrame(products)

    # Hapus baris dengan title invalid
    df = df[df['title'].str.lower() != 'unknown product']

    # Konversi price
    df['price'] = df['price'].replace(r'[^\d.]', '', regex=True)
    df['price'] = df['price'].replace('', np.nan)
    df.dropna(subset=['price'], inplace=True)

    df['price'] = df['price'].astype(float) * rupiah
    
    # Konversi rating
    df['rating'] = df['rating'].replace(r'[^0-9.]', '', regex=True)  
    df['rating'] = df['rating'].replace('', np.nan) 
    df.dropna(subset=['rating'], inplace=True)  
    df['rating'] = df['rating'].astype(float)
    df['rating'] = np.floor(df['rating'] * 10) / 10  # Bulatkan ke bawah 1 desimal 

    #Konversi colors
    df['colors'] = df['colors'].replace(r'\D', '', regex = True)
    df['colors'] = df['colors'].replace('', np.nan)
    df.dropna(subset=['colors'], inplace= True)

    df['colors'] = df['colors'].astype(int)

    #Konversi size
    df['size'] = df['size'].replace(r'Size:\s', '', regex= True)
    df['size'] = df['size'].replace('', np.nan)
    df.dropna(subset=['size'], inplace= True)

    #Konversi gender
    df['gender'] = df['gender'].replace(r'Gender:\s', '', regex= True)
    df['gender'] = df['gender'].replace('', np.nan)
    df.dropna(subset=['gender'], inplace= True)

    ## Drop duplicates & null
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    # Tambahkan kolom timestamp
    df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return df