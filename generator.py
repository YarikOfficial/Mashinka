import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def np_gen_func_line(func:dict = None, length:int = 10, discretisation:int = 1,) -> tuple[np.ndarray | None, dict | None]:
    """
    Генерирует числовой ряд по обычной математической функции.

    Поддерживаемые типы:
    - "linear": args = [a, b]
    - "power": args = [power, a, b]
    - "root": args = [power, a, b]

    Параметры:
    - func: словарь вида {"type": str, "args": list}
    - length: длина ряда, должно быть > 0
    - discretisation: степень дискретизации, должно быть > 0

    Ограничения:
    - Для power и root:
    - - Брать значения в пределах (-1,1) нельзя
    - - При значении (-inf;-1] x = 0 удаляется

    Возвращает:
    - y: массив значений функции
    - data: словарь со служебными данными

    При ошибке:
    - Возвращает (None, None)
    - Вызывает исключение при некорректных входных данных
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
            power = func["args"][0]
            a = func["args"][1]
            b = func["args"][2]

            if power < 1 and power > -1:
                raise ValueError(f"\nДля таких параметров есть root функция!\npower - {power}\n")
            elif power <= -1:
                x = x[1:]

            y = a*np.pow(x,power)+b

        elif func["type"] == "root":
            power = func["args"][0]

            if power == 0:
                raise ZeroDivisionError(f"\nЧё, самый умный?!\npower - {power}\n")

            a = func["args"][1]
            b = func["args"][2]
            
            if power < 1 and power > -1:
                raise ValueError(f"\nДля таких параметров есть power функция!\npower - {power}\n")
            elif power <= -1:
                x = x[1:]
            
            y = a*np.pow(x,1/power)+b

        else:
            raise ValueError(f"\nНекорректный тип функции!\ntype - {func["type"]}\n")
    except ValueError:
        raise
    except ZeroDivisionError:
        raise
    except Exception as e:
        print(f"Ошибка создания значений числовой последовательности!\n=====\n{e}")
        return None, None
        
    data = {}
    data.update({"TOTALlen":len(y),"length":length,"discr":discretisation,"type":func["type"],"x_line":x})
    
    return y, data


def np_gen_func_wave(func:dict = None, length:int = 10, accuracy:int = 1) -> tuple[np.ndarray | None, dict | None]:
    """
    Генерирует числовой ряд по тригонометрической функции.

    Поддерживаемые типы:
    - "sin": args = [a, b]
    - "cos": args = [a, b]
    - "tan": args = [a, b]

    Параметры:
    - func: словарь вида {"type": str, "args": list}
    - length: длина ряда, должно быть > 0
    - accuracy: точность построения, должно быть > 0

    Ограничения:
    - Никаких, удачи

    Возвращает:
    - y: массив значений функции
    - data: словарь со служебными данными

    При ошибке:
    - Возвращает (None, None)
    - Вызывает исключение при некорректных входных данных
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
            x = x + (2 * np.pi * length / (16 * accuracy * length)) / 2

            a = func["args"][0]
            b = func["args"][1]

            y = a*np.tan(x)+b

        else:
            raise ValueError(f"\nНекорректный тип функции!\ntype - {func["type"]}\n")
    except ValueError:
        raise
    except Exception as e:
        print(f"Ошибка создания значений числовой последовательности!\n=====\n{e}")
        return None, None
        
    data = {}
    data.update({"TOTALlen":len(y),"length":length,"acc":16*accuracy,"type":func["type"],"x_line":x})
    
    return y, data

