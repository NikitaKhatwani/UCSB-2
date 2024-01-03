from re import U
import numpy as np
import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import plotly.offline as pyo
import matplotlib.pyplot as plt
import folium as fo
from streamlit_folium import folium_static, st_folium
from PIL import Image
import plotly.express as px

@st.cache_data
def load_data(path):
    """
    Write 1-2 lines of code here to load the data from CSV to a pandas dataframe
    and return it.
    """
    # Load data
    raw_df = pd.read_excel(path)
    # Move the last row to become the first row
    raw_df = pd.concat([raw_df.iloc[-1:], raw_df.iloc[:-1]], ignore_index=True)
    return raw_df


@st.cache_data
def load_daily_data(path):
    """
    Write 1-2 lines of code here to load the data from CSV to a pandas dataframe
    and return it.
    """
    # Load data
    raw_df = pd.read_excel(path)
    # Move the last row to become the first row
    raw_df = pd.concat([raw_df.iloc[-1:], raw_df.iloc[:-1]], ignore_index=True)
    #covert dates to date time format
    raw_df['Dates'] = pd.to_datetime(raw_df['Dates'])
    # Assuming 'Dates' is the name of your DateTime column
    raw_df.set_index('Dates', inplace=True)
    # Daily sum of all values within the same day
    raw_df = raw_df.resample('D').sum()
    # Reset the index to bring 'Dates' back as a column
    raw_df.reset_index(inplace=True)
    return raw_df





@st.cache_data
def area_pieChart(df2):

    # Replace 'Auxiliary' with 'Academic'
    df2['Building Categorization Notes'] = df2['Building Categorization Notes'].replace('Auxiliary', 'Academic')
    # Group data by building category and sum area
    grouped_data = df2.groupby('Building Categorization Notes')['Building_Area (GSF)'].sum()
    
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(grouped_data, labels=grouped_data.index, autopct='%1.1f%%', startangle=140)
    ax.set_title('Breakdown of Building Area by Building Category')
    ax.axis('equal')  # Equal aspect ratio ensures that the pie chart is drawn as a circle.

    # Display pie chart using Streamlit
    st.pyplot(fig)





def make_graph(index):

    # Create a new figure for the selected building
    fig = go.Figure()

    # Plot the first line (CHW)
    fig.add_trace(
        go.Scatter(x=CW_df['Dates'], y=CW_df.iloc[:,index], mode='lines', name='Chilled water', line=dict(color='#5289C7')))


    # Plot the second line (HW)
    fig.add_trace(
            go.Scatter(x=HW_df['Dates'], y=HW_df.iloc[:, index]+DHW_df.iloc[:, index], mode='lines', name='Hot water',line=dict(color='#FF6961')))

    # # Plot the third line (DHW)
    # fig.add_trace(
    #         go.Scatter(x=DHW_df['Dates'], y=DHW_df.iloc[:, index], mode='lines', name='DHW', line=dict(color='#A94064')))

    # Set title
    fig.update_layout(
        title_text=f"{CW_df.columns[index]}"
    )

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )


    # Display in Streamlit
    st.plotly_chart(fig)


def make_daily_graph(index):

    # Create a new figure for the selected building
    fig = go.Figure()

    # Plot the first line (CHW)
    fig.add_trace(
        go.Scatter(x=CW_df['Dates'], y=CW_daily_df.iloc[:,index], mode='lines', name='Chilled water', line=dict(color='#5289C7')))


    # Plot the second line (HW)
    fig.add_trace(
            go.Scatter(x=HW_df['Dates'], y=HW_daily_df.iloc[:, index]+DHW_daily_df.iloc[:, index], mode='lines', name='Hot water',line=dict(color='#FF6961')))

    # # Plot the third line (DHW)
    # fig.add_trace(
    #         go.Scatter(x=DHW_df['Dates'], y=DHW_daily_df.iloc[:, index], mode='lines', name='DHW', line=dict(color='#A94064')))

    # Set title
    fig.update_layout(
        title_text=f"{CW_df.columns[index]}"
    )

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )


    # Display in Streamlit
    st.plotly_chart(fig)






