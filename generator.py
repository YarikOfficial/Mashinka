import numpy as np
import matplotlib.pyplot as plt

def np_gen_func_line(func = None, length = 10, discretisation = 1, do_negative = False):
    """
    Генератор ряда на основе математический функции.\n
    Поддерживается на данный момент:\n
    Линейная - "linear" args = [коэфф.;свободный]\n
    Степенная - "power" args = [степень;коэфф.;свободный]\n
    Корень - "root" args = [степень;коэфф.;свободный]\n
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
        
    data = {}
    data.update({"TOTALlen":len(y),"length":length,"discr":discretisation,"type":func["type"]})
    
    return y, data


def np_gen_func_wawe(func = None, length = 10 ,accuracy = 1, return_data = False):
    """
    Генератор ряда на основе математический функции.\n
    Поддерживается на данный момент:\n
    Синусоида - "sin" args = [коэфф.;свободный]\n
    Косинусоида - "cos" args = [коэфф.;свободный]\n
    Тангенсоида - "tan" args = [коэфф.;свободный]\n
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
    """

    y = None

    #Генератор последовательности
    try:
        x = np.linspace(0,2*np.pi*length,16*accuracy*length,endpoint=True,dtype=np.float64)
    except Exception as e:
        print(f"Ошибка создания аргументов числовой последовательности!\n=====\n{e}")
        return None

    #Получение значений
    try:
        if func == None:
            raise ValueError("Не выбран тип функции!\n")
        
        elif func["type"] == "sin":
            a = func["args"][0]
            b = func["args"][1]

            y = a*np.sin(x)+b

        elif func["type"] == "cos":
            a = func["args"][0]
            b = func["args"][1]

            y = a*np.cos(x)+b

        elif func["type"] == "tan":
            a = func["args"][0]
            b = func["args"][1]

            y = a*np.tan(x)+b

        else:
            raise ValueError("Некорректный тип функции!\n")
    except Exception as e:
        print(f"Ошибка создания значений числовой последовательности!\n=====\n{e}")
        return None
        

    data = {}
    data.update({"TOTALlen":len(y),"length":length,"acc":16*accuracy,"type":func["type"]})
    
    return y, data


def get_mis(y, data = None, mode = 0, count = 0, seed = 993):
    """
    Внесение помех в снегерированные данные\n
    y - данные\n
    data - вместе с данными должны идти\n
    mode - режим работы\n
    count - кол-во ошибок\n
    mode:
    X1 - внесение ошибок по индексам
    X2 - внесение ошибок по аргументам
    1X - 3 сигмы
    2X - вброс на *10
    3X - случайное значение в пределах +-10*arg
    """

    if data == None:
        raise RuntimeError("Потерял дату? ИДИ И ИЩИ!\n")
    
    if mode == 0:
        raise ValueError("Неверный режим работы!\n")

    if count == 0: #ну вроде логично, как бы
        return y, data
    
    where = mode%10
    which = mode//10
    rand = np.random.default_rng(seed)

    if where == 1:
        vkid = rand.choice(data["TOTALlen"],count,replace=False)
    elif where == 2:
        args = rand.choice(data["length"],count,replace=False)

        if(data["type"] != "sin" and data["type"] != "cos" and data["type"] != "tan"):
            vkid = (args[:, None] * data["discr"] + np.arange(data["discr"])).ravel()
        else:
            vkid = (args[:, None] * data["acc"] + np.arange(data["acc"])).ravel()
    else:
        raise ValueError("Некорректный режим выбора!\n")

    if which == 1:
        #y[vkid] = y.mean() * 3 * y.std()
        mu = y.mean()
        sigma = y.std(ddof=0)
        y[vkid] = mu+rand.choice([-1,1],size=y[vkid].shape)*(3.0*sigma)
    elif which == 2:
        y[vkid] *= 10
    elif which == 3:
        #y[vkid] = rand.random()*10*rand.choice([-1,1],1)*y[vkid]
        y[vkid] = rand.choice([-1,1],size=y[vkid].shape)*10*rand.random(size=y[vkid].shape)*np.abs(y[vkid])
    else:
        raise ValueError("Некорректный режим вставки!\n")
    
    data.update({"where":vkid,"seed":seed,"mode":mode})

    return y, data


#def test():
#    func = {"type":"linear","args":[3,1]}
#    N = 10
#    
#    dataline,data = np_gen_func_line(func,N,10,False)

#    dataline_miss,data = get_mis(dataline,data,11,round(N/10))

#    plt.plot(dataline)
#    print(data)
#    plt.show()

#test()

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