from bs4 import BeautifulSoup
from urllib.request import urlopen


def get_sale(url='https://7745.by/sale/'):
    '''эта функция запускается со старта приложения, создаёт список категорий и возвращает список кнопок,
     которые соответствуют категориям акций'''
    page_store = urlopen(url).read().decode('utf-8')  # -> получаем содержимое страницы

    # Записываем страницу в файл, чтобы не мучить сайт и не получить бан, а в дальнейшем работать по полученному файлу:
    with open('sale_page.html', 'w', encoding='utf-8') as file:
        file.write(page_store)

    # Читаем полученный файл:
    with open('sale_page.html', 'r', encoding='utf-8') as file:
        sale_page = file.read()

    # Готовим суп:
    soup_store = BeautifulSoup(sale_page, 'html.parser')
    # print(soup_store)

    # Находим все различные направления акций:
    pages_sales = soup_store.find_all('a', class_="sales-list__item")

    # Работае с полученным списком акций:
    pages_sales_list = []  # -> создаём список списков категорий акций для кнопок "Название категории, ссылка, колонка,ряд "
    all_categorise_href = []

    column = 1
    row = 2
    for page in pages_sales:
        href_art = 'https://7745.by' + page.attrs['href']  # -> получаем ссылки на страницы с акциями
        all_categorise_href.append(href_art)
        page_name = page.attrs['href'].replace('/sale/', '').replace('-',
                                                                     '_')  # -> получаем название для временного файла
        name_categorie = page.find('div',
                                   class_="sales-list__title").contents  # -> получаем имя категории на русском, для названия кнопок

        # Заносим данные необходимые для кнопок в список кнопок:
        for name in name_categorie:
            if row <= 8:
                pages_sales_list.append([name, href_art, column, row, page_name])
                row += 1
            else:
                row = 0
                column += 1
                pages_sales_list.append([name, href_art, column, row, page_name])

    return pages_sales_list  # -> возвращаем список кнопок


