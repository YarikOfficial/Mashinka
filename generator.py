import numpy as np
from math import pow,sin,cos
import matplotlib.pyplot as plt

def np_gen_func_line(func = None, length = 10, discretisation = 1, do_negative = False, return_data = False):
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

    y = None


    #Генератор последовательности
    try:
        if(do_negative == True):
            x = np.linspace(-round(length/2),round(length/2),discretisation*length+1,endpoint=True,dtype=np.float64)
        elif(do_negative == False):
            x = np.linspace(0,length,discretisation*length+1,endpoint=True,dtype=np.float64)
        else:
            raise ValueError("Некорректный выбор режима!\n")
    except Exception as e:
        print(f"Ошибка создания аргументов числовой последовательности!\n=====\n{e}")
        return None

    #Получение значений
    try:
        if func == None:
            raise ValueError("Не выбран тип функции!\n")
        
        elif func["type"] == "linear":
            a = func["args"][0]
            b = func["args"][1]

            y = a*x+b

        elif func["type"] == "power":
            stepen = func["args"][0]
            a = func["args"][1]
            b = func["args"][2]

            y = a*np.pow(x,stepen)+b

        elif func["type"] == "root":
            stepen = func["args"][0]
            a = func["args"][1]
            b = func["args"][2]

            y = a*np.pow(x,1/stepen)+b

        else:
            raise ValueError("Некорректный тип функции!\n")
    except Exception as e:
        print(f"Ошибка создания значений числовой последовательности!\n=====\n{e}")
        return None
        

    if return_data == False:
        return y
    elif return_data == True: #не готово
        return y
    else:
        print("Ну тут вообще RuntimeError, но ладно, прощаю\n")
        return y

# def test():
#     func = {"type":"power","args":[1,0]}
#     length = 16
    
#     dataline = np_gen_func_line(func,length)

#     plt.plot(dataline)
#     plt.show()

# test()

#питон не умеет считать по нецелым, это печельно
#убрал на тесте, потом что-нибудь придумать

#и сразу в ячейку применять тоже
#значит везде append проставить надо будет

#===

#исправил добавление значения везде
#исправил дискретизацию
#исправил обработку отрицательных


#===

#Переделал на np вид
#убрал синусы нахуй, потом мб добавлю