import requests
from multiprocessing import Pool
import os
cwd = os.getcwd()
import time
def initializer():
    global data
    myfile_akun = open(f"./env.txt","r")
    data = myfile_akun.read()
    
def generator(id):
    headers = {
        'authority': 'api.products.aspose.app',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8,id;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://products.aspose.app',
        'referer': 'https://products.aspose.app/',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }


    params = {
            'culture': 'id',
            }
    datas = {
            'barcodetype': data,
            'content': id,
            'filetype': 'PNG',
            'showCodeText': 'true',
            'filesize': '1',
            }
    
    response = requests.post('https://api.products.aspose.app/barcode/generate/generatebarcode', params=params, headers=headers, data=datas).json()
    getImg = requests.get(f"https://api.products.aspose.app/{response['downloadPath']}")
    if os.path.exists(f'{cwd}/img') == False:
        os.mkdir(f'{cwd}/img')
    if getImg.status_code == 200:
        with open(f"{cwd}/img/{id}.jpg", 'wb') as f:
            f.write(getImg.content)
    print(f"[{time.strftime('%d-%m-%y %X')}] Success Generate: {id}")
    
if __name__ == '__main__':
    global list_accountsplit
    global url
    print(f"[{time.strftime('%d-%m-%y %X')}] Automation Barcodes") 
    file_list_akun = "data.txt"
    myfile_akun = open(f"{cwd}/{file_list_akun}","r")
    akun = myfile_akun.read()
    list_accountsplit = akun.split("\n")
    target = input(f"[{time.strftime('%d-%m-%y %X')}] Code Type: ")
    with open('env.txt','w') as f: f.write(f'{target}')
    jumlah = int(input(f"[{time.strftime('%d-%m-%y %X')}] Multi Processing: "))
    with Pool(jumlah,initializer) as p:  
        p.map(generator, list_accountsplit)
