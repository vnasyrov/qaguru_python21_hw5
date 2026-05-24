```python
from selene import browser, have, be, command
from selenium import webdriver
from pathlib import Path
from datetime import datetime
import os
```

# Указать браузер по имени
```python
from selene import browser

browser.config.driver_name = 'chrome'              # указать Chrome
browser.config.driver_name = 'firefox'             # указать Firefox
browser.config.driver_name = 'edge'                # указать Edge
```

# Передать драйвер с опциями
```python
from selene import browser
from selenium import webdriver

# Chrome
options = webdriver.ChromeOptions()                # создаём опции для Chrome
options.add_argument('--headless')                 # запуск без открытия окна браузера
options.add_argument('--window-size=1920,1080')    # размер окна
driver = webdriver.Chrome(options=options)         # создаём драйвер с опциями
browser.config.driver = driver                     # передаём драйвер в Selene

# Firefox
options = webdriver.FirefoxOptions()               # создаём опции для Firefox
options.add_argument('--headless')                 # запуск без открытия окна браузера
options.add_argument('--width=1920')               # ширина окна
options.add_argument('--height=1080')              # высота окна
driver = webdriver.Firefox(options=options)        # создаём драйвер с опциями
browser.config.driver = driver                     # передаём драйвер в Selene

# Edge
options = webdriver.EdgeOptions()                  # создаём опции для Edge
options.add_argument('--headless')                 # запуск без открытия окна браузера
options.add_argument('--window-size=1920,1080')    # размер окна
driver = webdriver.Edge(options=options)           # создаём драйвер с опциями
browser.config.driver = driver                     # передаём драйвер в Selene
```

# Поиск элементов > Один элемент
```python
from selene import browser

browser.element('.main-header')                             # найдёт первый элемент с классом main-header
browser.element('.main-header').element('.sub-header')      # найдёт .sub-header внутри .main-header
browser.element('#output #currentAddress')                  # найдёт #currentAddress внутри #output (через пробел)
browser.element('#output').element('#currentAddress')       # то же самое, но цепочкой
```

# Поиск элементов > Несколько элементов
```python
from selene import browser

browser.all('.main-header')                                 # найдёт ВСЕ элементы с классом main-header
browser.all('.main-header').first                           # первый элемент (индекс 0)
browser.all('.main-header')[0]                              # первый элемент (то же самое)
browser.all('.main-header').second                          # второй элемент (индекс 1)
browser.all('.main-header')[1]                              # второй элемент (то же самое)
```

# Поиск элементов > Дубли id
```python
from selene import browser

# Если несколько элементов имеют одинаковый id - берём нужный по номеру
browser.all('#currentAddress').first                        # первый элемент с id=currentAddress
browser.all('#currentAddress').second                       # второй элемент с id=currentAddress

# Или ищем внутри родительского элемента
browser.element('#output #currentAddress')                  # ищем #currentAddress внутри #output
browser.element('#output').element('#currentAddress')       # то же самое, но цепочкой
```

# Ввод текста
```python
from selene import browser

browser.element('#firstName').type('Иванов Иван')           # ввод текста по одной букве (как пользователь)
browser.element('#firstName').set_value('Иванов Иван')      # ввод текста сразу через JS (быстрее)
```

# Использование have.be и have.js_property
```python
from selene import browser, have, be

# Текст на странице      -> have.text
# Значение поля          -> have.value
# Атрибут в HTML         -> have.attribute
# Чекбокс/радиокнопка    -> have.js_property('checked', True/False)
# Поле заблокировано     -> have.js_property('disabled', True/False)
# Поле только для чтения -> have.js_property('readOnly', True/False)
# Элемент скрыт          -> have.js_property('hidden', True/False)

browser.element('#submit').should(be.disabled)      # элемент заблокирован
browser.element('#submit').should(be.enabled)       # элемент доступен
browser.element('#submit').should(be.visible)       # элемент виден
browser.element('#submit').should(be.hidden)        # элемент скрыт
browser.element('#checkbox').should(be.selected)    # чекбокс/радиокнопка выбраны

# be.disabled  - проверяет HTML атрибут disabled - просто и читабельно
# js_property  - проверяет текущее состояние через JavaScript - надёжнее
# если be не справляется (элемент заблокирован через JS но нет атрибута disabled) - используй js_property
```

# Время ожидания
```python
from selene import browser, have

browser.config.timeout = 20.0                                       # глобальное время ожидания (по умолчанию 4 сек)

browser.element('#firstName').with_(timeout=15).should(             # время ожидания только для этого элемента
    have.value('Иванов Иван')                                       # приоритет выше глобального
)
```

# Команды command.
```python
from selene import browser, command

browser.element('element').perform(command.js.click)                # клик по элементу через JS
                                                                    # игнорирует перекрывающие элементы
                                                                    # например рекламный баннер на demoqa.com
browser.element('element').perform(command.js.scroll_into_view)     # прокрутка страницы до элемента

# Так не работает - perform() возвращает None, нельзя цеплять .click()
browser.element('#submit').perform(command.js.scroll_into_view).click()

# Правильно - разбить на две строки
browser.element('#submit').perform(command.js.scroll_into_view)
browser.element('#submit').click()

# Или использовать JS клик - он сам скроллит и игнорирует перекрывающие элементы
browser.element('#submit').perform(command.js.click)
```

