import pandas as pd

# Load dataset
df = pd.read_csv("Atlantic_Spain(1).csv")

#show first rows
print(df.head())

#show info
print(df.info())

# Clean text columns
df['song'] = df['song'].str.strip().str.lower()
df['artist'] = df['artist'].str.strip().str.lower()

# Convert date column
df['date'] = pd.to_datetime(df['date'])

# Create unique song id
df['song_id'] = df['song'] + "_" + df['artist']

print(df.head())

# Check entries per day
print(df.groupby('date').size().head())

# Build lifecycle table
lifecycle = df.groupby('song_id').agg({'date' : ['min', 'max'],'position' : ['min', 'count']})

# Rename columns
lifecycle.columns = ['entry_date', 'exit_date', 'peak_position', 'days_count']

# Calculate total days
lifecycle['days_on_playlist'] = (lifecycle['exit_date'] - lifecycle['entry_date']).dt.days + 1

print(lifecycle.head())

# Peak date
#Row where position is best(minimum)
peak_dates = df.loc[df.groupby('song_id')['position'].idxmin()]
#keep only reuired columns
peak_dates = peak_dates[['song_id', 'date']]
#rename
peak_dates = peak_dates.rename(columns={'date' : 'peak_date'})

# Merge with lifecylce
lifecycle = lifecycle.merge(peak_dates, on='song_id')

# Calculate entry to peak
lifecycle['entry_to_peak'] = (lifecycle['peak_date'] - lifecycle['entry_date']).dt.days

print(lifecycle.head())

#unique song-level attributes
extra = df[['song_id', 'is_explicit', 'album_type']].drop_duplicates()

#merge with licycle table
lifecycle = lifecycle.merge(extra, on='song_id')

print(lifecycle.head())

#calc KPI
print("Average Days on Playlist: ", lifecycle['days_on_playlist'].mean())

print("Average Entry to Peak: ",lifecycle['entry_to_peak'].mean())

print("Average Peak Position: ", lifecycle['peak_position'].mean())

print(lifecycle.groupby('is_explicit')['days_on_playlist'].mean())

print(lifecycle.groupby('album_type')['days_on_playlist'].mean())

# sort data
df = df.sort_values(['song_id', 'date'])

# Finds gap btn appearance
df['prev_date'] = df.groupby('song_id')['date'].shift(1)

df['gap_days'] = (df['date'] - df['prev_date']).dt.days

print(df[['song_id', 'date', 'prev_date', 'gap_days']].head(10))

# New entries
new_entries = df[df['prev_date'].isna()]

print("Total Number of New Entries: ",new_entries.shape[0])

# Daily new songs entries
daily_entries = new_entries.groupby('date').size()

print(daily_entries.head())

# Stability of the playlist
daily_unique = df.groupby('date')['song_id'].nunique()

print(daily_unique.head())

# Churn rate
churn_rate = daily_entries.mean()

print("Average Daily Churn: ", churn_rate)

# Songs that dont last long
short_life = lifecycle[lifecycle['days_on_playlist'] <= 5]

print("Short-life sons: ", len(short_life))

import matplotlib.pyplot as plt
#daily entries plot
daily_entries.plot(title="Daily New Entries")
plt.show()
