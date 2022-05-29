import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os


def sale_category(url):
    '''на вход получает список ["имя категории товаров", "ссылка на катеорию товаров", "page_name"] и:
     -находит список всех страниц с акционными товарами выбранной категории
     -запускает функцию по поиску акционных товаров с каждой страницы
     -запускает функцию для записи данных в excel и открытия файла в редакторе excel'''

    try:
        os.mkdir(f'categories/{url[2]}')
    except FileExistsError:
        pass

    page_store = urlopen(url[1]).read().decode(
        'utf-8')

    with open(f"categories/{url[2]}/{url[2]}.html", 'w', encoding='utf-8') as html_file:
        html_file.write(page_store)

    with open(f"categories/{url[2]}/{url[2]}.html", 'r', encoding='utf-8') as page_html:
        page_category = page_html.read()

    soup_store = BeautifulSoup(page_category, 'html.parser')

    # находим все страницы с акциями в данной категории:
    all_sales_pages = soup_store.find_all(class_="pagination-point active")
    href_sp = {'1': [url[1], url[2]]}
    all_names_in_category = []
    all_list_prices_in_category = []
    all_href_prod_in_category = []
    for sp in all_sales_pages:
        href_sp[sp.text] = [f"http://7745.by{sp['href']}", url[2]]
    for i, g in href_sp.items():
        page_i = for_every_page_category(i, g)
        for name in page_i[0]:
            all_names_in_category.append(name)
        for price in page_i[1]:
            all_list_prices_in_category.append(price)
        for href in page_i[2]:
            all_href_prod_in_category.append(href)
    writer([all_names_in_category, all_list_prices_in_category, all_href_prod_in_category, url[2], url[0]])


def for_every_page_category(i, g):
    '''получает в качестве аргументов название для временной страницы и ссылку на страницу.
    находит акционные товары на странице и возвращает список ["имя товара", "акция", "ссылка на товар"]'''

    page_store = urlopen(g[0]).read().decode(
        'utf-8')

    with open(f"categories/{g[1]}/{i}.html", 'w', encoding='utf-8') as html_file:
        html_file.write(page_store)

    with open(f"categories/{g[1]}/{i}.html", 'r', encoding='utf-8') as page_html:
        page_category = page_html.read()
    soup_category = BeautifulSoup(page_category, 'html.parser')
    tag_names_products = soup_category.find_all('a', "item-block_name item-block_name--tile")

    names_products = []  # -> список наименований акционных товаров
    list_prices = []  # -> список цен акционных товаров
    href_products = []  # -> список ссылок акционных товаров

    for n in tag_names_products:
        list_prices_n = []
        name = n.text
        names_products.append(name)
        container = n.parent.parent.parent
        price_1 = container.find_all(class_="price-summary_title-cell")
        href_products.append(f"http://7745.by/{n['href']}")

        for p in price_1:
            value_price = p.text
            price = ''.join(p.find_next().text.split())
            prices = f'{value_price[:-1]} = {price}'
            list_prices_n.append(prices)

        list_prices.append(list_prices_n)
    return [names_products, list_prices, href_products]


def all_sale_categori():
    '''функция для кнопки "все категории"
    находит ссылки на все категории, проходит по ним и возвращает список
    ["имя товара", "акция", "ссылка на товар", "имя категории"]'''

    with open('sale_page.html', 'r', encoding='utf-8') as file:
        sale_page = file.read()

    # Готовим суп:
    soup_store = BeautifulSoup(sale_page, 'html.parser')
    # print(soup_store)

    # Находим все различные направления акций:
    pages_sales = soup_store.find_all('a', class_="sales-list__item")

    # Работае с полученным списком акций:
    all_categorise = [] # -> создаём список списков категорий акций для кнопок "Название категории, ссылка"
    writer_list = [] #-> список для записи в excel

    for page in pages_sales:
        href_art = 'https://7745.by' + page.attrs['href']  # -> получаем ссылки на страницы с акциями
        categories_name = page.find('div',
                                   class_="sales-list__title").contents  # -> получаем имя категории на русском, для названия кнопок
        name_categorie=categories_name[0]
        page_name = page.attrs['href'].replace('/sale/', '').replace('-',
                                                                     '_')  # -> получаем название для временного файла
        all_categorise.append([name_categorie, href_art, page_name])

    for category in all_categorise:
        try:
            os.mkdir(f'categories/{category[2]}')
        except FileExistsError:
            pass

        page_store = urlopen(category[1]).read().decode(
            'utf-8')

        with open(f"categories/{category[2]}/{category[2]}.html", 'w', encoding='utf-8') as html_file:
            html_file.write(page_store)

        with open(f"categories/{category[2]}/{category[2]}.html", 'r', encoding='utf-8') as page_html:
            page_category = page_html.read()

        soup_store = BeautifulSoup(page_category, 'html.parser')

        # находим все страницы с акциями в данной категории:
        all_sales_pages = soup_store.find_all(class_="pagination-point active")
        href_sp = {'1': [category[1], category[2]]}
        all_names_in_category = []
        all_list_prices_in_category = []
        all_href_prod_in_category = []
        for sp in all_sales_pages:
            href_sp[sp.text] = [f"http://7745.by{sp['href']}", category[2]]
        for i, g in href_sp.items():
            page_i = for_every_page_category(i, g)
            for name in page_i[0]:
                all_names_in_category.append(name)
            for price in page_i[1]:
                all_list_prices_in_category.append(price)
            for href in page_i[2]:
                all_href_prod_in_category.append(href)
        writer_list.append([all_names_in_category, all_list_prices_in_category, all_href_prod_in_category, category[2], category[0]])
    writer_all(writer_list)

def writer(list_for_write):
    '''записывает данные в excel-файл и запускает его в редакторе'''

    # составляю словарь для записи в excel:
    df = pd.DataFrame(
        {'Наменование товара': list_for_write[0], 'Описание акции': list_for_write[1], 'Ссылка': list_for_write[2]})
    with pd.ExcelWriter(f'categories/excel/{list_for_write[3]}.xlsx', engine='xlsxwriter') as wb:
        df.to_excel(wb, index=False, sheet_name=list_for_write[4])
        sheet = wb.sheets[list_for_write[4]]
        sheet.set_column('A:B', 60)
        sheet.set_column('B:C', 80)

    # запускает excel файл:
    dir_project = os.getcwd()
    excel_file = dir_project + f'\\categories\\excel\\{list_for_write[3]}.xlsx'
    os.system(excel_file)


def writer_all(list_for_write):
    '''записывает данные в excel-файл и запускает его в редакторе'''

    with pd.ExcelWriter(f'categories/excel/all_sales_products.xlsx', engine='xlsxwriter') as wb:
        for list in list_for_write: #-> цикл по гигантскому списку всех категорий
            df = pd.DataFrame(
                {'Наменование товара': list[0], 'Описание акции':list[1], 'Ссылка': list[2]})
            df.to_excel(wb, index=False, sheet_name=list[4])
            sheet = wb.sheets[list[4]]
            sheet.set_column('A:B', 60)
            sheet.set_column('B:C', 80)
    #
    # запускает excel файл:
    dir_project = os.getcwd()
    excel_file = dir_project + f'\\categories\\excel\\all_sales_products.xlsx'
    os.system(excel_file)