# Изменение масштаба страницы
```python
from selene import browser

browser.driver.execute_script(
    "document.querySelector('.body-height').style.transform='scale(.65)'"   # уменьшение масштаба до 65%
)
```

# Загрузка файла > Есть тег input type = 'file'
```python
from selene import browser

browser.element('#uploadPicture').send_keys(os.path.abspath('picture.png'))  # файл лежит рядом с тестом
```

# Загрузка файла > Нет тега input type = 'file'
```python
from selene import browser

browser.element('#uploadPicture').perform(
    command.js.drop_file(os.path.abspath('img.png'))                        # загрузка через JS
)
```

# Загрузка файла > Универсальный способ через utils.py
```python
from selene import browser
from pathlib import Path

# Структура проекта:
# python_hw5_selene_basics/              <- корень проекта
# ├── utils.py                      <- сюда кладём функцию path
# ├── conftest.py                   <- фикстуры
# ├── tests/
# │   └── test_demoqa_form.py       <- наш тест
# └── resources/                    <- сюда кладём файлы для тестов
#     └── 1.jpg                     <- наше изображение

# utils.py
def path(file_name):                # file_name - параметр (имя файла передаётся снаружи при вызове)
    return str(
        Path(__file__).parent               # /hw5_selene_basics/ - выходим из файла в папку
                                            # один parent - так как utils.py лежит в корне проекта
        .joinpath(f'resources/{file_name}') # f'resources/{file_name}' - это f-строка
                                            # буква f перед кавычками означает что всё что в {}
                                            # будет заменено на значение параметра file_name
                                            # например: /python_hw5_selene_basics/resources/1.jpg
    )

# если бы функция лежала в tests/test_demoqa_form.py - нужно два parent
def path(file_name):
    return str(
        Path(__file__).parent.parent        # /python_hw5_selene_basics/tests/ -> /python_hw5_selene_basics/
        .joinpath(f'resources/{file_name}') # /python_hw5_selene_basics/resources/1.jpg
    )

# используем в тесте test_demoqa_form.py
from utils import path                                               # импортируем функцию из utils.py
browser.element('#uploadPicture').send_keys(path('1.jpg'))          # '1.jpg' подставится вместо
                                                                     # {file_name} в f-строке
```

# Работа со слайдером > Смещение в пикселях
```python
from selene import browser, command

browser.element('element').perform(
    command.drag_and_drop_by_offset(x=277, y=0)         # перемещение на 277px вправо
)
browser.element('element').perform(
    command.drag_and_drop_by_offset(x=-277, y=0)        # перемещение на 277px влево
)
```

# Работа со слайдером > Перемещение к элементу
```python
from selene import browser, command

browser.element('element').perform(
    command.drag_and_drop_to('element2')                # element - что перемещаем
                                                        # element2 - куда перемещаем
)
```

# Работа с датами > Форматирование
```python

# важно импортировать именно так - иначе будет ошибка: AttributeError: module 'datetime' has no attribute 'today'
from datetime import datetime

today = datetime.today()            # получаем сегодняшнюю дату и время: 2026-05-24 14:30:00

# Коды форматирования:
# %d - день числом (24)
# %B - месяц полным словом (May)       <- большая буква = полный вариант
# %b - месяц сокращённо (May, Jan)     <- маленькая буква = короткий вариант
# %Y - год полностью (2026)            <- большая буква = полный вариант
# %y - год сокращённо (26)             <- маленькая буква = короткий вариант
# %m - месяц цифрой (05)

today.strftime('%d %B %Y')          # '24 May 2026'  - день месяц(словом) год
today.strftime('%d %b %Y')          # '24 May 2026'  - сокращённый месяц
today.strftime('%d %m %Y')          # '24 05 2026'   - месяц цифрой
today.strftime('%d %B %y')          # '24 May 26'    - короткий год
```

# Работа с датами > Динамическая проверка
```python
from selene import browser, have
from datetime import datetime

# Так писать нельзя - тест будет падать каждый день!
browser.element('#dateOfBirthInput').should(have.value('24 May 2026'))

# Правильно - генерируем дату динамически
today = datetime.today().strftime('%d %B %Y')
browser.element('#dateOfBirthInput').should(have.value(today))          # каждый день дата актуальна
```

# Работа с датами > Выбор через календарь
```python
from selene import browser, have

browser.element('#dateOfBirthInput').click()                            # открываем календарь

# Выбираем месяц (счёт идёт с 0!)
# option[value="0"]  - January     option[value="6"]  - July
# option[value="1"]  - February    option[value="7"]  - August
# option[value="2"]  - March       option[value="8"]  - September
# option[value="3"]  - April       option[value="9"]  - October
# option[value="4"]  - May         option[value="10"] - November
# option[value="5"]  - June        option[value="11"] - December

browser.element('.react-datepicker__month-select').element('option[value="6"]').click()     # июль
browser.element('.react-datepicker__year-select').element('option[value="1993"]').click()   # год
browser.element('.react-datepicker__day--012').click()                                      # 12 число

browser.element('#dateOfBirthInput').should(have.value('12 Jul 1993'))  # проверяем результат
```

# Работа с датами > Хранение в переменной
```python
from selene import browser, have
from datetime import datetime

today = datetime.today().strftime('%d %B %Y')
browser.element('#dateOfBirthInput').set_value(today)                   # вводим
browser.element('#dateOfBirthInput').should(have.value(today))          # проверяем то же самое значение
```
