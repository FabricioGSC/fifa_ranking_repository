from operator import concat
import os
import csv
import requests

from bs4 import BeautifulSoup

months = {'jan':'01','feb':'02','mar':'03','apr':'04','may':'05','jun':'06','jul':'07','aug':'08','sept':'09','oct':'10','nov': '11', 'dec':'12'}

def convert(origin: str):
    __proccess(origin)

def __proccess(origin: str):
    for i in os.listdir(f'{origin}/'):
        folder_abs_path = f'{os.getcwd()}/{origin}/{i}'
        if(os.path.isdir(folder_abs_path)):
            print(folder_abs_path)
            success = __convert_all_files(folder_abs_path, i, origin)
            if(success):
                __remove_processed_files(folder_abs_path)

def change_order_name(name: str):
    sp = name.split('_')
    return f'{sp[2]}_{__get_number_of_month(sp[1])}_{sp[0]}'

def __get_number_of_month(month: str):
   return months.get(month.lower())

def __convert_all_files(path: str, folder_name: str, origin: str) -> bool:
    print(f'Ready to convert all files in {path} - {folder_name}')
    try:
        file = open(f'{origin}.csv', 'a')
        csv_writer = csv.writer(file)
        
        list_html_files = os.listdir(path)
        list_html_files.sort()

        for arq in list_html_files:
            if(arq.endswith('.html')):
                html_file = open(f'{path}/{arq}', 'r')
                soup = BeautifulSoup(html_file, 'html.parser')
                for table_index, table_line in enumerate(soup.find_all('tr')):
                    if table_index > 0:
                        line = []
                        line.append(change_order_name(folder_name).replace('_','-'))
                        img_col = None
                        for idx, col in enumerate(table_line.find_all('td')):
                            if(idx == 1):
                                img_col = col
                            elif(idx == 2):
                                team, abr = __adjust_team(col)
                                __create_image(img_col,abr)
                                line.append(team)
                                line.append(abr)
                            elif(idx == 6):
                                line.append(__adjust_variations(col))
                            elif(not idx == 7):
                                line.append(col.get_text())
                        
                        if(len(line) > 0):
                            csv_writer.writerow(line)
                
        file.close()
        return True
    except Exception as e:
        print("ERRO ", e)
        return False
        
def __adjust_team(col):
    return [span.get_text() for span in col.find_all('span')]

def __create_image(col,abr):
    for img in col.find_all('img'):
        if not os.path.isfile('dataset/img/'+abr+'.webp'):
            response = requests.get(img['src'])
            file = open('dataset/img/'+abr+'.webp', "wb")
            file.write(response.content)
            file.close()
        return 'dataset/img/'+abr+'.webp'

def __adjust_variations(col):
    for div in col.find_all('div'):
        try:
            aria:str = div['aria-label']
            if('up' in aria):
                return 'up'
            elif('down' in aria):
                return 'down'
            else:
                return '-'
        except: 
            pass
    
    return '-'

def __adjust_team(col):
    return [span.get_text() for span in col.find_all('span')]

def __remove_processed_files(path: str):
    for file in os.listdir(path):
        print(f"Removing {file}")
        os.remove(f'{path}/{file}')
    
    os.removedirs(path)

if __name__ == '__main__':
    convert()