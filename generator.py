import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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

    #Защита
    length = int(length)
    discretisation = int(discretisation)
    
    if length <= 0:
        raise ValueError(f"\nНекорректная длина функции!\nlength - {length}\n")
    
    if discretisation <= 0:
        raise ValueError(f"\nНекорректное значение дискретизации!\ndiscretisation - {discretisation}\n")

    y = None

    #Генератор последовательности
    try:
        if(do_negative == True):
            x = np.linspace(-round(length/2),round(length/2),discretisation*length+1,endpoint=True,dtype=np.float64)
        elif(do_negative == False):
            x = np.linspace(0,length,discretisation*length+1,endpoint=True,dtype=np.float64)
        else:
            raise ValueError("\nНекорректный выбор режима!\n")
    except Exception as e:
        print(f"Ошибка создания аргументов числовой последовательности!\n=====\n{e}")
        return None, None

    #Получение значений
    try:
        if func is None:
            raise ValueError("\nНе выбран тип функции!\n")
        
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

            if stepen == 0:
                raise ZeroDivisionError(f"\nЧё, самый умный?!\nstepen - {stepen}\n")

            a = func["args"][1]
            b = func["args"][2]
            
            y = a*np.pow(x,1/stepen)+b

        else:
            raise ValueError(f"\nНекорректный тип функции!\ntype - {func["type"]}\n")
    except Exception as e:
        print(f"Ошибка создания значений числовой последовательности!\n=====\n{e}")
        return None, None
        
    data = {}
    data.update({"TOTALlen":len(y),"length":length,"discr":discretisation,"type":func["type"],"x_line":x})
    
    return y, data


