import toml
import streamlit as st
import generator as gen
import matplotlib.pyplot as plt
#import warnings
#warnings.filterwarnings('ignore')

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
    axes[2].scatter(x[data["where"]], data["dataline_miss"][data["where"]], label="Выбросы", color="black", s=35, zorder=3)
    if data_analysed is not None:
        axes[2].scatter(x[data_analysed], data["dataline_miss"][data_analysed], label="Аномальные точки", color="yellow", s=35, zorder=4)
    axes[2].set_title("Последовательность с выбросами")
    axes[2].set_xlabel("x")
    axes[2].set_ylabel("y")
    axes[2].grid(True, alpha=0.3)
    axes[2].legend()

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

#ахаха, надеюсь, ещё придумаю, как это сделать менее грубо, но иначе streamlit кидает варны, которые сильно мешают

st.set_page_config(layout="centered") #layout = "wide" - по ширине страницы, пока не знаю, как лучше

st.title("Модель для обнаружения аномалий в числовых последовательностях")

type = st.selectbox("Выберите функцию", ["Линейная", "Степенная", "Корень", "Синус", "Косинус", "Тангенс"])

arg1, arg2, arg3 = st.columns(3)
with arg1:
    a = st.number_input("a", value=2.6667)
with arg2:
    b = st.number_input("b", value=0.45)
with arg3:
    c = st.number_input("c (только для корня и степени)")

if type == "Линейная": 
    type = "linear"
    args = [a, b]
elif type == "Степенная": 
    type = "power"
    args = [a, b, c]
elif type == "Корень": 
    type = "root"
    args = [a, b, c]
elif type == "Синус": 
    type = "sin"
    args = [a, b]
elif type == "Косинус": 
    type = "cos"
    args = [a, b]
elif type == "Тангенс": 
    type = "tan"
    args = [a, b]
    
if 'count' not in st.session_state:
    st.session_state.length = 100
    st.session_state.scaling = 10
    st.session_state.mode_noise = 1
    st.session_state.strength = 0.1
    st.session_state.sleek = 10
    st.session_state.mode_miss = 11
    st.session_state.count = 10

data = gen.get_data(func={"type":type,"args":args},length=st.session_state.length,scaling=st.session_state.scaling,mode_noise=st.session_state.mode_noise,
                    strength=st.session_state.strength,sleek=st.session_state.sleek,mode_miss=st.session_state.mode_miss,count=st.session_state.count,seed_noise=111,seed_miss=993)

# Если без draw_plots:
#fig, ax = plt.subplots(figsize=(12, 6)) 
#fig = gen.draw_data(data, 3)
#graphs = st.pyplot(fig)

draw_plots(data)
plt.close('all')

gen_new = st.button("Сгенерировать новые данные", type = "primary", use_container_width = True)

if gen_new:
    st.rerun()

but0, but1= st.columns(2)

with but0:
   st.button("Найти аномалии статистическим методом", type = "primary", use_container_width = True)

with but1:
    st.button("Найти аномалии ML методом", type = "primary", use_container_width = True)

st.header("Подробное редактирование:")

par1, par2, par3, par4 = st.columns(4)
with par1:
    st.session_state.length = st.number_input("Длина", value=100)
with par2:
    st.session_state.scaling = st.number_input("Растягивание (точность)", value=10)
with par3:
    st.session_state.mode_noise = st.number_input("Режим шума", value=1)
with par4:
    st.session_state.strength = st.number_input("Сила шума", value=0.1)

par5, par6, par7 = st.columns(3)
with par5:
    st.session_state.sleek = st.number_input("Растяжимость шума", value=10)
with par6:
    st.session_state.mode_miss = st.number_input("Режим внесения выбросов", value=11)
with par7:
    st.session_state.count = st.number_input("Количество выбросов", value=10)