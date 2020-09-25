# Data Science Project showing the number of COVID-19 Cases in the country and in counties of New Jersey
# Created by Ibrahim Usmani


# Import the required libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Assign the case variable to read the dataset you are using
cases = pd.read_csv("https://raw.githubusercontent.com/higgamo/DSfiles/master/covid_19_data.csv")

# Import plotly express library for the line graph
import plotly.express as px 

# The following code till Line 38 is the code for the line graph
grp = cases.groupby(['ObservationDate', 'Country/Region'])['Confirmed', 'Deaths', 'Recovered'].max()
grp = grp.reset_index()
grp['Date'] = pd.to_datetime(grp['ObservationDate'])
grp['Date'] = grp['Date'].dt.strftime('%m/%d/%Y')
grp['Active'] = grp['Confirmed'] - grp['Recovered'] - grp['Deaths']
grp['Country'] = grp['Country/Region']
fig = px.choropleth(grp, locations="Country", locationmode='country names',
 color="Confirmed",
 hover_name="Country/Region",
 hover_data = [grp.Recovered,grp.Deaths,grp.Active],
 projection="mercator",
 animation_frame="Date",width=1000, height=700,
 color_continuous_scale='Reds',
 range_color=[1000,50000],
 title='World Map of Coronavirus Confirmed Cases')
fig.update(layout_coloraxis_showscale=True)

# Set the variable for the us covid cases
us_covid = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv", header = 0,
dtype={"fips": str}, parse_dates=[0])

# Unique method to classify state
us_covid['state'].unique()

# Query method to define the desired states from the dataset
us_covid_ne = us_covid.query('state == ["Connecticut", "Maine", "Massachusetts", "New Hampshire", "Rhode Island", "Vermont", "New Jersey", "New York", "Pennsylvania"]')

# Import the url library request and url open from python libraries
from urllib.request import urlopen

# Plotting the bar graph as depicted
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
 counties = json.load(response)
import plotly.express as px
us_covid_ne_latest = us_covid_ne.query('date == "03/15/2020"')
fig = px.choropleth_mapbox(us_covid_ne_latest,
 geojson=counties,
 locations='fips',
 color='cases',
 color_continuous_scale="Reds",
 range_color=(0, 10000),
 mapbox_style="carto-positron",
 zoom=3,
 center = {"lat": 37.0902, "lon": -95.7129},
 opacity=0.5
 )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

us_covid_ne2 = us_covid.query('state == ["Vermont", "New Jersey", "New York"]')
us_covid_ne2.head()

plt.figure(figsize=(12,10))
sns.lineplot(x="date", y="cases", hue="state", data=us_covid_ne2)
plt.title('Covid 19 Cases')
plt.show()

nj_covid = us_covid.query('state == "New Jersey"')
nj_covid.head()

covidplot = nj_covid.pivot_table(index="county", values=["cases","deaths"], aggfunc="sum")

plt.figure(figsize=(15,10))
sns.barplot(x=covidplot.index, y="cases", data=covidplot)
plt.xticks(rotation=90)
plt.show()

