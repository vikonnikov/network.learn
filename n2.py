# -*- coding: utf8 -*-

# Код написан по мотиву статьи с Хабра
#
# --- *** Нейросети для чайников. Часть 2 — Перцептрон *** ---
# --- *** https://habrahabr.ru/post/144881/ *** ---
#
# Допустим что мы обучаем нашу сеть распознавать только цифру 5
# По очереди вводим цифры от 0 до 9
# Приложение загружает изображение, соответствующее введенной цифре
# Далее отвечаем на вопрос приложения, правильно ли оно определило букву
# Вводим цифры до тех пор пока сеть не начнет распознавать цифру 5
# и отличать её от всех остальных цифр

import os
import numpy
from PIL import Image, ImageDraw, ImageFont

DIMENTIONS = (26, 18) # Размер изображения
DIRLIB = './lib' # Директория с изображениями
FONTPATH = "arial.ttf"
FONTSIZE = 30 # Размер шрифта

WIIGHTFILE = 'weights.txt' # Файл с весами нейрона
LIMIT = 100 # Некоторый коэффициент, подобранный случайно

class Neuron:
    """Нейрон"""
    filename = 'weights.txt' # Файл с весами нейрона
    def __init__(self):
        self.weights = self.load_weights() # Загружаем веса из файла

    def identify(self, digit):
        """Пытаемся идентифицировать цифру"""
        multiple = digit * self.weights # умножение сигнала на вес
        summ = numpy.sum(multiple) # суммирование входных сигналов

        return summ >= LIMIT # сравнение с порогом

    def load_weights(self):
        """Загружаем веса из файла"""
        if os.path.exists(WIIGHTFILE):
            return numpy.loadtxt(WIIGHTFILE)
        else:
            return numpy.zeros(DIMENTIONS) # Если файла весов нет, тогда инициализируем их нулями

    def save_weights(self):
        """Сохраняем веса в файл"""
        numpy.savetxt(WIIGHTFILE, self.weights, fmt='%d')

    def tune(self, result, digit):
        """Подстраиваем веса нейрона.
        Метод вызывается в том случае, если мы "говорим" алгоритму о том, что он отработал неверно.

        result - реазультат идентификации
        digit - цифра загруженная из файла"""
        if result:
            self.weights -= digit
        else:
            self.weights += digit

class Network:
    """Сеть, состоящая из одного нейрона"""
    def __init__(self):
        self.neuron = Neuron()

    def teach(self):
        """Обучаем нейронную сеть"""
        while True:
            try:
                digit = self.load(raw_input('digit -> '))
            except EOFError:
                # Выход по CTRL + Z
                self.neuron.save_weights()
                break
            else:
                result = self.neuron.identify(digit)
                answer = raw_input("Is %sdigit 5, rigth? Type yes/no -> " % ('' if result else 'not ')).lower()

                if answer == 'yes': # Алгоритм предложил нам верный ответ
                    pass
                elif answer == 'no': # Неверный ответ
                    self.neuron.tune(result, digit)

    def load(self, digit):
        """Загружаем цифру из файла"""
        path = os.path.join(DIRLIB, '%s.png' % digit)
        img = Image.open(path)
        array = numpy.array(img)

        # Преобразуем матрицу с цветами пикселов
        # закрашенный пиксель = 1, белый = 0
        check = lambda color: 0 if color >= 250 else 1

        self.map(array, check)

        return array

    def map(self, array, func):
        """Применяем функцию к каждому элементу 2D-массива"""
        for i in xrange(DIMENTIONS[0]):
            for j in xrange(DIMENTIONS[1]):
                array[i][j] = func(array[i][j])

class App:
    """Класс приложения"""
    def __init__(self):
        # self.generate()
        # Расскомментировать, если необходимо генерировать цифры
        # В директорию тогда нужно положить файл со шрифтом "arial.ttf"

        self.network = Network()

    def run(self):
        """Запуск приложение"""
        self.network.teach()

    def generate(self):
        """Генерируем изображения с цифрами от 0 до 9"""
        if not os.path.exists(DIRLIB):
            os.mkdir(DIRLIB)

        for digit in range(10):
            path = os.path.join(DIRLIB, '%s.png' % digit)

            img = Image.new("L", DIMENTIONS[::-1], "white")
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(FONTPATH, FONTSIZE)
            draw.text((0, -3), str(digit), 0, font=font)
            img.save(path)

if __name__ == "__main__":
    app = App()
    app.run()