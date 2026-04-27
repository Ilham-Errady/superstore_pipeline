import pandas as pd

def clean_my_data():
    df = pd.read_csv("../staging/raw_avito_data.csv")
    df['price'] = df['price'].str.replace(r'\D', '', regex=True)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df.dropna(subset=['title', 'price'], inplace=True)
    df.to_csv("../clean/cleaned_avito_data.csv", index=False)
    print("تم تنظيف البيانات وحفظها في مجلد clean.")

if __name__ == "__main__":
    clean_my_data()