def np_gen_func_wave(func = None, length = 10, accuracy = 1):
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
    accuracy - кол-во точек на обороте*16\n
    \n
    """

    #Защита
    length = int(length)
    accuracy = int(accuracy)

    if length <= 0:
        raise ValueError(f"\nНекорректная длина функции!\nlength - {length}\n")
    
    if accuracy <= 0:
        raise ValueError(f"\nНекорректное значение точности!\naccuracy - {accuracy}\n")

    y = None

    #Генератор последовательности
    try:
        x = np.linspace(0,2*np.pi*length,16*accuracy*length+1,endpoint=True,dtype=np.float64)
    except Exception as e:
        print(f"Ошибка создания аргументов числовой последовательности!\n=====\n{e}")
        return None, None

    #Получение значений
    try:
        if func is None:
            raise ValueError("\nНе выбран тип функции!\n")
        
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
            raise ValueError(f"\nНекорректный тип функции!\ntype - {func["type"]}\n")
    except Exception as e:
        print(f"Ошибка создания значений числовой последовательности!\n=====\n{e}")
        return None, None
        
    data = {}
    data.update({"TOTALlen":len(y),"length":length,"acc":16*accuracy,"type":func["type"],"x_line":x})
    
    return y, data


def get_miss(y, data = None, mode = 0, count = 0, seed = 993):
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

    #Защита
    count = int(count)
    seed = int(seed)

    if data is None:
        raise RuntimeError("\nПотерял дату? ИДИ И ИЩИ!\n")
    
    if mode <= 0:
        raise ValueError(f"\nНеверный режим работы!\nmode - {mode}\n")

    if count == 0: #ну вроде логично, как бы
        return y, data
    
    if count < 0:
        raise ValueError(f"\nНекорректное кол-во вбросов\ncount - {count}")
    
    #Создание вбросов
    new_y = np.copy(y)
    
    where = mode%10
    which = mode//10

    #Определение места
    try:
        rand = np.random.default_rng(seed)

        if where == 1:
            if count > data["TOTALlen"]:
                raise ValueError(f"\nЧисло ошибок больше последовательности!\ncount - {count} size - {data["TOTALlen"]}\n")
            vkid = rand.choice(data["TOTALlen"],count,replace=False)
        elif where == 2:
            if count > data["length"]:
                raise ValueError(f"\nЧисло ошибок больше кол-ва аргументов последовательности!\ncount - {count} size - {data["length"]}\n")
            args = rand.choice(data["length"],count,replace=False)

            if(data["type"] != "sin" and data["type"] != "cos" and data["type"] != "tan"):
                vkid = (args[:, None] * data["discr"] + np.arange(data["discr"])).ravel()
            else:
                vkid = (args[:, None] * data["acc"] + np.arange(data["acc"])).ravel()
        else:
            raise ValueError(f"\nНекорректный режим выбора!\nwhere - {where}\n")
    except Exception as e:
        print(f"Ошибка создания точек вброса!\n=====\n{e}")
        return None, None
        
    #Определение что
    try:
        if which == 1:
            #new_y[vkid] = new_y.mean() * 3 * new_y.std()
            mu = new_y.mean()
            sigma = new_y.std(ddof=0)
            new_y[vkid] = mu+rand.choice([-1,1],size=new_y[vkid].shape)*(3.0*sigma)
        elif which == 2:
            new_y[vkid] *= 10
        elif which == 3:
            #new_y[vkid] = rand.random()*10*rand.choice([-1,1],1)*new_y[vkid]
            new_y[vkid] = rand.choice([-1,1],size=new_y[vkid].shape)*10*rand.random(size=new_y[vkid].shape)*np.abs(new_y[vkid])
        else:
            raise ValueError(f"\nНекорректный режим вставки!\nwhich - {which}\n")
    except Exception as e:
        print(f"Ошибка внесения вброса!\n=====\n{e}")
        return None, None

    data.update({"where":vkid,"seed_mis":seed,"mode":mode})

    return new_y, data

def get_noise(y, data = None, strength = 0.05, sleek = 10, seed = 993):
    """
    Создания шума в последовательности\n
    strength - предел шума\n
    sleek - дробность предела
    """

    #Защита
    sleek = int(sleek)

    if data is None:
        raise RuntimeError("\nПотерял дату? ИДИ И ИЩИ!\n")
    
    if strength == 0:
        return y, data
    
    if strength < 0:
        raise ValueError(f"\nНекорректное значение разброса\nstrength - {strength}\n")
    
    if sleek <= 0:
        raise ValueError(f"\nНекорректное значение дробности\nsleek - {sleek}\n")

    #Создание шума
    try:
        new_y = np.copy(y)
        
        rand = np.random.default_rng(seed)

        noise = np.linspace(0,strength,sleek+1,endpoint=True,dtype=np.float64)

        new_y = new_y + rand.choice([-1,1],size=new_y.shape) * rand.choice(noise,size=new_y.shape) * new_y

    except Exception as e:
        print(f"Ошибка внесения шума!\n=====\n{e}")
        return None, None

    data.update({"strength":strength,"seed_noise":seed,"sleek":sleek})

    return new_y, data

def draw_plots(dataline, dataline_noise, dataline_miss, data):
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    x = data["x_line"]

    axes[0].plot(x, dataline, label="Чистый ряд", linewidth=2)
    axes[0].set_title("Чистая последовательность")
    axes[0].set_ylabel("y")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    axes[1].plot(x, dataline_noise, label="Шум", linewidth=1.8)
    axes[1].set_title("Последовательность с шумом")
    axes[1].set_ylabel("y")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    axes[2].plot(x, dataline_miss, label="Шум + выбросы", linewidth=1.8)
    axes[2].scatter(x[data["where"]], dataline_miss[data["where"]], label="Выбросы", s=35)
    axes[2].set_title("Последовательность с выбросами")
    axes[2].set_xlabel("x")
    axes[2].set_ylabel("y")
    axes[2].grid(True, alpha=0.3)
    axes[2].legend()

    plt.tight_layout()
    plt.show()

def draw_one_plot(dataline, dataline_noise, dataline_miss, data):
    fig, ax = plt.subplots(figsize=(12, 6))

    x = data["x_line"]
    
    ax.plot(x, dataline, label="Чистый ряд", color="blue", linewidth=2)
    ax.plot(x, dataline_noise, label="С шумом", color="orange", linewidth=1.8)
    ax.plot(x, dataline_miss, label="С выбросами", color="red", linewidth=1.8)

    ax.scatter(x[data["where"]], dataline_miss[data["where"]], label="Точки выбросов", color="black", s=35, zorder=3)

    ax.set_title("Сравнение последовательностей")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.3)
    ax.legend()

    plt.tight_layout()
    plt.show()

def data_to_pd(dataline, dataline_noise, dataline_miss, data):
    df = pd.DataFrame({"x": data["x_line"], "clean": dataline, "noise": dataline_noise, "miss": dataline_miss})

    df["noise_delta"] = df["noise"] - df["clean"]
    df["miss_delta_from_noise"] = df["miss"] - df["noise"]
    df["miss_delta_from_clean"] = df["miss"] - df["clean"]
    df["noise_abs_delta"] = np.abs(df["noise_delta"])
    df["miss_abs_delta_from_noise"] = np.abs(df["miss_delta_from_noise"])
    df["miss_abs_delta_from_clean"] = np.abs(df["miss_delta_from_clean"])

    df["noise_changed"] = (df["noise"] != df["clean"]).astype(int)
    df["miss_changed"] = (df["miss"] != df["noise"]).astype(int)

    df["is_miss"] = 0
    df.loc[data["where"], "is_miss"] = 1

    return df

# def test():
#     func_line = {"type":"linear","args":[2,2]}
#     func_wave = {"type":"linear","args":[2,2]}
#     N = 10
    
#     dataline,data = np_gen_func_line(func_line,N,1,False)
#     #datawave = np_gen_func_wave(func_wave,10,10)
#     if dataline is None or data is None:
#         raise RuntimeError("\nОшибка получения последовательности!\n")
    
#     dataline_noise, data = get_noise(dataline,data,0.1,1)
#     dataline_miss, data = get_miss(dataline_noise,data,21,3)

#     draw_one_plot(dataline,dataline_noise,dataline_miss,data)

#     df = data_to_pd(dataline,dataline_noise,dataline_miss,data)

#     print(df)
#     print("\n")
#     print(df[["noise_abs_delta", "miss_abs_delta_from_clean"]].describe())

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

#===

#сделал генератор шума
#сделал почти всё
#пофиксил некоторое дерьмо