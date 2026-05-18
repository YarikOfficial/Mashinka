import toml
import streamlit as st
import generator as gen
import analyzer as anlz
import matplotlib.pyplot as plt
import numpy as np
import random
from sklearn.metrics import f1_score

def load_config():
    try:
        with open('.streamlit\config.toml', 'r') as f:
            config = toml.load(f)
        return config
    except FileNotFoundError:
        st.error("Файл toml не найден!")
        return None
    except Exception as e:
        st.error(f"Ошибка при загрузке TOML: {e}")
        return None
    
load_config()

def graphics(data, type, pars, data_analysed_stat = None, data_analysed_ML = None):
    
    fig, axes = plt.subplots(1, 1, figsize=(9.5, 7.8), sharex=True)

    x = data["x_line"]

    axes.plot(x, data["dataline_miss"], label="Последовательность", color="#6C68AD", linewidth=1.8)
    axes.scatter(x[data["where"]], data["dataline_miss"][data["where"]], label="Аномальные точки", color="#08001D", s=100, zorder=3)

    if data_analysed_stat is not None:
        try:
            axes.scatter(x[data_analysed_stat], data["dataline_miss"][data_analysed_stat], label="Обнаруженные аномальные точки (статистический метод)", color="#FF0000", s=100, zorder=4)
            axes.set_title(f"F1 score = {f1_score(np.array(data['df']['is_miss']), data_analysed_stat, average='macro')}")
        except:
            pass

    if data_analysed_ML is not None:
        try:
            axes.scatter(x[data_analysed_ML], data["dataline_miss"][data_analysed_ML], label="Обнаруженные аномальные точки (ML метод)", color="#35D814", s=100, zorder=5)
            axes.set_title(f"F1 score = {f1_score(np.array(data['df']['is_miss']), data_analysed_ML, average='macro')}")
        except:
            pass
    
    ylabels = {
        "linear": f"{pars[0]}x + {pars[1]}",
        "power": f"{pars[0]}x^{pars[2]} + {pars[1]}",
        "root": f"{pars[0]}x^(1/{pars[2]}) + {pars[1]}",
        "sin": f"{pars[0]}sinx + {pars[1]}",
        "cos": f"{pars[0]}cosx + {pars[1]}",
        "tan": f"{pars[0]}tgx + {pars[1]}"
    }
    axes.set_xlabel("x", fontsize=14, fontweight='bold')
    axes.set_ylabel(ylabels[type], fontsize=14, fontweight='bold')
    axes.grid(True, alpha=0.3)
    axes.legend()

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

