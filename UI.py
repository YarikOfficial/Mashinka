import toml
import streamlit as st
import generator
import matplotlib.pyplot as plt
'''
Генерировать числовую последовательность (временной ряд) с заданными 
параметрами (например: синусоида с шумом + случайные выбросы). 
Выбирать алгоритм поиска аномалий (статистический или ML). 
Отображать график, где цветом выделены найденные аномальные точки. 
Выводить базовые метрики (сколько аномалий найдено). 
'''

def Data():
    func = {"type":"linear","args":[3,1]}
    N = 10
    dataline,data = generator.np_gen_func_line(func,N,10,False)
    dataline_miss,data = generator.get_mis(dataline,data,11,round(N/10))
    return dataline
    
st.title("Модель для обнаружения аномалий в числовых последовательностях")

#st.selectbox("Выберите функцию", ["Линейная", "Степенная", "Корень", "Синус", "Косинус", "Тангенс"])

plt.plot(Data())
st.pyplot(plt.gcf())

st.button("Сгенерировать новые данные", type = "primary", use_container_width = True)

but0, but1= st.columns(2)

with but0:
   st.button("Найти аномалии статистическим методом", type = "primary", use_container_width = True)

with but1:
    st.button("Найти аномалии ML методом", type = "primary", use_container_width = True)

