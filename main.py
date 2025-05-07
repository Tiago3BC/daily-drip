import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data_cleaning import clean_rain_data

st.set_page_config(
    page_title="The Daily Drip",
    page_icon="☔️",
    layout="wide",
)

uploaded_file = st.sidebar.file_uploader(
    "Upload your [**MeteoBlue**](https://www.meteoblue.com/en/weather/archive/export?daterange=2024-01-01%20-%202025-05-06&locations%5B%5D=jardim-de-bel%25c3%25a9m_portugal_11810184&domain=NEMSAUTO&params%5B%5D=&params%5B%5D=&params%5B%5D=precip&params%5B%5D=&params%5B%5D=&params%5B%5D=&params%5B%5D=&params%5B%5D=&params%5B%5D=&utc_offset=%2B00%3A00&timeResolution=hourly&temperatureunit=CELSIUS&velocityunit=KILOMETER_PER_HOUR&energyunit=watts&lengthunit=metric&degree_day_type=10%3B30&gddBase=10&gddLimit=30) rain CSV",
    type=["csv"]
)

if uploaded_file is not None:
    with open("temp.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())

    cleaned_df = clean_rain_data("temp.csv")

    st.sidebar.success("Data cleaned successfully! Here's a snippet:")
    st.sidebar.dataframe(cleaned_df.head(10))

    rain_data = cleaned_df

    csv = cleaned_df.to_csv(index=False).encode("utf-8")
    st.sidebar.download_button(
        "Download cleaned CSV",
        data=csv,
        file_name="rain-data-cleaned.csv",
        mime="text/csv",
    )

else:
    rain_data = pd.read_csv("fallback.csv")


rain_data["Date"] = pd.to_datetime(rain_data["Date"]).dt.date

st.markdown(
    "<h1 style='text-align: left;'>The Daily Drip ☔️</h1>", unsafe_allow_html=True
)
st.markdown("<h3 style='text-align: left;'>Dashboard 1</h1>", unsafe_allow_html=True)

##--------------------------------------------DASHBOARD 1#--------------------------------------------
# Create containers for the layout
col1, col2, col3, col4 = st.columns((1, 2, 1, 1))
container1 = col1.container(height=517, border=True)
container2 = col2.container(height=517, border=True)
container3 = col3.container(height=517, border=True)
container4 = col4.container(height=517, border=True)

st.markdown("---")
st.markdown("<h3 style='text-align: left;'>Dashboard 2</h3>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns((1, 2, 1, 1))
d2_container1 = col1.container(height=517, border=True)
d2_container2 = col2.container(height=517, border=True)
d2_container3 = col3.container(height=517, border=True)
d2_container4 = col4.container(height=517, border=True)

# Controls D1
container4.markdown(
    "<h3 style='text-align: center;'>Controls 🎮</h3>", unsafe_allow_html=True
)

# Location selection D1
container4.write("##### Location")
location = container4.selectbox("Select a location:", options="Belém", index=0)

# Controls for D1 (dates)
container4.write("##### Date Range Selection")

start_date = container4.date_input(
    "From:",
    value="2024-01-01",
    min_value=rain_data["Date"].min(),
    max_value=rain_data["Date"].max(),
)
end_date = container4.date_input(
    "To:",
    value="2024-01-31",
    min_value=rain_data["Date"].min(),
    max_value=rain_data["Date"].max(),
)

# Controls D2
d2_container4.markdown(
    "<h3 style='text-align: center;'>Controls 🎮</h3>", unsafe_allow_html=True
)

# Location selection D2
d2_container4.write("##### Location")
location = d2_container4.selectbox(
    "Select a location:", options="Belém", index=0, key="d2_location"
)

# Date range selection
d2_container4.write("##### Date Range Selection")

# Controls for D2(dates)
d2_start_date = d2_container4.date_input(
    "From:",
    value="2025-01-01",
    min_value=rain_data["Date"].min(),
    max_value=rain_data["Date"].max(),
    key="d2_start",
)
d2_end_date = d2_container4.date_input(
    "To:",
    value="2025-01-31",
    min_value=rain_data["Date"].min(),
    max_value=rain_data["Date"].max(),
    key="d2_end",
)

# Filter data for Dashboard 1
mask = (rain_data["Date"] >= start_date) & (rain_data["Date"] <= end_date)
filtered_data = rain_data.loc[mask]

# Filter data for Dashboard 2
d2_mask = (rain_data["Date"] >= d2_start_date) & (rain_data["Date"] <= d2_end_date)
d2_filtered_data = rain_data.loc[d2_mask]

# Precompute values needed in both dashboards
total_rainfall = filtered_data["Precipitation (mm)"].sum()
d2_total_rainfall = d2_filtered_data["Precipitation (mm)"].sum()
average_rainfall = filtered_data["Precipitation (mm)"].mean()
d2_average_rainfall = d2_filtered_data["Precipitation (mm)"].mean()
max_rainfall = filtered_data["Precipitation (mm)"].max()
d2_max_rainfall = d2_filtered_data["Precipitation (mm)"].max()
rainy_days = filtered_data[filtered_data["Precipitation (mm)"] > 0].shape[0]
d2_rainy_days = d2_filtered_data[d2_filtered_data["Precipitation (mm)"] > 0].shape[0]
total_days = (end_date - start_date).days + 1
d2_total_days = (d2_end_date - d2_start_date).days + 1


container1.markdown(
    "<h3 style='text-align: center;'>Intensity 🌧️</h3>", unsafe_allow_html=True
)

container2.markdown(
    "<h3 style='text-align: center;'>Daily Distribution 🗓️</h3>", unsafe_allow_html=True
)

# Comment
container4.write(
    "*The Information was precleaned so it only shows data from ***7am*** to ***17pm***.*"
)

# Validate interval
if start_date > end_date:
    st.error("Start date must be before end date.")
else:
    # Filter data
    mask = (rain_data["Date"] >= start_date) & (rain_data["Date"] <= end_date)
    filtered_data = rain_data.loc[mask]

    # Display bar chart
    chart_data = filtered_data.copy()
    chart_data["Date"] = chart_data["Date"].astype(str)
    container2.bar_chart(
        chart_data.set_index("Date")["Precipitation (mm)"], color="#9370db", height=412
    )

    # Display donut chart
    chart_data = filtered_data.copy()
    intensity_counts = (
        chart_data["Rain Intensity"]
        .value_counts()
        .reindex(["No Rain", "Mild Rain", "Moderate Rain", "Heavy Rain"], fill_value=0)
    )
    fig = go.Figure(
        data=[
            go.Pie(
                labels=intensity_counts.index,
                values=intensity_counts.values,
                hole=0.6,
                marker=dict(colors=["#dda0dd", "#9370db", "#8a2be2", "#4b0082"]),
                textinfo="percent",
                textfont=dict(color="white"),
                textposition="inside",
            )
        ]
    )

    fig.update_layout(
        height=300,
        margin=dict(t=10, b=10, l=0, r=0),
        legend=dict(orientation="h", yanchor="top", y=0.0, xanchor="center", x=0.5),
    )

    container1.plotly_chart(fig, use_container_width=True)

container3.markdown(
    "<h3 style='text-align: center;'>Stats #️⃣</h3>", unsafe_allow_html=True
)
# Display total rainfall
container3.metric(
    label="Total Rainfall",
    value=f"{total_rainfall:.2f} mm",
    border=False,
    delta=f"{(total_rainfall - d2_total_rainfall):.2f} mm",
)
# Display average rainfall
container3.metric(
    label="Average Rainfall",
    value=f"{average_rainfall:.2f} mm",
    border=False,
    delta=f"{(average_rainfall - d2_average_rainfall):.2f} mm",
)
# Display maximum rainfall
container3.metric(
    label="Maximum Rainfall in a Single Day",
    value=f"{max_rainfall:.2f} mm",
    border=False,
    delta=f"{(max_rainfall - d2_max_rainfall):.2f} mm",
)
# Display as a combined message
container3.metric(
    label="Rain Frequency",
    value=f"{rainy_days} out of {total_days}",
    help="Number of days with rain vs total selected days",
    border=False,
    delta=f"{(rainy_days - d2_rainy_days)} days",
)

# --------------------------------------------DASHBOARD 2#--------------------------------------------

d2_container1.markdown(
    "<h3 style='text-align: center;'>Intensity 🌧️</h3>", unsafe_allow_html=True
)

d2_container2.markdown(
    "<h3 style='text-align: center;'>Daily Distribution 🗓️</h3>", unsafe_allow_html=True
)

# Comment
d2_container4.write(
    "*The information was precleaned so it only shows data from ***7am*** to ***17pm***.*"
)

# Validate interval
if d2_start_date > d2_end_date:
    st.error("Start date must be before end date.")
else:
    # Filter data
    d2_mask = (rain_data["Date"] >= d2_start_date) & (rain_data["Date"] <= d2_end_date)
    d2_filtered_data = rain_data.loc[d2_mask]

    # Display bar chart
    d2_chart_data = d2_filtered_data.copy()
    d2_chart_data["Date"] = d2_chart_data["Date"].astype(str)

    d2_container2.bar_chart(
        d2_chart_data.set_index("Date")["Precipitation (mm)"],
        color="#66b3ff",
        height=412,
    )

    # Display donut chart
    d2_chart_data = d2_filtered_data.copy()
    d2_intensity_counts = (
        d2_chart_data["Rain Intensity"]
        .value_counts()
        .reindex(["No Rain", "Mild Rain", "Moderate Rain", "Heavy Rain"], fill_value=0)
    )
    d2_fig = go.Figure(
        data=[
            go.Pie(
                labels=d2_intensity_counts.index,
                values=d2_intensity_counts.values,
                hole=0.6,
                marker=dict(colors=["#cce5ff", "#66b3ff", "#339af0", "#1864ab"]),
                textinfo="percent",
                textfont=dict(color="white"),
                textposition="inside",
            )
        ]
    )

    d2_fig.update_layout(
        height=300,
        margin=dict(t=10, b=10, l=0, r=0),
        legend=dict(orientation="h", yanchor="top", y=-0.0, xanchor="center", x=0.5),
    )

    d2_container1.plotly_chart(d2_fig, use_container_width=True)

d2_container3.markdown(
    "<h3 style='text-align: center;'>Stats #️⃣</h3>", unsafe_allow_html=True
)
# Display total rainfall
d2_container3.metric(
    label="Total Rainfall",
    value=f"{d2_total_rainfall:.2f} mm",
    border=False,
    delta=f"{(d2_total_rainfall - total_rainfall):.2f} mm",
)
# Display average rainfall
d2_container3.metric(
    label="Average Rainfall",
    value=f"{d2_average_rainfall:.2f} mm",
    border=False,
    delta=f"{(d2_average_rainfall - average_rainfall):.2f} mm",
)
# Display maximum rainfall
d2_container3.metric(
    label="Maximum Rainfall in a Single Day",
    value=f"{d2_max_rainfall:.2f} mm",
    border=False,
    delta=f"{(d2_max_rainfall - max_rainfall):.2f} mm",
)
# Display as a combined message
d2_container3.metric(
    label="Rain Frequency",
    value=f"{d2_rainy_days} out of {d2_total_days}",
    help="Number of days with rain vs total selected days",
    border=False,
    delta=f"{(d2_rainy_days - rainy_days)} days",
)

# --------------------------------------------DATA COMPARISON#--------------------------------------------
st.markdown("---")
st.markdown(
    "<h4 style='text-align: center;'>Compare the Raw Data or Export it Yourself 📁</h4>",
    unsafe_allow_html=True,
)

col1, col2 = st.columns((1, 1))
d3_container1 = col1.container(border=False)
d3_container2 = col2.container(border=False)

with d3_container1.expander("Show data (Dashboard 1)", expanded=False):
    st.dataframe(filtered_data.reset_index(drop=True))

with d3_container2.expander("Show data (Dashboard 2)", expanded=False):
    st.dataframe(d2_filtered_data.reset_index(drop=True))
