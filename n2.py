# -*- coding: cp1251 -*-

# ��� ������� �� ������ ������ � �����
#
# --- *** ��������� ��� ��������. ����� 2 � ���������� *** ---
# --- *** https://habrahabr.ru/post/144881/ *** ---
#
# �������� ��� �� ������� ���� ���� ������������ ������ ����� 5
# �� ������� ������ ����� �� 0 �� 9
# ���������� ��������� �����������, ��������������� ��������� �����
# ����� �������� �� ������ ����������, ��������� �� ��� ���������� �����
# ������ ����� �� ��� ��� ���� ���� �� ������ ������������ ����� 5
# � �������� � �� ���� ��������� ����

import os
import numpy
from PIL import Image, ImageDraw, ImageFont

DIMENTIONS = (26, 18) # ������ �����������
DIRLIB = './lib' # ���������� � �������������
FONTPATH = "arial.ttf"
FONTSIZE = 30 # ������ ������

WIIGHTFILE = 'weights.txt' # ���� � ������ �������
LIMIT = 100 # ��������� �����������, ����������� ��������

class Neuron:
    """������"""
    filename = 'weights.txt' # ���� � ������ �������
    def __init__(self):
        self.weights = self.load_weights() # ��������� ���� �� �����

    def identify(self, digit):
        """�������� ���������������� �����"""
        multiple = digit * self.weights # ��������� ������� �� ���
        summ = numpy.sum(multiple) # ������������ ������� ��������

        return summ >= LIMIT # ��������� � �������

    def load_weights(self):
        """��������� ���� �� �����"""
        if os.path.exists(WIIGHTFILE):
            return numpy.loadtxt(WIIGHTFILE)
        else:
            return numpy.zeros(DIMENTIONS) # ���� ����� ����� ���, ����� �������������� �� ������

    def save_weights(self):
        """��������� ���� � ����"""
        numpy.savetxt(WIIGHTFILE, self.weights, fmt='%d')

    def tune(self, result, digit):
        """������������ ���� �������.
        ����� ���������� � ��� ������, ���� �� "�������" ��������� � ���, ��� �� ��������� �������.

        result - ���������� �������������
        digit - ����� ����������� �� �����"""
        if result:
            self.weights -= digit
        else:
            self.weights += digit

class Network:
    """����, ��������� �� ������ �������"""
    def __init__(self):
        self.neuron = Neuron()

    def teach(self):
        """������� ��������� ����"""
        while True:
            try:
                digit = self.load(raw_input('digit -> '))
            except EOFError:
                # ����� �� CTRL + Z
                self.neuron.save_weights()
                break
            else:
                result = self.neuron.identify(digit)
                answer = raw_input("Is %sdigit 5, rigth? Type yes/no -> " % ('' if result else 'not ')).lower()

                if answer == 'yes': # �������� ��������� ��� ������ �����
                    pass
                elif answer == 'no': # �������� �����
                    self.neuron.tune(result, digit)

    def load(self, digit):
        """��������� ����� �� �����"""
        path = os.path.join(DIRLIB, '%s.png' % digit)
        img = Image.open(path)
        array = numpy.array(img)

        # ����������� ������� � ������� ��������
        # ����������� ������� = 1, ����� = 0
        check = lambda color: 0 if color >= 250 else 1

        self.map(array, check)

        return array

    def map(self, array, func):
        """��������� ������� � ������� �������� 2D-�������"""
        for i in xrange(DIMENTIONS[0]):
            for j in xrange(DIMENTIONS[1]):
                array[i][j] = func(array[i][j])

class App:
    """����� ����������"""
    def __init__(self):
        # self.generate()
        # ������������������, ���� ���������� ������������ �����
        # � ���������� ����� ����� �������� ���� �� ������� "arial.ttf"

        self.network = Network()

    def run(self):
        """������ ����������"""
        self.network.teach()

    def generate(self):
        """���������� ����������� � ������� �� 0 �� 9"""
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