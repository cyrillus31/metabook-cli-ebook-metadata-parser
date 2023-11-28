# METABOOK <br> <p>(CLI e-book metadata parser)</p>

Реализовал CLI инструмент [metabook](Task_2/metabook/) для парсинга электронных книг форматов epub и fb2, с удобной архитектурой под расширение. 

Использованы только встроенные библиотеки: [argparse](https://docs.python.org/3/library/argparse.html), [xml](https://docs.python.org/3/library/xml.etree.elementtree.html). 

<br>

Описание функцианла иструмента:

```console
usage: E-book metadata parser [-h] [-v] filename [filename ...]

Returns title, author, publisher and date published from a specified EPUB or FB2

positional arguments:
  filename       insert a relative or absolute filepaths

options:
  -h, --help     show this help message and exit
  -v, --verbose  display additional information
```

<br>

### Архитектура 
Я поставил себе целью разработать поддерживаемое, тестируемое и удобно расширяемое приложение, соблюдая принципы SOLID, DRY, KISS.  
Класс [EbookParser](Task_2/metabook/ebparser.py) работает с интерфейсом [абстрактного класса](Task_2/metabook/ebook/abstract_ebook.py), представляющего электронную книгу, который требует реализации менеджера контекста (т.к. зачастую для парсинга книги ее требуется распаковать, а после парсинга почистить распакованные файлы) и метода `get_metadata()`, осуществляющего сам парсинг и возвращающего необходимые данные в датаклассе с модифицированным методом `__str__` для удобства вывода в **stdout**. В свою очередь, строчная репрезентация датакласса зависит от наличия флага `--verbose`, который добавляет к выводу информацию о языкe книги и ее описание.  


От [абстрактного класса Ebook](Task_2/metabook/ebook/abstract_ebook.py) наследуются классы, соответствующие поддерживаемым форматам электронных книг: [EPUB_book](Task_2/metabook/ebook/epub.py) и [FB2_book](Task_2/metabook/ebook/fb2.py). За создание объектов этих классов отвечает [фабрика](Task_2/metabook/ebook/ebook_factory.py). В случае с EPUB форматом, метод `__enter__` распаковывает файлы книги во временную папку, где метод `_find_opf` найдет файл с расширением .opf, содержащий метаданные книги для последующего парсинга, после чего метод `__exit__` удалит временную папку. В случае с форматом FB2, который не требует разархивации, метод `__enter__` просто возвращает self.   

<br>

### Запуск


```console
git clone https://github.com/cyrillus31/take-home-weborama.git
cd take-home-weborama/metabook/
```
К проекту прилагаются файлы для проверки работы программы:

```console
python main.py ../../Books/* --verbose
```
CLI инструмент может работать с абсолютными и относительными путями файлов и любым количеством аргументов.