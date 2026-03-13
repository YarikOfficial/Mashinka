import toml
import streamlit as st
import generator
import matplotlib.pyplot as plt

#Генерировать числовую последовательность (временной ряд) с заданными 
#параметрами (например: синусоида с шумом + случайные выбросы). 
#Выбирать алгоритм поиска аномалий (статистический или ML). 
#Отображать график, где цветом выделены найденные аномальные точки. 
#Выводить базовые метрики (сколько аномалий найдено). 


def Draw(type, args):
    func = {"type":type,"args":args}
    N = 10
    if type == "linear" or type == "power" or type == "root":
        dataline,data = generator.np_gen_func_line(func,N,10,False)
    dataline_miss,data = generator.get_mis(dataline,data,11,round(N/10))
    return dataline
    
st.title("Модель для обнаружения аномалий в числовых последовательностях")

type = st.selectbox("Выберите функцию", ["Линейная", "Степенная", "Корень", "Синус", "Косинус", "Тангенс"])

if type == "Линейная": type = "linear"
elif type == "Степенная": type = "power"
elif type == "Корень": type = "root"
elif type == "Синус": type = "sin"
elif type == "Косинус": type = "cos"
elif type == "Тангенс": type = "tan"

arg1, arg2, arg3 = st.columns(3)
with arg1:
    a = st.text_input("a")
with arg2:
    b = st.text_input("b")
with arg3:
    c = st.text_input("c")

plt.plot(Draw("linear",[3,1]))
st.pyplot(plt.gcf())

if st.button("Сгенерировать новые данные", type = "primary", use_container_width = True):
    plt.plot(Draw(type,[a,b]))
    st.pyplot(plt.gcf())

but0, but1= st.columns(2)

with but0:
   st.button("Найти аномалии статистическим методом", type = "primary", use_container_width = True)

with but1:
    st.button("Найти аномалии ML методом", type = "primary", use_container_width = True)

