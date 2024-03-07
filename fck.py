import requests
from concurrent.futures import ThreadPoolExecutor
import time
from bs4 import BeautifulSoup

def attack(url):
    fckeditor_urls = (
        '/FCKeditor/editor/filemanager/browser/default/connectors/asp/connector.asp?Command=GetFoldersAndFiles&Type=Image&CurrentFolder=/',
        '/FCKeditor/editor/filemanager/browser/default/browser.html?Type=File&Connector=../../connectors/php/connector.php',
        '/FCKeditor/editor/filemanager/browser/default/browser.html?Type=Image&Connector=connectors/jsp/connector.jsp',
        '/FCKeditor/editor/filemanager/browser/default/connectors/test.html',
        '/FCKeditor/editor/filemanager/upload/test.html',
        '/FCKeditor/editor/filemanager/connectors/test.html',
        '/FCKeditor/editor/filemanager/connectors/uploadtest.html',
        '/FCKeditor/editor/filemanager/browser/default/browser.html?Type=Image&Connector=connectors/jsp/connector',
        '/editor/filemanager/browser/default/connectors/asp/connector.asp?Command=GetFoldersAndFiles&Type=Image&CurrentFolder=/',
        '/editor/filemanager/browser/default/connectors/jsp/connector.jsp?Command=GetFoldersAndFiles&Type=Image&CurrentFolder=/',
        '/editor/filemanager/browser/default/connectors/php/connector.php?Command=GetFoldersAndFiles&Type=Image&CurrentFolder=/',
        '/editor/filemanager/browser/default/browser.html?type=Image&connector=connectors/asp/connector.asp',
        '/editor/filemanager/browser/default/browser.html?type=Image&connector=connectors/jsp/connector.jsp',
        '/editor/filemanager/browser/default/browser.html?type=Image&connector=connectors/php/connector.php',
        '/editor/filemanager/browser/default/browser.html?Type=Image&Connector=http://www.site.com%2Ffckeditor%2Feditor%2Ffilemanager%2Fconnectors%2Fphp%2Fconnector.php',
        '/editor/filemanager/browser/default/browser.html?Type=Image&Connector=http://www.site.com%2Ffckeditor%2Feditor%2Ffilemanager%2Fconnectors%2Fjsp%2Fconnector.jsp',
        '/editor/filemanager/browser/default/browser.html?Type=Image&Connector=http://www.site.com%2Ffckeditor%2Feditor%2Ffilemanager%2Fconnectors%2Fasp%2Fconnector.asp',
        '/editor/filemanager/browser/default/browser.html?Type=Image&Connector=connectors/jsp/connector.jsp',
        '/editor/filemanager/browser/default/browser.html?Type=Image&Connector=connectors/asp/connector.asp',
        '/editor/filemanager/browser/default/browser.html?Type=Image&Connector=connectors/php/connector.php',
        '/editor/filemanager/browser/default/connectors/test.html',
        '/editor/filemanager/upload/test.html',
        '/editor/filemanager/connectors/test.html',
        '/editor/filemanager/connectors/uploadtest.html',
        '/editor/filemanager/browser/default/browser.html?Type=Image&Connector=connectors/jsp/connector'
        # ... (tambahkan URL Fckeditor lainnya di sini)
    )

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    headers = {"User-Agent": user_agent}

    results = []
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    for fckeditor_url in fckeditor_urls:
        full_url = url + fckeditor_url
        try:
            verify_response = requests.get(full_url, headers=headers, timeout=5)
            if verify_response.status_code == 200:
                soup = BeautifulSoup(verify_response.text, 'html.parser')
                title_tag = soup.find('title')
                if title_tag and 'FCKeditor - Resources Browser' in title_tag.text:
                    print(f"Vuln Fckeditor: {url}")
                    results.append(full_url)
                    # Simpan hasil langsung saat vuln terdeteksi
                    with open("result.txt", "a") as file:
                        file.write(full_url + "\n")
        except Exception as e:
            print(f"No Vuln {url}")
    return results

def main():
    start_time = time.time()
    print("Mass Scanner FCKEditor ")
    input_file = input("Give Me Ur List: ")
    
    try:
        with open(input_file, "r") as file:
            url_list = file.read().splitlines()
    except FileNotFoundError:
        print(f"File '{input_file}' tidak ditemukan. Program berhenti.")
        return

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(attack, url) for url in url_list]

        all_results = []
        for future in futures:
            results = future.result()
            all_results.extend(results)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\n[+] Proses selesai dalam waktu {elapsed_time:.2f} detik.")
    print(f"[+] Hasil telah disimpan di 'result.txt'.")

if __name__ == "__main__":
    main()
