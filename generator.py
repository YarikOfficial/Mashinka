import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def np_gen_func_line(func = None, length = 10, discretisation = 1,):
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
        x = np.linspace(0,length,discretisation*length+1,endpoint=True,dtype=np.float64)
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
            #если степень (-1,1), слать нахуй
            #если она меньше 0, то у нас число наше будет 1/x
            #если чётная, и x <0, то брать как -(|x|^stepen)
            #если нечётная, то и так вроде должен пахать
            stepen = func["args"][0]
            a = func["args"][1]
            b = func["args"][2]

            y = a*np.pow(x,stepen)+b

        elif func["type"] == "root":
            #если она опять же (-1,1), слать нахуй
            #остальные правила примерно тоже описаны, так что делаем, потом
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
    data.update({"TOTALlen":len(y),"length":length,"discr":discretisation,"type":func["type"],"x_line":x,"x_clear":np.arange(length+1)})
    
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
    data.update({"TOTALlen":len(y),"length":length,"acc":16*accuracy,"type":func["type"],"x_line":x,"x_clear":np.arange(length+1)})
    
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

    new_y = np.copy(y)

    if data is None:
        raise RuntimeError("\nПотерял дату? ИДИ И ИЩИ!\n")
    
    if mode <= 0:
        raise ValueError(f"\nНеверный режим работы!\nmode - {mode}\n")

    if count == 0: #ну вроде логично, как бы
        vkid = np.array([])
        data.update({"where":vkid,"seed_mis":seed,"mode":mode})
        return new_y, data
    
    if count < 0:
        raise ValueError(f"\nНекорректное кол-во вбросов\ncount - {count}")
    
    #Создание вбросов
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

def get_noise(y, data = None, mode = None, strength = 0.05, sleek = 10, seed = 993):
    """
    Создания шума в последовательности\n
    mode - тип шума\n
    strength - предел шума\n
    sleek - дробность предела\n
    mode:
    1 - +/- strength от значения
    2 - +/- strength от mean
    3 - +/- strength от среднего в пределах mean или 1
    """

    #Защита
    sleek = int(sleek)

    new_y = np.copy(y)

    if data is None:
        raise RuntimeError("\nПотерял дату? ИДИ И ИЩИ!\n")
    
    if strength == 0:
        data.update({"strength":strength,"seed_noise":seed,"sleek":sleek})
        return new_y, data
    
    if strength < 0:
        raise ValueError(f"\nНекорректное значение разброса\nstrength - {strength}\n")
    
    if sleek <= 0:
        raise ValueError(f"\nНекорректное значение дробности\nsleek - {sleek}\n")

    #Создание шума
    try:
        rand = np.random.default_rng(seed)

        noise = np.linspace(0,strength,sleek+1,endpoint=True,dtype=np.float64)

        if mode == 1:
            new_y = new_y + rand.choice([-1,1],size=new_y.shape) * rand.choice(noise,size=new_y.shape) * new_y
        elif mode == 2:
            mean = new_y.mean()
            new_y = new_y + rand.choice([-1,1],size=new_y.shape) * rand.choice(noise,size=new_y.shape) * mean
        elif mode == 3:
            mean = new_y.mean()
            if mean == 0:
                mean = 1
            new_y = new_y + rand.choice([-1,1],size=new_y.shape) * rand.choice(noise,size=new_y.shape) * rand.random(1) * mean
        else:
            raise ValueError(f"\nНекорретный режив внесения шума!\nmode - {mode}\n")
            
    except Exception as e:
        print(f"Ошибка внесения шума!\n=====\n{e}")
        return None, None

    data.update({"strength":strength,"seed_noise":seed,"sleek":sleek})

    return new_y, data

def draw_plots(data, data_analysed = None):
    if data_analysed is not None:
        fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    else:
        fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    x = data["x_line"]

    axes[0].plot(x, data["dataline"], label="Чистый ряд", color="blue", linewidth=2)
    axes[0].set_title("Чистая последовательность")
    axes[0].set_ylabel("y")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    axes[1].plot(x, data["dataline_noise"], label="Шум", color="orange", linewidth=1.8)
    axes[1].set_title("Последовательность с шумом")
    axes[1].set_ylabel("y")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    axes[2].plot(x, data["dataline_miss"], label="Шум + выбросы", color="red", linewidth=1.8)

    if np.size(data["where"]) != 0:
        axes[2].scatter(x[data["where"]], data["dataline_miss"][data["where"]], label="Выбросы", color="black", s=36, zorder=3)
    if data_analysed is not None:
        axes[2].scatter(x[data_analysed], data["dataline_miss"][data_analysed], label="Аномальные точки", color="yellow", s=20, zorder=4)
        
    axes[2].set_title("Последовательность с выбросами")
    axes[2].set_xlabel("x")
    axes[2].set_ylabel("y")
    axes[2].grid(True, alpha=0.3)
    axes[2].legend()

    plt.tight_layout()
    plt.show()

