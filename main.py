import requests
import pandas as pd
from bs4 import BeautifulSoup
import openpyxl

def get_half_string(s):
    # Obliczamy połowę długości napisu
    half_length = len(s) // 2
    # Zwracamy pierwszą połowę napisu
    return s[:half_length]


def save_dataframe_to_csv(df, file_path):
    """
    Zapisuje DataFrame do pliku CSV.

    Parameters:
    df (pandas.DataFrame): DataFrame, który chcemy zapisać.
    file_path (str): Ścieżka do pliku CSV (z rozszerzeniem .csv), gdzie ma zostać zapisany DataFrame.
    """
    try:
        # Zapisz DataFrame do pliku CSV
        df.to_csv(file_path, encoding='utf-8', index=False)  # index=False, jeśli nie chcesz zapisywać indeksów
        print(f'DataFrame został zapisany w pliku: {file_path}')
    except Exception as e:
        print(f'Wystąpił błąd podczas zapisywania pliku: {e}')


def save_dataframe_to_excel(df, file_path):
    """
    Zapisuje DataFrame do pliku Excel.

    Parameters:
    df (pandas.DataFrame): DataFrame, który chcemy zapisać.
    file_path (str): Ścieżka do pliku Excel (z rozszerzeniem .xlsx), gdzie ma zostać zapisany DataFrame.
    """
    try:
        # Zapisz DataFrame do pliku Excel
        df.to_excel(file_path, index=False)  # index=False, jeśli nie chcesz zapisywać indeksów
        print(f'DataFrame został zapisany w pliku: {file_path}')
    except Exception as e:
        print(f'Wystąpił błąd podczas zapisywania pliku: {e}')


def get_titles():
    url = 'https://edukacja.um.warszawa.pl/szkoly-i-placowki/szkoly-publiczne/prowadzone-przez-m-st-warszawa?_AssetPublisher_ldd4BO81G5zj_f_list_109153861__109153866__field1=liceum+og%C3%B3lnokszta%C5%82c%C4%85ce&_AssetPublisher_ldd4BO81G5zj_cur=8'

    response = requests.get(url, verify=False)
    html_content = response.content


    soup = BeautifulSoup(html_content, 'html.parser')

    table = soup.find('table', class_="table table-striped")
    headers = table.find_all("th")
    titles = []
    # print(headers)
    for i in headers:
        title = i.text
        titles.append(title)

    for index, el in enumerate(titles):
        titles[index] = el.replace('\n', '').replace('Sortuj dane po kolumnie', '').replace('/ jednostki\n\n\n', '')

    titles = [get_half_string(i) for i in titles]
    return titles


def fill_df(titles):
    df = pd.DataFrame(columns=titles)
    for i in range(1, 9):

        url = 'https://edukacja.um.warszawa.pl/szkoly-i-placowki/szkoly-publiczne/prowadzone-przez-m-st-warszawa?_AssetPublisher_ldd4BO81G5zj_f_list_109153861__109153866__field1=liceum+og%C3%B3lnokszta%C5%82c%C4%85ce&_AssetPublisher_ldd4BO81G5zj_cur='
        url += str(i)
        response = requests.get(url, verify=False)
        html_content = response.content


        soup = BeautifulSoup(html_content, 'html.parser')

        # Znajdź tabele
        table = soup.find('table', class_="table table-striped")

        rows = table.find_all("tr")
        # print(rows)
        for i in rows[1:]:
            data = i.find_all("td")
            row = [tr.text for tr in data]

            for index, el in enumerate(row):
                row[index] = el.replace('\nNazwa szkoły/ jednostki:', '').replace('\n', '').replace('Typ placówki:',
                                                                                                    '').replace('  ',
                                                                                                                '').replace(
                    'Dzielnica:', '').replace('Adres:', '').replace('Telefon:', '').replace('WWW:', '').replace('E-mail:', '')
            df.loc[len(df)] = row
    return df

titles = get_titles()
df = fill_df(titles)
save_dataframe_to_excel(df, 'dane_licea_w_warszawie.xlsx')
save_dataframe_to_csv(df, 'dane_licea_w_warszawie.csv')

