import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
from sendmail import sendmail


def reader_and_change(filename):
    # CSV dosyasını oku
    df = pd.read_csv(filename, encoding="utf-8-sig")
    checked=set()
    # "author" sütununu kontrol et
    if "author" in df.columns:
        # "author" sütununda "CNN TÜRK" olanları işle
        urls = df[df["author"].isin(["Cnnturk.com", "CNN TÜRK", "Fanatik", "DHA", "İHA", "Milliyet", "Hürriyet", "Haber Merkezi", "hurriyet.com.tr", "AA" ,"cnnturk.com"])]["pageUrlCleanNoProtcol"]
        for original_url in urls:
            url="https://" + original_url
            if url not in checked:
                try:
                    html = requests.get(url).content
                    soup = BeautifulSoup(html, "html.parser")
                    checked.add(url)

                    creators = soup.find("meta", {"property" : "creators"})
                    if creators:
                        author = creators.get("content")
                        if author:
                            for idx in df.index[df['pageUrlCleanNoProtcol'] == original_url]:
                                df.at[idx, 'author'] = author
                                print(f"TEST PASSED | {author} | {url}")
                        else:
                            for idx in df.index[df['pageUrlCleanNoProtcol'] == original_url]:
                                df.at[idx, 'author'] = ""
                                print(f"TEST FAILED | {author} | {url}")

                except Exception:
                    df['author'] = np.where(df['pageUrlCleanNoProtcol'] == original_url, "", df['author']) 
                    print("PROBLEM")   #erişim izni olmayanları "" çevirir

    df.to_csv("_04_25_2024_updated.csv", index=False, encoding="utf-8-sig")
    
if __name__ =="__main__":
    reader_and_change("_04_25_2024.csv")

