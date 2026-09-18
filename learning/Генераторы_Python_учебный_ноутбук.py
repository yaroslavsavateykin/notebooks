import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Генераторы в Python: учебный ноутбук (очень подробно)

    Этот ноутбук — пошаговое руководство, чтобы **понять “на ощущениях”**, что такое генераторы, зачем они нужны и как ими пользоваться.

    **Что ты получишь в конце:**
    - чёткое понимание разницы: *итерируемое* → *итератор* → *генератор*;
    - уверенность в `yield`, `yield from`, генераторных выражениях;
    - практические паттерны: ленивые пайплайны, большие файлы, бесконечные последовательности;
    - “продвинутый уровень”: `send()`, `throw()`, `close()` и аккуратное завершение.

    > Совет: выполняй ячейки по порядку и иногда **меняй код** (это лучший способ “прочувствовать”).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 0. Быстрый ориентир

    **Слова, которые будут встречаться:**

    - **iterable (итерируемое)** — объект, по которому можно пройтись в цикле `for`.
      - Примеры: `list`, `tuple`, `str`, `dict`, `set`, `range`, файл, и т.д.
    - **iterator (итератор)** — объект, который *выдаёт элементы по одному* через `next()` и помнит своё состояние.
    - **generator (генератор)** — *удобный способ создать итератор* с помощью функции с `yield` (или генераторного выражения).

    Главная идея: **генераторы делают вычисления “ленивыми”** — значения создаются **по требованию**, а не заранее.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Итерация в Python под капотом

    Цикл

    ```python
    for x in something:
        ...
    ```

    примерно делает:

    ```python
    it = iter(something)     # получить итератор
    while True:
        try:
            x = next(it)     # взять следующий элемент
        except StopIteration:
            break
        ...
    ```

    Давай посмотрим это живьём.
    """)
    return


@app.cell
def _():
    _data = [10, 20, 30]
    it = iter(_data)
    print(it)
    print(next(it))  # это итератор
    print(next(it))
    # Следующий next(it) выбросит StopIteration
    print(next(it))
    return


@app.cell
def _():
    _data = [10, 20, 30]
    it_1 = iter(_data)
    for _i in it_1:
        print(_i)
    return (it_1,)


@app.cell
def _(it_1):
    try:
        print(next(it_1))
    except StopIteration as e:
        print('StopIteration пойман — итератор закончился.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Важный “факт ощущения”
    Итератор — это **одноразовый** объект: как только элементы закончились, он “пустой”.
    """)
    return


@app.cell
def _():
    it2 = iter([1, 2, 3])
    print(list(it2))  # "съели" итератор
    print(list(it2))  # второй раз уже нечего
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Где здесь генераторы?

    Генератор — это итератор, который обычно создают так:

    - **генераторная функция**: содержит `yield`
    - **генераторное выражение**: `(x*x for x in ...)`

    Начнём с сравнения “список сразу” vs “ленивый поток”.
    """)
    return


@app.cell
def _():
    def squares_list(n):
        return [_i * _i for _i in range(n)]  # создаёт сразу ВСЕ значения

    def squares_gen(n):
        for _i in range(n):
            yield (_i * _i)  # создаёт значения ПО ОДНОМУ
    print(squares_list(5))
    print(squares_gen(5))  # это не список!
    return (squares_gen,)


@app.cell
def _(squares_gen):
    _g = squares_gen(5)
    print('type:', type(_g))
    print(next(_g))
    print(next(_g))
    print(list(_g))  # доедаем оставшееся
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Что делает `yield`?

    `yield` **останавливает выполнение функции**, *возвращает значение наружу* и **запоминает место**, где остановились.

    Когда ты вызываешь `next()` снова — выполнение продолжается **сразу после `yield`**.
    """)
    return


