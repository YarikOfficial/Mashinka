import numpy as np
from math import pow,sin,cos
import matplotlib.pyplot as plt

def gen_func_line(func = None, length = 10, discretisation = 1, do_negative = False, return_data = False):
    """
    Генератор ряда на основе математический функции.\n
    Поддерживается на данный момент:\n
    Линейная - "linear" args = [коэфф.;свободный]\n
    Степенная - "power" args = [степень;коэфф.;свободный]\n
    Корень - "root" args = [степень;коэфф.;свободный]\n
    Синусоида - "sin" args = [коэфф.;свободный]\n
    Косинусоида - "cos" args = [коэфф.;свободный]\n
    \n
    func - словарь с ключами:\n
    "type" - где хранится тип функции в строке\n
    "args" - список аргументов к необходимой функции\n
    \n
    length - кол-во значений x обрабатываемых функцией\n
    \n
    discretisation - как сильно будет одно значение обрабатываться\n
    \n
    do_negative - будет ли обработка с отрицательных значений\n
    \n
    return_data - пока не готово\n
    """

    y = []

    if func == None:
        raise ValueError("Не выбран тип функции")
    
    elif func["type"] == "linear":
        a = func["args"][0]
        b = func["args"][1]

        if do_negative == True:
            for x in range(length/2,length/2,1/discretisation):
                y[x] = a*x+b
        else:
            for x in range(0,length,1):
                y.append(a*x+b)

    elif func["type"] == "power":
        stepen = func["args"][0]
        a = func["args"][1]
        b = func["args"][2]

        if do_negative == True:
            for x in range(length/2,length/2,1/discretisation):
                y[x] = a*pow(x,stepen)+b
        else:
            for x in range(0,length,1/discretisation):
                y[x] = a*pow(x,stepen)+b

    elif func["type"] == "root":
        stepen = func["args"][0]
        a = func["args"][1]
        b = func["args"][2]

        if do_negative == True:
            for x in range(length/2,length/2,1/discretisation):
                y[x] = a*pow(x,1/stepen)+b
        else:
            for x in range(0,length,1/discretisation):
                y[x] = a*pow(x,1/stepen)+b

    elif func["type"] == "sin":
        a = func["args"][0]
        b = func["args"][1]

        if do_negative == True:
            for x in range(length/12,length/12,1/(6*discretisation)):
                y[x] = a*sin(x)+b
        else:
            for x in range(0,length/6,1/(6*discretisation)):
                y[x] = a*sin(x)+b

    elif func["type"] == "cos":
        a = func["args"][0]
        b = func["args"][1]

        if do_negative == True:
            for x in range(length/12,length/12,1/(6*discretisation)):
                y[x] = a*cos(x)+b
        else:
            for x in range(0,length/6,1/(6*discretisation)):
                y[x] = a*cos(x)+b

    else:
        raise ValueError("Некорректный тип функции")
    
    if return_data == False:
        return y
    else:
        return y
    
def test():
    func = {"type":"linear","args":[2,0]}
    length = 100
    discretisation = 10
    
    dataline = gen_func_line(func,length,discretisation)

    plt.plot(dataline)
    plt.show()

test()

#питон не умеет считать по нецелым, это печельно
#убрал на тесте, потом что-нибудь придумать

#и сразу в ячейку применять тоже
#значит везде append проставить надо будет