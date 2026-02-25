import toml
import streamlit as st

st.title("Модель для обнаружения аномалий в числовых последовательностях")

but0, but1= st.columns(2)
with but0:
    st.button("Сгенерировать новые данные", use_container_width = True,
              type = "primary")
with but1:
    st.button("Найти аномалии методом А")
    st.button("Найти аномалии методом Б")