@app.cell
def _():
    def demo():
        print('A: старт')
        yield 1
        print('B: после первого yield')
        yield 2
        print('C: после второго yield')
        yield 3
        print('D: конец')
    _g = demo()
    print('Создали генератор, но он ещё ничего не печатал.')
    print('next #1 ->', next(_g))
    print('next #2 ->', next(_g))
    print('next #3 ->', next(_g))
    try:
        print('next #4 ->', next(_g))
    except StopIteration:
        print('Генератор завершился (StopIteration).')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Генератор = “состояние + шаг выдачи”

    Обычно генераторы используют, когда:
    - данных много (не хочется держать всё в памяти),
    - вычисления дорогие (не хочется считать лишнее),
    - хочется строить “поток” преобразований (пайплайн).

    Давай почувствуем экономию памяти.
    """)
    return


@app.cell
def _():
    import sys
    n = 100000
    _lst = [_i for _i in range(n)]  # 100k, можно увеличить
    _gen = (_i for _i in range(n))
    print(type(_gen))
    print('Размер списка (байт):', sys.getsizeof(_lst))
    # Важно: getsizeof не считает память элементов списка — но уже видно,
    # что у генератора "контейнер" крошечный, а список ощутимее.
    print('Размер генератора (байт):', sys.getsizeof(_gen))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Простой практический паттерн: “поток преобразований”

    Сделаем пайплайн:
    1) взять числа
    2) отфильтровать
    3) преобразовать
    4) взять первые N

    Важно: **ни один шаг не будет хранить всё целиком**.
    """)
    return


@app.cell
def _():
    def numbers():
        _i = 0
        while True:
            yield _i
            _i = _i + 1

    def only_even(iterable):
        for x in iterable:
            if x % 2 == 0:
                yield x

    def square(iterable):
        for x in iterable:
            yield (x * x)

    def take(iterable, n):
        it = iter(iterable)
        for _ in range(n):
            yield next(it)
    pipeline = take(square(only_even(numbers())), 10)
    print(list(pipeline))
    return (take,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Обсуждение
    - `numbers()` — **бесконечный генератор**
    - `only_even()` и `square()` — генераторы, которые “оборачивают” другой поток
    - `take()` — ограничивает поток

    Такую композицию удобно читать, потому что каждый шаг прост.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Генераторные выражения

    Это “компактная форма” генератора:

    - список: `[expr for x in it if cond]`
    - генератор: `(expr for x in it if cond)`

    Разница ощущается по памяти и ленивости.
    """)
    return


@app.cell
def _():
    nums = range(10)
    _lst = [x * x for x in nums if x % 2 == 0]
    _gen = (x * x for x in nums if x % 2 == 0)
    print('list:', _lst)
    print('gen :', _gen)
    print('gen -> list:', list(_gen))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. `return` в генераторе и значение StopIteration

    В генераторной функции можно написать `return value`.
    Тогда генератор завершится, а `value` окажется внутри `StopIteration.value`.

    На практике это редко нужно, но полезно понимать.
    """)
    return


@app.cell
def _():
    def gen_with_return():
        yield 'шаг 1'
        yield 'шаг 2'
        return 'готово!'
    _g = gen_with_return()
    print(next(_g))
    print(next(_g))
    try:
        next(_g)
    except StopIteration as e:
        print('StopIteration.value =', e.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. `yield from`: делегирование генератора

    `yield from other_iterable` делает две вещи:
    1) выдаёт все элементы `other_iterable`
    2) аккуратно прокидывает `send/throw/close` (это важно для продвинутых случаев)

    Сравни “вручную” и через `yield from`.
    """)
    return


@app.cell
def _():
    def chain_manual(a, b):
        for x in a:
            yield x
        for x in b:
            yield x

    def chain_yield_from(a, b):
        yield from a
        yield from b
    _gen = chain_manual([1, 2], 'ab')
    print(next(_gen))
    print(next(_gen))
    print(next(_gen))
    print(next(_gen))
    print(list(chain_manual([1, 2], 'ab')))
    print(list(chain_yield_from([1, 2], 'ab')))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Реальная задача: читать большой файл построчно

    Файл в Python сам по себе — итерируемый объект: строки читаются **лениво**.

    Но часто хочется:
    - пропускать пустые строки,
    - убирать пробелы,
    - брать только первые N строк и т.д.

    Сделаем “streaming” обработку.
    """)
    return


