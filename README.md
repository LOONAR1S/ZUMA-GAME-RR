# Zuma

## Описание
Данное приложение является реализацией компьютерной игры «Zuma Deluxe».

Автор: Жукова Дарья

## Требования
* Python 3.8
* pygame

## Состав
* Графическая версия: `main.py`
* Модули: `game/`
* Тесты: `tests.py`
* Изображения: `game/images/`
* Шрифты: `game/fonts/`

## Пример запуска: 
Windows:
`python main.py`
Linux:
`python3 main.py`

## Подробности реализации
Основной файл - main.py. В нём находится основной класс игры `Game` и вспомогательный класс `Level`.
В папке game находятся необходимые для игры модули. 
* `BallGenerator` ответственнен за генерацию и хранение мячей, а так же произведение различных операций над цепочкой мячей
* `ShootingManager` ответственнен за выстрелы
* `BonusManager` ответственнен за генерацию и реализацию бонусов
* `ScoreManager`ответственнен за хранение и подсчет очков и жизней
* `Sprites` хранит все необходимые для игры спрайты (`Player`, `Ball`, `ShootingBall`, `Finish`)
* `Path`генерирует путь в зависимости от текущего уровня
* `Params` хранит в себе все нужные для игры константы
* `ui`ответственнен за отрисову экрана и его составляющих

## Тестирование
На модули в папке game написаны тесты в файле test.py. Покрытие строк составляет 46%