def init_session_state():
    defaults = {
        'length': 100,
        'scaling': 10,
        'mode_noise': 1,
        'strength': 0.1,
        'sleek': 10,
        'mode_miss1': "3 сигмы",
        'mode_miss2': "По индексам",
        'count': 10,
        'seed_noise': 111,
        'seed_miss': 993,
        'outliers_st': None,
        'outliers_ML': None,
        'threshold': 3.0,
        'split': 5,
        'contamination': 0.01,
        'rand_seed_noise': True,
        'rand_seed_miss': True,
        'a': 1,
        'b': 1,
        'c': 1,
        'function_type': "Линейная",
        'form_key': 0,
        'meth_type': "Isolation Forest",
        'neigh': 5
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def refresh_form():
    st.session_state.form_key += 1
    st.rerun()

init_session_state()

st.set_page_config(layout="centered", 
                   page_title="Модель для обнаружения аномалий в числовых последовательностях"
                ) 

st.title("Модель для обнаружения аномалий в числовых последовательностях")

function_map = {
    "Линейная": "linear",
    "Степенная": "power", 
    "Корень": "root",
    "Синус": "sin",
    "Косинус": "cos",
    "Тангенс": "tan"
    }

type = function_map[st.session_state.function_type]
if type in ["power", "root"]:
    args = [st.session_state.a, st.session_state.b, st.session_state.c]
else:
    args = [st.session_state.a, st.session_state.b, 666]

mode1_map = {"3 сигмы": 1,
            "Вброс на *10": 2,
            "Случайное значение в пределах +-10*arg": 3
            }

mode2_map = {"По индексам": 1,
            "По аргументам": 2
            }

mode_miss = mode1_map[st.session_state.mode_miss1] * 10 + mode2_map[st.session_state.mode_miss2]

data = gen.get_data(func={"type":type,"args":args},
                        length=st.session_state.length,
                        scaling=st.session_state.scaling,
                        mode_noise=st.session_state.mode_noise,
                        strength=st.session_state.strength,
                        sleek=st.session_state.sleek,
                        mode_miss=mode_miss,
                        count=st.session_state.count,
                        seed_noise=st.session_state.seed_noise,
                        seed_miss=st.session_state.seed_miss
                    )



function_options = ["Линейная", "Степенная", "Корень", "Синус", "Косинус", "Тангенс"]
func = st.selectbox("Выберите функцию", 
                    function_options,
                    index=function_options.index(st.session_state.function_type)
                )
st.session_state.function_type = func

arg1, arg2, arg3 = st.columns(3)
with arg1:
    a = st.number_input("Угловой коэффициент", value=st.session_state.a)
    st.session_state.a = a
with arg2:
    b = st.number_input("Свободный коэффициент", value=st.session_state.b)
    st.session_state.b = b
with arg3:
    st.session_state.c = st.number_input(
        "Показатель корня/степени", 
        disabled = not (st.session_state.function_type in ["Степенная", "Корень"]),
        value=st.session_state.c
    )

if st.button("Сгенерировать новые данные", type = "primary", use_container_width = True):
        if st.session_state.rand_seed_noise:
            st.session_state.seed_noise = random.randint(0, 1000)
        if st.session_state.rand_seed_miss:
            st.session_state.seed_miss = random.randint(0, 1000)
        st.session_state.outliers_st = None
        st.session_state.outliers_ML = None
        st.rerun()

with st.expander("Настройки генерации"):

    par1, par2, par3, par4 = st.columns(4)
    with par1:
        st.session_state.length = st.number_input(
            "Длина",
            #min_value=1, 
            #max_value=100, 
            value=st.session_state.length
        )
    with par2:
        st.session_state.scaling = st.number_input(
            "Масштаб по оси X",
            #min_value=1, 
            #max_value=100,
            value=st.session_state.scaling
        )
    with par3:
        st.session_state.mode_noise = st.selectbox(
            "Режим шума",
            options=[1, 2, 3],
            index=[1, 2, 3].index(st.session_state.mode_noise) if st.session_state.mode_noise in [1, 2, 3] else 1,
            format_func=lambda x: f"Режим {x}"
        )
    with par4:
        st.session_state.strength = st.slider(
            "Интенсивность шума", 
            min_value=0.0, 
            max_value=1.0, 
            value=st.session_state.strength,
            step=0.01
        )

    par5, mode1, mode2, par6 = st.columns(4)
    with par5:
        st.session_state.sleek = st.number_input(
            "Плавность шума",
            #min_value=1, 
            #max_value=100, 
            value=10
        )
    with mode1:
        mode1_options = ["3 сигмы", "Вброс на *10", "Случайное значение в пределах +-10*arg"]
        mode1 = st.selectbox("Режим выбросов", 
                            mode1_options,
                            index=mode1_options.index(st.session_state.mode_miss1)
                        )
        st.session_state.mode_miss1 = mode1
    with mode2:
        mode2_options = ["По индексам", "По аргументам"]
        mode2 = st.selectbox("Внесение ошибок",
                            mode2_options,
                            index=mode2_options.index(st.session_state.mode_miss2)
                        )
        st.session_state.mode_miss2 = mode2
    with par6:
        st.session_state.count = st.number_input(
            "Количество выбросов",
            min_value=0, 
            #max_value=100,
            value=10
        )

    par7, par7c, par8, par8c = st.columns(4)
    with par7c:
        st.session_state.rand_seed_noise = st.checkbox("Случайный сид шума", value=st.session_state.rand_seed_noise)
    with par7:
        st.session_state.seed_noise = st.number_input(
            "Сид шума",
            disabled=st.session_state.rand_seed_noise,
            min_value=0, 
            max_value=9999,
            value=st.session_state.seed_noise
        )
    with par8c:
        st.session_state.rand_seed_miss = st.checkbox("Случайный сид выбросов", value=st.session_state.rand_seed_miss)
    with par8:
        st.session_state.seed_miss = st.number_input(
            "Сид выбросов",
            disabled=st.session_state.rand_seed_miss,
            min_value=0, 
            max_value=9999,
            value=st.session_state.seed_miss
        )

with st.expander("Настройки статистического метода"):

    par_st1, par_st2 = st.columns(2)
    with par_st1:
        st.session_state.threshold = st.number_input(
            "Значение Сигма",
            #min_value=1, 
            #max_value=100, 
            value=st.session_state.threshold
        )
    with par_st2:
        st.session_state.split = st.number_input(
            "Разбиение массива данных",
            #min_value=1, 
            #max_value=100,
            value=st.session_state.split
        )
with st.expander("Настройки ML метода"):
    meth_options = ["Isolation Forest", "Local Outlier Factor"]
    meth = st.selectbox("Выберите метод", 
                        meth_options,
                        index=meth_options.index(st.session_state.meth_type)
                    )
    st.session_state.meth_type = meth
    par9, par10 = st.columns(2)
    with par9:
        st.session_state.contamination = st.number_input(
                "Ожидаемый процент выбросов",
                disabled=not(st.session_state.meth_type=="Isolation Forest"),
                #min_value=1, 
                #max_value=100, 
                value=st.session_state.contamination
            )
    with par10:
        st.session_state.neigh = st.number_input(
                "Количество ближайших соседей",
                disabled=not(st.session_state.meth_type=="Local Outlier Factor"),
                #min_value=1, 
                #max_value=100, 
                value=st.session_state.neigh
            )
    
with st.form("draw"):    
    but0, but1= st.columns(2)
    with but0:
        if st.form_submit_button("Найти аномалии статистическим методом", type = "primary", use_container_width = True):
            dataline = data["dataline_miss"]
            st.session_state.outliers_ML = None
            st.session_state.outliers_st = anlz.zscore_find_outliers(dataline, 
                                                            threshold=st.session_state.threshold, 
                                                            split=st.session_state.split
                                                        )
            refresh_form()
    with but1:
        if st.form_submit_button("Найти аномалии ML методом", type = "primary", use_container_width = True):
            X = anlz.get_X(data)
            st.session_state.outliers_st = None
            st.session_state.outliers_ML = None
            if st.session_state.meth_type == "Isolation Forest":
                st.session_state.outliers_ML = anlz.ml_isoforest(X, st.session_state.contamination)
            elif st.session_state.meth_type == "Local Outlier Factor":
                st.session_state.outliers_ML = anlz.ml_lof(X, st.session_state.neigh)
            refresh_form()

    graphics(data, type, args, st.session_state.outliers_st, st.session_state.outliers_ML)
    plt.close('all')