def draw_one_plot(data, data_analysed = None):
    fig, ax = plt.subplots(figsize=(12, 6))

    x = data["x_line"]
    
    ax.plot(x, data["dataline"], label="Чистый ряд", color="lime", linewidth=2, zorder=3)
    ax.plot(x, data["dataline_noise"], label="С шумом", color="blue", linewidth=1.5, zorder=2)
    ax.plot(x, data["dataline_miss"], label="С выбросами", color="red", linewidth=1.5, zorder=1)

    if np.size(data["where"]) != 0:
        ax.scatter(x[data["where"]], data["dataline_miss"][data["where"]], label="Точки выбросов", color="black", s=36, zorder=4)

    if data_analysed is not None:
        ax.scatter(x[data_analysed], data["dataline_miss"][data_analysed], label="Аномальные точки", color="yellow", s=20, zorder=5)

    ax.set_title("Сравнение последовательностей")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.3)
    ax.legend()

    plt.tight_layout()
    plt.show()

def data_get_pd(data = None):
    if data is None:
        raise RuntimeError("\nПотерял дату? ИДИ И ИЩИ!\n")

    df = pd.DataFrame({"x": data["x_line"], "clean": data["dataline"], "noise": data["dataline_noise"], "miss": data["dataline_miss"]})

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

    data.update({"df":df})

def get_data(func = None, length = None, scaling = None, mode_noise = None, strength = None, sleek = None, mode_miss = None, count = None, seed_noise = 993, seed_miss = 993):
    """
    Передайте все аргументы для функций ниже.\n
    Нужны:
    1) Сама функция
    2) Желаемая длина
    3) Желаемое растягивание (точность)
    4) Сила шума
    5) Растяжимость шума
    6) Режим внесения вброса
    7) Кол-во вбросов
    8) Сид (по желанию)\n
    Подробнее написано в самих функциях\n
    """

    if func is None or length is None or scaling is None or strength is None or sleek is None or mode_miss is None or mode_noise is None or count is None:
        raise ValueError("\nУмник, функция необходима, всё остальное тоже!\n")
    
    if func["type"] == "linear" or func["type"] == "root" or func["type"] == "power":
        dataline, data = np_gen_func_line(func=func,length=length,discretisation=scaling)
    elif func["type"] == "sin" or func["type"] == "cos" or func["type"] == "tan":
        dataline, data = np_gen_func_wave(func=func,length=length,accuracy=scaling)
    else:
        raise ValueError(f"\nНекорректный тип функции!\ntype - {func["type"]}\n")
    
    if dataline is None or data is None:
        raise RuntimeError("\nОшибка получения последовательности!\n")
    
    dataline_noise, data = get_noise(dataline,data=data,mode=mode_noise,strength=strength,sleek=sleek,seed=seed_noise)
    
    if dataline_noise is None or data is None:
        raise RuntimeError("\nОшибка внесения шума в последовательность!\n")
    
    dataline_miss, data = get_miss(dataline_noise,data=data,mode=mode_miss,count=count,seed=seed_miss)

    if dataline_miss is None or data is None:
        raise RuntimeError("\nОшибка внесения вбросов в последовательность!\n")

    data.update({"dataline":dataline,"dataline_noise":dataline_noise,"dataline_miss":dataline_miss})

    data_get_pd(data)

    return data

def draw_data(data = None, type = None, data_analysed = None):
    if data is None:
        raise RuntimeError("\nПотерял дату? ИДИ И ИЩИ!\n")

    if type == 1:
        draw_one_plot(data, data_analysed)
    elif type == 3:
        draw_plots(data, data_analysed)
    else:
        raise ValueError(f"\nНекорректный тип отрисовки!\ntype - {type}\n")
    


if __name__ == "__main__":
    def test():
        data = get_data(func={"type":"sin","args":[1,0]},length=10,scaling=10,mode_noise=3,strength=0.25,sleek=5,mode_miss=12,count=0,seed_noise=111,seed_miss=993)

        print(data["df"].head())

        draw_data(data,1)
    test()

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

#===

#сделал общую дату
#сделал общие функции