# MAIN CODE

# Use set_page_config to adjust the layout
st.set_page_config(
    page_title="Your App Title",
    layout="wide",  # Use wide layout for more control over spacing
)


st.title("UCSB Decarbonization")

CHW_path = "UCSB_Chilled Water loads_8670 kWH.xlsx"
HHW_path = "UCSB_Hot water_8670 kWH.xlsx"
DHW_path = "UCSB_DHW_8670 kWH.xlsx"
Area_path = "1204_Program&Areas.xlsx"

with st.spinner(text="Loading data..."):
    CW_df = load_data(CHW_path)
    HW_df = load_data(HHW_path)
    DHW_df = load_data(DHW_path)
    Area_df = load_data(Area_path)
# st.text("Visualize the overall dataset and some distributions here...")

if st.checkbox("Show Area Data"):
    st.write(Area_df)
    area_pieChart(Area_df)

if st.checkbox("Show CHW Raw Data"):
    st.write(CW_df)

if st.checkbox("Show HHW Raw Data"):
    st.write(HW_df)

if st.checkbox("Show DHW Raw Data"):
    st.write(DHW_df)

# st.header("Custom slicing")
# st.text("Implement your interactive slicing tool here...")

# st.header("Person sampling")
# st.text("Implement a button to sample and describe a random person here...")
# Create an empty list to store the graphs
figs = []


# Convert 'DateColumn' to datetime
CW_df['Dates'] = pd.to_datetime(CW_df['Dates'])
HW_df['Dates'] = pd.to_datetime(HW_df['Dates'])
DHW_df['Dates'] = pd.to_datetime(DHW_df['Dates'])

#get maximum number of columns
coolingCols = int(CW_df.shape[1])

#preparing daily data 
CW_daily_df = load_daily_data(CHW_path)
HW_daily_df = load_daily_data(HHW_path)
DHW_daily_df = load_daily_data(DHW_path)



# Create a two-column layout
campus_hourly_col, campus_daily_col = st.columns(2)

# Hourly graph
with campus_hourly_col:
        st.markdown("<h3 style='margin-bottom:-33px;font-size: 20px;'>Hourly</h3>", unsafe_allow_html=True)
        make_graph(23)

# Daily graph
with campus_daily_col:
        st.markdown("<h3 style='margin-bottom:-33px;font-size: 20px;'>Daily</h3>", unsafe_allow_html=True)
        make_daily_graph(23)




#Map code
st.header("Campus Map")

# Subheader with reduced spacing
st.write("Select buildings on the map or from the filter below")

map = fo.Map(location = [34.410567258666674, -119.832], tiles = "cartodbpositron", \
                zoom_start = 15, min_zoom = 14, max_zoom = 2,
                width = "100%", height = "75%")


#plotting all buidligns on map
for i, row in Area_df.iterrows():

    if "total" in row['Building_Name'].lower():
        continue

    # Skip rows with NaN values in Latitude or Longitude
    if pd.isna(row['Latitude']) or pd.isna(row['Longitude']):
        continue

    # Extracting information from the current row
    popContent = f"Name: {row['Building_Name']} <br> \
        Program: {row['Building Categorization Notes']} <br>\
        Area: {row['Building_Area (GSM)']} <br>  "

    # Creating a Folium Circle marker
    fo.Circle(
        radius=15,
        location=[row['Latitude'], row["Longitude"]],
        fill=True,
        fill_opacity=1,
        popup=fo.Popup(popContent, min_width=200, max_width=200),
        tooltip=row['Building_Name']
    ).add_to(map)


######here



# Create a list of building names with an initial option
building_names = ["Select buildings"] + list(CW_df.columns[1:])

filterCol,mapCol, = st.columns([1,4])
index = np.nan
selection_method = np.nan
if "selected_building" not in st.session_state:
    st.session_state.selected_building = "Select buildings"


if "selected_building_map" not in st.session_state:
    st.session_state.selected_building_map = "Select buildings"

