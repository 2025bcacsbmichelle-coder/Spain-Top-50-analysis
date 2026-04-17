import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Top 50 🎵Spain's Music Analysis")

#load data
df = pd.read_csv("Atlantic_Spain(1).csv")

#preprocess
df['song'] = df['song'].str.strip().str.lower()
df['artist'] = df['artist'].str.strip().str.lower()
df['song_id'] = df['song'] + "_" + df['artist']
df['date'] = pd.to_datetime(df['date'])

#lifecycle
lifecycle = df.groupby('song_id').agg({'date' : ['min', 'max'], 'position' : ['min', 'max']})

lifecycle.columns = ['entry_date', 'exit_date', 'peak_position', 'days_count']

lifecycle['days_on_playlist'] = (lifecycle['exit_date'] - lifecycle['entry_date']).dt.days + 1

#KPI cards
st.subheader("📈Key Performance Indicators")

col1, col2, col3 = st.columns(3)

col1.metric("Average Days on Playlist", round(lifecycle['days_on_playlist'].mean(), 2))
col2.metric("Average Peak Position", round(lifecycle['peak_position'].mean(), 2))
col3.metric("Total Songs", lifecycle.shape[0])

# Churn
df = df.sort_values(['song_id', 'date'])
df['prev_date'] = df.groupby('song_id')['date'].shift(1)

new_entries = df[df['prev_date'].isna()]

daily_entries = new_entries.groupby('date').size()

st.subheader("🔄️Playlist Churn (Daily New Entries)")

fig, ax = plt.subplots()
daily_entries.plot(ax=ax)
st.pyplot(fig)

#Explicit vs lifecycle chart
extra = df[['song_id', 'is_explicit']].drop_duplicates()
lifecycle = lifecycle.merge(extra, on='song_id')

st.subheader("🚫Explicit vs Non-Explicit Perfomance")

fig2, ax2 = plt.subplots()
sns.boxplot(x='is_explicit', y="days_on_playlist", data=lifecycle, ax=ax2)
st.pyplot(fig2)

st.subheader("📋Lifecycle Data")
st.dataframe(lifecycle)