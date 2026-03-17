import toml
import streamlit as st
import generator as gen
import analyzer as anlz
import matplotlib.pyplot as plt

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

def graphics(data, data_analysed = None):
    
    fig, axes = plt.subplots(1, 1, figsize=(9.5, 7.8), sharex=True)

    x = data["x_line"]

    axes.plot(x, data["dataline_miss"], label="Последовательность", color="#6C68AD", linewidth=1.8)
    axes.scatter(x[data["where"]], data["dataline_miss"][data["where"]], label="Выбросы", color="#08001D", s=100, zorder=3)

    if data_analysed is not None:
        try:
            axes.scatter(x[data_analysed], data["dataline_miss"][data_analysed], label="Аномальные точки", color="#FF0000", s=100, zorder=4)
        except:
            pass

    axes.set_xlabel("x", fontsize=14, fontweight='bold')
    axes.set_ylabel("y", fontsize=14, fontweight='bold')
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
        'mode_miss': 11,
        'count': 10,
        'seed_noise': 111,
        'seed_miss': 993,
        'outliers': None,
        'threshold': 3.0,
        'split': 5
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

st.set_page_config(layout="centered", 
                   page_title="Модель для обнаружения аномалий в числовых последовательностях",
                   initial_sidebar_state="expanded"
                ) 
st.title("Модель для обнаружения аномалий в числовых последовательностях")

with st.form("main_form"):

    function_type = st.selectbox("Выберите функцию", 
                        ["Линейная", 
                        "Степенная", 
                        "Корень", 
                        "Синус", 
                        "Косинус", 
                        "Тангенс"]
            )

    arg1, arg2, arg3 = st.columns(3)

    with arg1:
        a = st.number_input("A", value=2.6667)
    with arg2:
        b = st.number_input("B", value=0.45)
    with arg3:
        c = st.number_input(
            "C (только для корня и степени)", 
            disabled = not (function_type in ["Степенная", "Корень"])
        )

    function_map = {
        "Линейная": "linear",
        "Степенная": "power", 
        "Корень": "root",
        "Синус": "sin",
        "Косинус": "cos",
        "Тангенс": "tan"
    }

    type = function_map[function_type]
    if type in ["power", "root"]:
        args = [a, b, c]
    else:
        args = [a, b]


    data = gen.get_data(func={"type":type,"args":args},
                        length=st.session_state.length,
                        scaling=st.session_state.scaling,
                        mode_noise=st.session_state.mode_noise,
                        strength=st.session_state.strength,
                        sleek=st.session_state.sleek,
                        mode_miss=st.session_state.mode_miss,
                        count=st.session_state.count,
                        seed_noise=st.session_state.seed_noise,
                        seed_miss=st.session_state.seed_miss
                    )

    graphics(data, st.session_state.outliers)
    plt.close('all')

    if st.form_submit_button("Сгенерировать новые данные", type = "primary", use_container_width = True):
        st.session_state.outliers = None

    but0, but1= st.columns(2)

    with but0:
        if st.form_submit_button("Найти аномалии статистическим методом", type = "primary", use_container_width = True):
            dataline = data["dataline_miss"]
            st.session_state.outliers = anlz.find_outliers(dataline, 
                                                           threshold=st.session_state.threshold, 
                                                           split=st.session_state.split
                                                        )

    with but1:
        st.form_submit_button(
            "Найти аномалии ML методом", 
            type = "primary", 
            use_container_width = True,
            help = "В разработке"
        )



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
                "Растягивание",
                #min_value=1, 
                #max_value=100,
                value=st.session_state.scaling
            )
        with par3:
            st.session_state.mode_noise = st.selectbox(
                "Режим шума",
                options=[1, 2],
                index=[1, 2].index(st.session_state.mode_noise) if st.session_state.mode_noise in [1, 2] else 1,
                format_func=lambda x: f"Режим {x}"
            )
        with par4:
            st.session_state.strength = st.slider(
                "Сила шума", 
                min_value=0.0, 
                max_value=1.0, 
                value=st.session_state.strength,
                step=0.01
            )

        par5, par6, par7 = st.columns(3)

        with par5:
            st.session_state.sleek = st.number_input(
                "Растяжимость шума",
                #min_value=1, 
                #max_value=100, 
                value=10
            )
        with par6:
            st.session_state.mode_miss = st.selectbox(
                "Режим выбросов",
                options=[11, 12, 21, 22, 31, 32],
                index=[11, 12, 21, 22, 31, 32].index(st.session_state.mode_miss) if st.session_state.mode_miss in [11, 12, 21, 22, 31, 32] else 1,
                format_func=lambda x: f"Режим {x}",
                help="""
                X1 - внесение ошибок по индексам\n
                X2 - внесение ошибок по аргументам\n
                1X - 3 сигмы\n
                2X - вброс на *10\n
                3X - случайное значение в пределах +-10*arg.
                """
            )
        with par7:
            st.session_state.count = st.number_input(
                "Количество выбросов",
                #min_value=1, 
                #max_value=100,
                value=10
            )

        par8, par9 = st.columns(2)

        with par8:
            st.session_state.seed_noise = st.number_input(
                "Seed шума",
                #min_value=0, 
                #max_value=9999,
                value=st.session_state.seed_noise
            )
        with par9:
            st.session_state.seed_miss = st.number_input(
                "Seed выбросов",
                #min_value=0, 
                #max_value=9999,
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