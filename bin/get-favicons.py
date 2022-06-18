import mysql.connector
import os
import requests
import favicon

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bobthefish",
    database="reader",
)

def download(domain,  id):
    useragent_headers = {'User-Agent': 'Spudooli Reader/1.0 - favicon scraper - https://reader.spudooli.com/about'}
    icons = favicon.get(domain, headers=useragent_headers)
    icon = icons[0]

    response = requests.get(icon.url, headers=useragent_headers, stream=True)
    icon_file = f'{str(id)}.{icon.format}'
    with open('/var/www/reader/reader/static/icons/' + icon_file, 'wb') as image:
        for chunk in response.iter_content(1024):
            image.write(chunk)
    
    try:
        os.system(f"convert /var/www/reader/reader/static/icons/{icon_file} -thumbnail 64x64 -flatten /var/www/reader/reader/static/icons/{id}.gif")
    except:
        print(f"failed to convert {icon_file}") 
        pass

if __name__=='__main__':
    
    cursor = connection.cursor(buffered = True)
    cursor.execute("SELECT id, websiteurl FROM feeds")

    for row in cursor:
        try:
            print(row[1])
            download(row[1], row[0])
        except Exception as e:
            print(e)
            print("Error processing feed: --------------------------------------------" + row[1])
            pass
    cursor.close()  