@app.cell
def _():
    from pathlib import Path

    p = Path("demo_big_text.txt")
    p.write_text("\n".join([
        "  first  ",
        "",
        "second",
        "   third",
        "",
        "fourth"
    ]), encoding="utf-8")

    def clean_lines(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    yield line

    print(list(clean_lines(p)))
    return (p,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Важное замечание
    Генератор `clean_lines` открывает файл в `with` и **закрывает его сам** после завершения итерации.

    Но если ты **не доитерируешь** генератор, файл может оставаться открыт до сборки мусора.
    Ниже покажем, как гарантировать закрытие через `try/finally` и `close()`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Аккуратное завершение: `close()` и `finally`

    Когда ты вызываешь `g.close()`, в генератор бросается `GeneratorExit`.
    Если внутри есть `finally`, он выполнится.

    Это важно для ресурсов: файлы, соединения, блокировки.
    """)
    return


@app.cell
def _():
    def resource_demo():
        print('Открыли ресурс')
        try:
            yield 1
            yield 2
            yield 3
        finally:
            print('Закрыли ресурс (finally)')
    _g = resource_demo()
    print(next(_g))
    _g.close()  # досрочно закрыли
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Продвинутый режим: `send()` — генератор как корутина

    Обычный `next(g)` эквивалентен `g.send(None)`.

    Если внутри генератора есть выражение вида:

    ```python
    x = yield something
    ```

    то значение, отправленное через `.send(value)`, попадёт в переменную `x`.

    Это позволяет делать генераторы “приёмниками”.
    """)
    return


@app.cell
def _():
    def accumulator():
        total = 0
        while True:
            x = (yield total)  # выдаём текущее, а затем получаем новое через send()
            if x is None:
                continue
            total = total + x
    acc = accumulator()
    print('prime ->', next(acc))
    print('send 10 ->', acc.send(10))
    # "запуск" (prime): первый next/ send(None) до первого yield
    print('send 5  ->', acc.send(5))
    print('send 1  ->', acc.send(1))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Почему нужен “prime”?
    Пока генератор не дошёл до первого `yield`, ему “некуда” принимать значение.

    Поэтому обычно делают:
    - `next(gen)` один раз,
    - или пишут обёртку-декоратор для автозапуска (ниже).
    """)
    return


@app.cell
def _():
    from functools import wraps

    def coroutine(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            _g = func(*args, **kwargs)  # auto-prime
            next(_g)
            return _g
        return wrapper

    @coroutine
    def moving_average():
        values = []
        while True:
            x = (yield (sum(values) / len(values) if values else None))
            values.append(x)
    ma = moving_average()
    print(ma.send(10))
    print(ma.send(20))
    print(ma.send(30))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 11. `throw()` — бросить исключение внутрь генератора

    Иногда нужно “сигнализировать” генератору из внешнего кода:
    - “остановись”
    - “перейди в режим X”
    - “произошла ошибка”

    Тогда используют `g.throw(SomeError(...))`.
    """)
    return


@app.cell
def _():
    class StopNow(Exception):
        pass

    def controlled_counter():
        _i = 0
        try:
            while True:
                try:
                    yield _i
                    _i = _i + 1
                except ValueError:
                    _i = 0
        except StopNow:
            return 'остановили'
    _g = controlled_counter()
    print(next(_g), next(_g), next(_g))
    print('reset via throw(ValueError)')
    _g.throw(ValueError('reset'))
    print(next(_g), next(_g))
    try:
        _g.throw(StopNow())
    except StopIteration as e:
        print('Завершился, value:', e.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 12. Частые ошибки и как их “почувствовать”
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ошибка 1: “переиспользовать” генератор

    Генератор — одноразовый: если ты его “съел”, он пустой.
    Решение: **создавай новый** генератор или собирай в список (если объём нормальный).
    """)
    return


@app.cell
def _():
    def _gen():
        for _i in range(3):
            yield _i
    _g = _gen()
    print(list(_g))
    print(list(_g))
    print(list(_gen()))  # пусто  # новый генератор -> снова работает
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ошибка 2: “забыть, что генератор ленивый”

    Если внутри генератора есть `print`, ты увидишь его только при итерации.
    """)
    return


