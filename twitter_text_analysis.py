import streamlit as st
import plotly.express as px
from analysis import bigrams
from analysis import unigrams
from analysis import trigrams

colT1,colT2 = st.columns([1,8])
with colT2:
  st.title("Análise de Tweets  Tópico: Diversidade")


st.info('Os N-grams apresentados são as N palavras combinadas mais faladas no tópico pesquisado.', icon="ℹ️")
st.info('Quantidade de Tweets analisados: 60.000', icon="ℹ️")

st.subheader('Unigrams')

fig = px.bar(unigrams,
                y='words',
                x="count",
                template='plotly_white',
                   orientation='h')
fig.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'}, width=900, height=543)
fig.update_yaxes(automargin=True)
fig.update_layout(bargap=0.2)
st.plotly_chart(fig)

st.subheader('Bigrams')

fig = px.bar(bigrams,
                y='words',
                x="count",
                template='plotly_white',
                   orientation='h')
fig.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'}, width=900, height=543)
fig.update_yaxes(automargin=True)
fig.update_layout(bargap=0.2)
st.plotly_chart(fig)


st.subheader('Trigrams')

fig = px.bar(trigrams,
                y='words',
                x="count",
                template='plotly_white',
                   orientation='h',
             )
fig.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},width=900, height=543
                  )
fig.update_yaxes(automargin=True)
fig.update_layout(bargap=0.2)
st.plotly_chart(fig)