with filterCol:
# st.subheader('Utility graphs', divider="grey")
# Allow the user to select a building
    old_selection = st.session_state.selected_building
    selected_building_filter = st.multiselect("", building_names)
    st.session_state.selected_building = selected_building_filter
    if st.session_state.selected_building != old_selection:
        selection_method = "selectBox"



with mapCol:
        st_map = st_folium(map, width = 1500, height = 750)


        old_selection_map = st.session_state.selected_building_map
        point = st_map["last_object_clicked"]
        if point:
            latitude, longitude = point['lat'], point['lng']
        else:
            # latitude = Area_df.iloc[1]["Latitude"]
            # longitude = Area_df.iloc[1]["Longitude"]
            latitude = np.nan


        if np.isnan(latitude):
            # Subheader with reduced spacing
            pass
        else:
            df_point = Area_df[(Area_df["Latitude"] == latitude) & (Area_df["Longitude"] == longitude)]
            selected_building_map =   df_point["Building_Name"].iloc[0]
            st.session_state.selected_building_map = selected_building_map
            if st.session_state.selected_building_map != old_selection_map:
                selection_method = "map"
            # index = building_names.index(selected_building)  
            st.markdown(f'<p class = "smallSubHeader" > Your Selected Building is {df_point["Building_Name"].iloc[0]}. </p>'
                    , unsafe_allow_html = True)

            st.write(df_point)
    # # Highlight the building on the map
    #     selected_building_marker = f"{selected_building_filter}"
    #     fo.Marker(
    #             location=[latitude, longitude],
    #             popup=selected_building_marker,
    #             icon=fo.Icon(color='red', icon='info-sign'),
    #         ).add_to(st_map)    





if selection_method == "selectBox":
    # Get the index of the selected building
    for bldg in selected_building_filter:
        index = building_names.index(bldg)
elif selection_method == "map":
    index = building_names.index(selected_building_map)
 
if np.isnan(index):
    # Subheader with reduced spacing
     pass
else:
    # Subheader with reduced spacing
    st.markdown("<h3 style='margin-bottom:-25px;'>Utility graphs</h3>", unsafe_allow_html=True)
    # st.markdown("<h3 style='margin-bottom:-33px;font-size: 20px;'>Hourly</h3>", unsafe_allow_html=True)
    # make_graph(index)
    # st.markdown("<h3 style='margin-bottom:-33px;font-size: 20px;'>Daily</h3>", unsafe_allow_html=True)
    # make_daily_graph(index)
    
    # Create a two-column layout
    hourly_col, daily_col = st.columns(2)

    # Hourly graph
    with hourly_col:
        st.markdown("<h3 style='margin-bottom:-33px;font-size: 20px;'>Hourly</h3>", unsafe_allow_html=True)
        make_graph(index)

    # Daily graph
    with daily_col:
        st.markdown("<h3 style='margin-bottom:-33px;font-size: 20px;'>Daily</h3>", unsafe_allow_html=True)
        make_daily_graph(index)

# # Monthly box and whisker plots for each building
# st.header("Monthly Box and Whisker Plots")

# # Assuming CW_df and another_df have a common column "Dates"
# merged_df = pd.merge(CW_df, HW_df, on="Dates")

# # Melt the DataFrame for easier plotting
# melted_data = pd.melt(merged_df, id_vars=['Dates'], var_name="Building", value_name="Value")

# # Add a source column to distinguish between the two dataframes
# melted_data['Source'] = melted_data['Building'].apply(lambda x: 'CW_df' if x in CW_df.columns else 'HW_df')

# # Combine 'Building' and 'Source' to create a new column 'Building_Source'
# melted_data['Building_Source'] = melted_data['Building'] + '_' + melted_data['Source']

# # Extract the month from the Dates column
# melted_data['Month'] = melted_data['Dates'].dt.to_period("M").astype(str)

# # Create a box and whisker plot for each building separately
# fig = px.box(melted_data, x="Month", y="Value", color="Building", facet_col="Building_Source",
#              title="Monthly Box and Whisker Plots", facet_col_wrap=1, facet_row_spacing=0.02)
# st.plotly_chart(fig)