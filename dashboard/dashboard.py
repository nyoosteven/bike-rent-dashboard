import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title('Bike Sharing Dataset Analysis')

day_df = pd.read_csv('data/day.csv')
hour_df = pd.read_csv('data/hour.csv')

seasons = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
day_df['season'] = day_df['season'].map(seasons)
hour_df['season'] = hour_df['season'].map(seasons)

tahun = {0:'2011', 1:'2012'}
day_df['yr'] = day_df['yr'].map(tahun)
hour_df['yr'] = hour_df['yr'].map(tahun)

months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
day_df['mnth'] = day_df['mnth'].map(months)
hour_df['mnth'] = hour_df['mnth'].map(months)

day = {0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday', 4:'friday', 5:'saturday', 6:'sunday'}
day_df['weekday'] = day_df['weekday'].map(day)
hour_df['weekday'] = hour_df['weekday'].map(day)

weather = {1:'clear', 2:'mist', 3:'light snow', 4:'heavy rain'}
day_df['weathersit'] = day_df['weathersit'].map(weather)
hour_df['weathersit'] = hour_df['weathersit'].map(weather)

day_df['dteday']=pd.to_datetime(day_df['dteday'])
hour_df['dteday']=pd.to_datetime(hour_df['dteday'])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:

    st.write('Bike Sharing Analysis by Nyoo Steven')
    st.write('m010d4ky2698@bangkit.academy')
    start_date, end_date = st.date_input(
        label='Range of Time', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

day_df = day_df[(day_df["dteday"] >= str(start_date)) &
                (day_df["dteday"] <= str(end_date))]

hour_df = hour_df[(hour_df["dteday"] >= str(start_date)) &
                (hour_df["dteday"] <= str(end_date))]

st.subheader('Best Customer Based on RFM Parameters (day)')
rfm_df = day_df.groupby(by="weekday", as_index=False).agg({
    "dteday": "max", 
    "instant": "nunique", 
    "cnt": "sum" 
})

rfm_df.columns = ["day", "max_order_timestamp", "frequency", "monetary"]
rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
recent_date = day_df["dteday"].dt.date.max()
rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(25, 6))
colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]
sns.barplot(y="recency", x="day", data=rfm_df.sort_values(by="recency", ascending=True).head(5),  hue="day", ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
ax[0].tick_params(axis ='x', labelsize=15)
sns.barplot(y="frequency", x="day", data=rfm_df.sort_values(by="frequency", ascending=False).head(5),  hue="day", ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=15)
sns.barplot(y="monetary", x="day", data=rfm_df.sort_values(by="monetary", ascending=False).head(5),  hue="day", ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary", loc="center", fontsize=18)
ax[2].tick_params(axis='x', labelsize=15)
plt.tight_layout()
st.pyplot(plt)


# st.subheader('Korelasi pada setiap kolom')
# plt.figure(figsize=(12,8))
# sns.heatmap(hour_df.corr(), annot=True)
# st.pyplot(plt)

st.subheader('Distribusi Rental Sepeda per Jam')
plt.figure(figsize=(12,6))
ax = sns.boxplot(x='hr', y='cnt', data=hour_df)
for i in ax.containers:
    ax.bar_label(i,)
plt.tight_layout()
st.pyplot(plt)

st.subheader('Rental Counts Working Day vs Non Working Days')
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
workingday_df = hour_df[hour_df['workingday'] == 1]
non_workingday_df = hour_df[hour_df['workingday'] == 0]
axes[0].bar(workingday_df['hr'], workingday_df['cnt'])
axes[0].set_title('Rental Counts per Hour (Working Day)', fontsize=15)
axes[0].set_xlabel('Hour')
axes[0].set_ylabel('Count')
axes[1].bar(non_workingday_df['hr'], non_workingday_df['cnt'])
axes[1].set_title('Rental Counts per Hour (Non-Working Day)', fontsize=15)
axes[1].set_xlabel('Hour')
axes[1].set_ylabel('Count')
plt.tight_layout()
st.pyplot(plt)

st.subheader('Perbandingan clusters by season dan temperature')
plt.figure(figsize=(10,6))
custom_palette = sns.color_palette("husl", 4)
sns.scatterplot(x='temp', y='cnt', data=day_df, hue='season', palette=custom_palette)
plt.xlabel("Temperature (degC)")
plt.ylabel("Total Rides")
plt.title("Clusters of bikeshare rides by season and temperature")
plt.tight_layout()
st.pyplot(plt)

st.subheader('Pengaruh cuaca dan musim terhadap produktivitas Bike Sharing')
col1, col2 = st.columns(2)

with col1:
    weather = hour_df.groupby("weathersit").cnt.sum().sort_values(ascending=False).reset_index()
    plt.figure(figsize=(8,5))
    sns.barplot(y="cnt", x="weathersit", data=weather)
    plt.title('Number of User by Weather', fontsize=15)
    plt.tight_layout()
    st.pyplot(plt)

with col2:
    season = hour_df.groupby("season").cnt.sum().sort_values(ascending=False).reset_index()
    plt.figure(figsize=(8,5))
    sns.barplot(y="cnt", x="season", data=season)
    plt.title('Number of User by Season', fontsize=15)
    plt.tight_layout()
    st.pyplot(plt)

st.subheader('Produktivitas Bike Sharing tiap bulan')
monthly_sum = day_df.groupby(['mnth', 'yr'])['cnt'].sum().reset_index()
monthly_sum['month_yr'] = pd.to_datetime(monthly_sum['yr'].astype(str) + '-' + monthly_sum['mnth'].astype(str))
monthly_sum = monthly_sum.sort_values('month_yr')
monthly_sum_2011 = monthly_sum[monthly_sum.yr == '2011']
monthly_sum_2012 = monthly_sum[monthly_sum.yr == '2012']

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
if len(monthly_sum_2011):
    axes[0].bar(monthly_sum_2011['month_yr'].dt.strftime('%m_%Y'), monthly_sum_2011['cnt'], color='skyblue')
    axes[0].set_xlabel('Month_Year')
    axes[0].set_ylabel('Total Rides')
    axes[0].set_title('Total Rides in 2011')
    axes[0].set_xticklabels(monthly_sum_2011['month_yr'].dt.strftime('%m_%Y'), rotation=45, ha='right')

if len(monthly_sum_2012):
    axes[1].bar(monthly_sum_2012['month_yr'].dt.strftime('%m_%Y'), monthly_sum_2012['cnt'], color='orange')
    axes[1].set_xlabel('Month_Year')
    axes[1].set_ylabel('Total Rides')
    axes[1].set_title('Total Rides in 2012')
    axes[1].set_xticklabels(monthly_sum_2012['month_yr'].dt.strftime('%m_%Y'), rotation=45, ha='right')
plt.tight_layout()
st.pyplot(plt)

st.subheader('Produktivitas Bike Sharing selama 24 jam')
plt.figure(figsize=(12,6))
ax = sns.boxplot(x='hr', y='cnt', data=hour_df)
plt.title('Distribusi Rental Sepeda per Jam')
for i in ax.containers:
    ax.bar_label(i,)
plt.tight_layout()
st.pyplot(plt)

plt.figure(figsize=(20, 5))
for day_type, color in zip(hour_df['workingday'].unique(), ['blue', 'orange']):
    subset = hour_df[hour_df['workingday'] == day_type]
    plt.errorbar(subset.groupby('hr')['cnt'].mean().index, 
                 subset.groupby('hr')['cnt'].mean().values,
                 yerr=subset.groupby('hr')['cnt'].std().values / len(subset), 
                 fmt='-o', label=day_type, color=color)

plt.title('Bike Sharing Productivity Based on Time', fontsize=15)
plt.xlabel('Hour')
plt.ylabel('Total Pengguna')
plt.legend(title='Working Day')
st.pyplot(plt)

st.caption(f"Copyright © 2024 All Rights Reserved [Nyoo Steven]")