@app.cell
def _():
    def loud():
        print('создали?')
        yield 1
        print('после yield')
    _g = loud()
    print('пока тишина')
    print(next(_g))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ошибка 3: замыкания и “последнее значение” в генераторных выражениях

    Похожая ловушка встречается в лямбдах в цикле.
    С генераторами тоже можно неожиданно “поймать” переменную поздно.

    Сравни:
    """)
    return


@app.cell
def _():
    funcs = []
    for _i in range(3):
        funcs.append(lambda: _i)
    print([f() for f in funcs])
    funcs2 = []  # все 2
    for _i in range(3):
    # фикс: захватить значение через аргумент по умолчанию
        funcs2.append(lambda i=_i: _i)
    print([f() for f in funcs2])  # 0,1,2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 13. “Мини-проект”: свой `itertools` руками

    Сделаем несколько полезных генераторов:
    - `chunked(iterable, size)` — выдаёт куски списка/потока
    - `flatten(iterable_of_iterables)` — расплющивает
    - `unique(iterable)` — убирает повторы, сохраняя порядок
    """)
    return


@app.cell
def _():
    def chunked(iterable, size):
        if size <= 0:
            raise ValueError("size должен быть > 0")
        buf = []
        for x in iterable:
            buf.append(x)
            if len(buf) == size:
                yield buf
                buf = []
        if buf:
            yield buf

    def flatten(iterable_of_iterables):
        for it in iterable_of_iterables:
            yield from it

    def unique(iterable):
        seen = set()
        for x in iterable:
            if x not in seen:
                seen.add(x)
                yield x

    print(list(chunked(range(10), 3)))
    print(list(flatten([[1,2], [], [3], [4,5]])))
    print(list(unique([1,2,1,3,2,4,4,5])))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 14. Упражнения (сразу с проверкой)

    Сделай упражнения, изменяя код в ячейках. Подсказки будут в комментариях.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Упражнение 1
    Напиши генератор `fibs()` — бесконечный генератор чисел Фибоначчи:
    $0,1,1,2,3,5,8,\dots$

    А затем возьми первые 15 через `take()`.
    """)
    return


@app.cell
def _(take):
    def fibs():
        # TODO: реализуй
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

    print(list(take(fibs(), 15)))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Упражнение 2
    Напиши генератор `grep_lines(path, pattern)`, который:
    - читает файл построчно,
    - выдаёт только строки, содержащие `pattern`,
    - возвращает строки уже без `\n` на конце.

    Проверь на `demo_big_text.txt`.
    """)
    return


@app.cell
def _(p):
    def grep_lines(path, pattern):
        # TODO: реализуй
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if pattern in line:
                    yield line.rstrip("\n")

    print(list(grep_lines(p, "ir")))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Упражнение 3
    Сделай генератор `running_max(iterable)`, который выдаёт текущий максимум на каждом шаге.

    Пример:
    - вход: `2, 1, 5, 3`
    - выход: `2, 2, 5, 5`
    """)
    return


@app.cell
def _():
    def running_max(iterable):
        it = iter(iterable)
        current = next(it)
        yield current
        for x in it:
            if x > current:
                current = x
            yield current

    print(list(running_max([2, 1, 5, 3, 10, 7])))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 15. Короткая шпаргалка

    - `yield x` — “верни x и поставь функцию на паузу”
    - `next(g)` — получить следующий элемент
    - `for x in g:` — удобный перебор
    - `g.close()` — закрыть генератор (запустит `finally`)
    - `g.send(v)` — отправить значение внутрь (`x = yield ...`)
    - `g.throw(E)` — бросить исключение внутрь
    - `yield from it` — отдать управление другому итератору/генератору

    ---

    Если хочешь, можешь написать, **какие примеры тебе ближе** (парсинг логов, обработка CSV, чтение huge-файлов, обработка фотографий/метаданных, телеграм-бот), и я добавлю в ноутбук “практический блок” именно под твою задачу.
    """)
    return


if __name__ == "__main__":
    app.run()
