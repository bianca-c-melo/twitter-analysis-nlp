import streamlit as st
import plotly.express as px
from analysis import bi_grams
from analysis import uni_grams
from analysis import tri_grams

colT1, colT2 = st.columns([1,8])
with colT2:
    st.title("Análise de Tweets  Tópico: Diversidade")


st.info('Os N-grams apresentados são as N palavras combinadas mais faladas no tópico pesquisado.', icon="ℹ️")
st.info('Quantidade de Tweets analisados: 60.000', icon="ℹ️")


st.subheader('Unigrams')

fig = px.bar(uni_grams, y='palavras', x="contagem", template='plotly_white', orientation='h')
fig.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'}, width=900, height=543)
st.plotly_chart(fig)


st.subheader('Bigrams')

fig = px.bar(bi_grams, y='palavras', x="contagem", template='plotly_white', orientation='h')
fig.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'}, width=900, height=543)
st.plotly_chart(fig)


st.subheader('Trigrams')

fig = px.bar(tri_grams, y='palavras', x="contagem", template='plotly_white', orientation='h')
fig.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},width=900, height=543)
st.plotly_chart(fig)