def get_miss(y:np.ndarray, data:dict = None, mode:int = 0, count:int = 0, seed:int = 993) -> tuple[np.ndarray | None, dict | None]:
    """
    Добавляет выбросы в готовый числовой ряд.

    Параметры:
    - y: исходный массив данных
    - data: словарь со служебными данными ряда
    - mode: режим внесения выбросов
    - count: количество выбросов, должно быть >= 0 и < length при X2 или < TOTALlen при X1
    - seed: seed генератора случайных чисел

    Режимы:
    - X1: выбор по индексам
    - X2: выбор по аргументам
    - 1X: 3 сигмы
    - 2X: умножение на 10
    - 3X: случайное значение в пределах ±10*arg

    Ограничения:
    - Никаких, удачи
    - При слишком большом count будет страшно

    Возвращает:
    - new_y: массив с выбросами
    - data: обновлённый словарь данных

    При ошибке:
    - Возвращает (None, None)
    - Вызывает исключение при некорректных входных данных
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
    except ValueError:
        raise
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
    except ValueError:
        raise
    except Exception as e:
        print(f"Ошибка внесения вброса!\n=====\n{e}")
        return None, None

    data.update({"where":vkid,"seed_mis":seed,"mode":mode})

    return new_y, data

def get_noise(y:np.ndarray, data:dict = None, mode:int = None, strength:float = 0.05, sleek:int = 10, seed:int = 993) -> tuple[np.ndarray | None, dict | None]:
    """
    Добавляет шум в числовой ряд.

    Параметры:
    - y: исходный массив данных
    - data: словарь со служебными данными ряда
    - mode: режим шума
    - strength: сила шума, должно быть >= 0
    - sleek: дробность шума, должно быть >= 0
    - seed: seed генератора случайных чисел

    Режимы:
    - 1: шум относительно значения
    - 2: шум относительно среднего
    - 3: шум относительно случайной доли среднего

    Ограничения:
    - strength >= 1 будет давать шум в среднем больше самой последовательности, не рекомендуется

    Возвращает:
    - new_y: массив с шумом
    - data: обновлённый словарь данных

    При ошибке:
    - Возвращает (None, None)
    - Вызывает исключение при некорректных входных данных
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
    
    if sleek < 0:
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
    except ValueError:
        raise
    except Exception as e:
        print(f"Ошибка внесения шума!\n=====\n{e}")
        return None, None

    data.update({"strength":strength,"seed_noise":seed,"sleek":sleek})

    return new_y, data

def draw_plots(data:dict, data_analysed:np.ndarray | None = None) -> None:
    """
    Рисует три отдельных графика:
    чистый ряд, ряд с шумом и ряд с выбросами.

    Параметры:
    - data: словарь с подготовленными данными

    Опционально:
    - data_analysed: индексы найденных аномальных точек

    Ограничения:
    - Молитесь на словарь

    Возвращает:
    - Красивая (опционально) картинка
    """

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

def draw_one_plot(data:dict, data_analysed:np.ndarray | None = None) -> None:
    """
    Рисует один общий график для сравнения рядов.

    Параметры:
    - data: словарь с подготовленными данными

    Опционально:
    - data_analysed: индексы найденных аномальных точек

    Ограничения:
    - Молитесь на словарь

    Возвращает:
    - Красивая (опционально) картинка
    """

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

def data_get_pd(data:dict | None = None) -> None:
    """
    Собирает pandas.DataFrame из подготовленных данных
    и сохраняет его в словарь data.

    Параметры:
    - data: словарь с рядами и служебными полями

    Ограничения:
    - Молитесь на словарь

    Возвращает:
    - Ничего
    """

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

def get_data(func:dict | None = None, length:int | None = None, scaling:int | None = None, mode_noise:int | None = None, strength:float | None = None, sleek:int | None = None, mode_miss:int | None = None, count:int | None = None, seed_noise:int = 993, seed_miss:int = 993) -> dict:
    """
    Полностью собирает данные:
    генерация ряда, добавление шума, добавление выбросов и создание DataFrame.

    Параметры:
    - func: словарь с описанием функции
    - length: длина ряда
    - scaling: дискретизация или точность
    - mode_noise: режим шума
    - strength: сила шума
    - sleek: дробность шума
    - mode_miss: режим выбросов
    - count: количество выбросов
    - seed_noise: seed для шума
    - seed_miss: seed для выбросов

    Ограничения:
    - Изучите документацию остальных функций, там всё написано

    Возвращает:
    - data: словарь со всеми подготовленными данными

    При ошибке:
    - Вызывает исключение
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

def draw_data(data:dict | None = None, type:int | None = None, data_analysed:np.ndarray | None = None) -> None:
    """
    Вызывает нужный способ отрисовки данных.

    Параметры:
    - data: словарь с подготовленными данными
    - type: тип отрисовки

    Опционально:
    - data_analysed: индексы найденных аномальных точек

    Поддерживаемые типы:
    - 1: один общий график
    - 3: три отдельных графика

    Ограничения:
    - Никаких, удачи

    Возвращает:
    - Картинка
    """

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
        data = get_data(func={"type":"tan","args":[1,0]},length=10,scaling=10,mode_noise=1,strength=0.25,sleek=10,mode_miss=11,count=4,seed_noise=111,seed_miss=993)

        print(data["df"].head())

        draw_data(data,1)
    test()