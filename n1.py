# -*- coding: cp1251 -*-

import os
import copy
import numpy
from PIL import Image, ImageDraw, ImageFont

# ��� ������� �� ������ ������ � �����
#
# --- *** ��������� ��� ��������. ������ *** ---
# --- *** https://habrahabr.ru/post/143129/ *** ---
#
# ������� ����� �����, ������� ����� ������� ���� ����
# ���� ���� ���������������� �����, ����� ������ Yes � ���������� �����������
# ���� ���� �������� �������, ����� ������ ��� ������ ����� �� ��� ���,
# ���� ���� �� �������������� ���� �����
#
# ������ ���������������� ���� ����������� � ���������� ./memory
# � �������� ������������� ����� ���������� ��� �������� ���� ���������������� �����
# � ������

DIMENTIONS = (30, 30)
DIRMEM = './memory' # ���������� � �������� ������������ ����
DIRLIB = './lib' # ���������� � ��������� �������������

class Neuron:
    """������"""
    weight = 0 # ���
    def __init__(self, letter):
        self.letter = letter

        # ���� � ����� ������� ������������ �����
        self.path = os.path.join(DIRMEM, '%s.png' % self.letter)

        self.load()

    def load(self):
        """��������� ����� ������������������ ����� �� ������"""
        if not os.path.exists(DIRMEM):
            os.mkdir(DIRMEM)

        path = self.path
        if os.path.exists(path):
            img = Image.open(path)
        else:
            img = Image.new("L", DIMENTIONS, "white")
            img.save(path)

        self.data = numpy.array(img)
        self.cache()

    def set(self, i, j, value):
        """������������� ���� ������� [i, j]"""
        self.data[i][j] = value

    def save(self):
        """��������� ����� ������������������ ����� � ������"""
        self.cache()

        path = self.path
        img = Image.fromarray(self._d, mode="L")
        img.save(path)

    def cache(self):
        """�������� ������� �����"""
        self._d = copy.deepcopy(self.data)

    def reset(self):
        """�������� ��� � ������� ����� � ��������� ���������"""
        self.data = copy.deepcopy(self._d)
        self.weight = 0

    def __call__(self, i, j):
        """�������������� ����� ��� ������� � [i, j] �������
        �� ������� �����"""
        return self.data[i][j]

class Network:
    """����, ��������� �� ������ �������"""
    count = 26
    def __init__(self):
        self.neurons = []

        for i in range(self.count):
            letter = chr(ord('A') + i)
            n = Neuron(letter)
            self.neurons.append(n)

    def identify(self, input):
        """�������� ���������������� �����"""
        log = []
        for neuron in self.neurons:
            for i in range(30):
                for j in range(30):
                    N, I = int(neuron(i,j)), int(input[i][j])
                    if abs(N - input[i][j]) < 120:
                        if input[i][j] < 250:
                            neuron.weight = neuron.weight + 1

                    if I != 0 or N != 0:
                        if input[i][j] < 250:
                            value = int(round((N + (N + I) / 2.0) / 2.0))
                            # print neuron.letter, neuron.weight, i, j, value
                            neuron.set(i, j, value)

            log.append('%s:%s' % (neuron.letter, neuron.weight))

        print 'Weights:', ' '.join(log)

        return self.max()

    def max(self):
        """�������� ������ � ������������ �����"""
        return max(self.neurons, key=lambda neuron: neuron.weight)

    def teach(self):
        """������� ��������� ����"""
        letter = self.load(raw_input('letter -> '))

        while True:
            neuron = self.identify(letter)
            answer = raw_input("Is letter '%s', right? Type Yes or correct letter  -> " % neuron.letter).upper()

            if answer in [neuron.letter, 'YES']:
                neuron.save()
                break

            for n in self.neurons:
                if n.letter == answer:
                    n.save()
                else:
                    n.reset()

    def load(self, letter):
        """��������� �������� ����������� ����� �� �����"""
        path = os.path.join(DIRLIB, '%s.png' % letter)
        img = Image.open(path)

        return numpy.array(img)

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
        """���������� ����������� � ������� �� A �� Z"""
        if not os.path.exists(DIRLIB):
            os.mkdir(DIRLIB)

        for i in range(26):
            letter = chr(ord('A') + i)
            path = os.path.join('./lib', '%s.png' % letter)

            img = Image.new("L", (30, 30), "white")
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("arial.ttf", 30)
            draw.text((0, 0), letter, 0, font=font)
            img.save(path)

if __name__ == "__main__":
    app = App()
    app.run()