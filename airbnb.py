# Importing Necessary Libraries
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import geopandas as gpd
import folium
import plotly.express as px
import matplotlib


# Reading Airbnb Dataset
df_new = pd.read_csv("Airbnb Dataset.csv")


# Mapping using Geopandas and Folium
def geo_mapping(country):    
    df_geo = gpd.GeoDataFrame(df_new, geometry = gpd.points_from_xy(df_new.Longitude, df_new.Latitude))
    map = folium.Map(location = df_geo[df_geo["Country"] == f"{country}"].reset_index().loc[0, ["Latitude", "Longitude"]], zoom_start = 12)
    folium.TileLayer("CartoDB positron", show=False).add_to(map)
    folium.TileLayer("CartoDB dark matter", show=False).add_to(map)

    if st.session_state["type1"] == "All": 
        df_geo[df_geo["Country"] == f"{country}"].explore(m = map,
                                                          color = "blue",
                                                          marker_kwds = dict(radius=4, fill=True),
                                                          tooltip = ["Name", "Street", "Price", "Ratings"],
                                                          popup = ["Min_nights", "Max_nights", "Accommodates", "Amenities"],
                                                          name = "df_all")
                                                          
    if st.session_state["type1"] == "Room_type":
        df_geo[(df_geo["Country"] == country)].explore(m = map,
                                                       column = "Room_type",
                                                       cmap = ["red", "blue", "green"],
                                                       marker_kwds = dict(radius=4, fill=True),
                                                       tooltip = ["Name", "Street", "Price", "Ratings"],
                                                       popup = ["Min_nights", "Max_nights", "Accommodates", "Amenities"],
                                                       name = "Room type",
                                                       legend = True) 
        
    if st.session_state["type1"] == "Property_type":
        df_geo[(df_geo["Country"] == country)].explore(m = map,
                                                       column = "Property_type",
                                                       cmap = list(matplotlib.colors.cnames.keys())[21:57],
                                                       marker_kwds = dict(radius=4, fill=True),
                                                       tooltip = ["Name", "Street", "Price", "Ratings"],
                                                       popup = ["Min_nights", "Max_nights", "Accommodates", "Amenities"],
                                                       name = "Property type",                                                     
                                                       legend = True)
                                                                                                            
    if st.session_state["type1"] == "Bed_type":
        df_geo[(df_geo["Country"] == country)].explore(m = map,
                                                       column = "Bed_type",
                                                       cmap = ["purple", "orange", "brown", "green", "pink" ],
                                                       marker_kwds = dict(radius=4, fill=True),
                                                       tooltip = ["Name", "Street", "Price", "Ratings"],
                                                       popup = ["Min_nights", "Max_nights", "Accommodates", "Amenities"],
                                                       name = "Bed type",                                                   
                                                       legend = True)
                                                      
    folium.LayerControl().add_to(map)
    html = map._repr_html_()
    return st.components.v1.html(html, width = 900, height = 490)


# Top types by Average Price (Property type, Bed type, Room type)
def top_types_by_avg_price(type):
    df_types = df_new.loc[:,[f"{type}", "Price", "Ratings"]][df_new["Country"] == st.session_state["country"]].groupby(f"{type}").mean().sort_values(by = "Price", ascending = False).reset_index()
    
    fig = px.bar(df_types,
                 x = f"{type}",
                 y = "Price",
                 color = "Price",
                 color_continuous_scale = "plasma",
                 hover_name = f"{type}",
                 hover_data = {f"{type}" : False, "Ratings" : True}, 
                 title = f"{type} by Average Price for {st.session_state["country"]}")
    
    fig.update_layout(title_font = {"size": 23, "color": "violet"})
    fig.update_layout(hoverlabel = dict(font = dict(size = 13)))
    fig.update_layout(height = 390)
    return fig


# Top types by Average Ratings (Property type, Bed type, Room type)
def top_types_by_avg_ratings(type):
    df_types = df_new.loc[:,[f"{type}", "Price", "Ratings"]][df_new["Country"] == st.session_state["country"]].groupby(f"{type}").mean().sort_values(by = "Ratings", ascending = False).reset_index()
    
    fig = px.bar(df_types,
                 x = f"{type}",
                 y = "Ratings", 
                 color = "Price", 
                 color_continuous_scale = "plasma",
                 hover_name = f"{type}", 
                 hover_data = {f"{type}" : False, "Price" : True}, 
                 title = f"{type} by Average Ratings for {st.session_state["country"]}")
    
    fig.update_layout(title_font = {"size": 22, "color": "violet"})
    fig.update_layout(hoverlabel = dict(font = dict(size = 13)))
    fig.update_layout(height = 390)
    return fig


# Top 10 Listing for each Country by Different Factors(Price, Ratings, Accommodates, Availability 30days, Availability 60days, availability 90days, Availability 365days)
def top_10_listing(country):
    df_listing = df_new[df_new["Country"] == f"{country}"].sort_values(by = f"{st.session_state["listing"]}", ascending = False).head(10)

    fig = px.bar(df_listing,  
                 x = f"{st.session_state["listing"]}",
                 y = "Name", 
                 color = f"{st.session_state["pr_l"]}",
                 color_continuous_scale = "rainbow", 
                 orientation = "h", 
                 hover_name = "Name", 
                 hover_data = {"Name" : False, "Ratings" : True}, 
                 title = f"Top 10 Listing by {st.session_state["listing"]} - {country}")
    
    fig.update_layout(title_font = {"size": 30, "color": "violet"})  
    fig.update_layout(hoverlabel = dict(font = dict(size = 13)))
    fig.update_layout(yaxis = dict(autorange="reversed"))
    fig.update_layout(height = 390)
    return fig


# Least 10 Listing by Price
def least_10_listing_by_price(country):
    df_listing = df_new.loc[:,["Name", "Price", "Ratings"]][df_new["Country"] == f"{country}"].sort_values(by = "Price", ascending = True).head(10)
    
    fig = px.bar(df_listing,  
                 x = "Price", 
                 y = "Name", 
                 color = "Price", 
                 color_continuous_scale = "rainbow",
                 orientation = "h", 
                 hover_name = "Name", 
                 hover_data = {"Name" : False, "Ratings" : True}, 
                 title = f"Least 10 Listing by Price - {country}")
    
    fig.update_layout(title_font = {"size": 30, "color": "violet"})
    fig.update_layout(hoverlabel = dict(font = dict(size = 13)))
    fig.update_layout(yaxis = dict(autorange="reversed"))
    return fig


# Top 10 Host for each Country by Different Factors(Price, Ratings, Accommodates, Availability 30days, Availability 60days, availability 90days, Availability 365days)
def top_10_host(country):
    df_host = df_new[df_new["Country"] == f"{country}"].sort_values(by = f"{st.session_state["host"]}", ascending = False).head(10)
    
    fig = px.bar(df_host,  
                 x = f"{st.session_state["host"]}", 
                 y = "Host_name", 
                 color = f"{st.session_state["pr_h"]}",
                 color_continuous_scale = "rainbow", 
                 orientation = "h", 
                 hover_name = "Host_name", 
                 hover_data = {"Host_name" : False, "Ratings" : True}, 
                 title = f"Top 10 Host by {st.session_state["host"]} - {country}")
    
    fig.update_layout(title_font = {"size": 30, "color": "violet"})
    fig.update_layout(hoverlabel = dict(font = dict(size = 13)))
    fig.update_layout(yaxis = dict(autorange="reversed"))
    fig.update_layout(height = 390)
    return fig


# Cancellation Policy by Average Price for each Country
def cancellation_policy_by_avg_price(country):    
    df_cp = df_new.loc[:,["Cancellation_policy", "Price", "Ratings"]][df_new["Country"] == f"{country}"].groupby("Cancellation_policy").mean().sort_values(by = "Price", ascending = False).reset_index()
    
    fig = px.pie(df_cp, 
                 names = "Cancellation_policy", 
                 values = "Price", 
                 hover_name = "Cancellation_policy", 
                 hover_data = {"Cancellation_policy" : False}, 
                 title = f"Cancellation Policy by Avg Price for {country}")
    
    fig.update_layout(title_font = {"size": 20, "color": "violet"})
    fig.update_layout(hoverlabel = dict(font = dict(size = 13)))
    fig.update_layout(yaxis = dict(autorange="reversed"))
    return fig


# Cancellation Policy by Average Ratings for each Country
def cancellation_policy_by_avg_ratings(country):
    df_cp = df_new.loc[:,["Cancellation_policy", "Price", "Ratings"]][df_new["Country"] == f"{country}"].groupby("Cancellation_policy").mean().sort_values(by = "Ratings", ascending = False).reset_index()
    
    fig = px.pie(df_cp, 
                 names = "Cancellation_policy", 
                 values = "Ratings", 
                 hover_name = "Cancellation_policy", 
                 hover_data = {"Cancellation_policy" : False}, 
                 title = f"Cancellation Policy by Avg Ratings for {country}")
    
    fig.update_layout(title_font = {"size": 20, "color": "violet"})
    fig.update_layout(hoverlabel = dict(font = dict(size = 13)))
    fig.update_layout(yaxis=dict(autorange="reversed"))
    return fig


# Top Countries by Average Listing Price
def country_by_avg_listing_price():
    df_country = df_new.loc[:,["Country", "Price", "Ratings"]].groupby("Country").mean().sort_values(by = "Price", ascending = False).reset_index()
    
    fig = px.pie(df_country, 
                 names = "Country", 
                 values = "Price", 
                 hover_name = "Country", 
                 hover_data = {"Country" : False}, 
                 title = "Countries by Average Listing Price",
                 hole = 0.5)
    
    fig.update_layout(title_font = {"size": 25, "color": "violet"})
    fig.update_layout(hoverlabel = dict(font = dict(size = 13)))
    fig.update_layout(height = 450)
    return fig


# Top Countries by Average Listing Ratings
def country_by_avg_listing_ratings():
    df_country = df_new.loc[:,["Country", "Price", "Ratings"]].groupby("Country").mean().sort_values(by = "Ratings", ascending = False).reset_index()
    
    fig = px.pie(df_country, 
                 names = "Country", 
                 values = "Ratings", 
                 hover_name = "Country", 
                 hover_data = {"Country" : False}, 
                 title = "Countries by Average Listing Ratings",
                 hole = 0.5)
    
    fig.update_layout(title_font = {"size": 25, "color": "violet"})
    fig.update_layout(hoverlabel = dict(font = dict(size = 13)))
    fig.update_layout(height = 450)
    return fig



# Streamlit Setup
st.set_page_config(page_title = 'Airbnb Analysis By kishore', layout = "wide")


with st.sidebar:
    selected = option_menu(menu_title = None,
                           options = ['Menu', "Airbnb Analysis"],
                           icons = ['house-door-fill', 'pie-chart-fill'],
                           default_index = 0,
                           orientation="horizontal",
                           styles = {"nav-link": {"font-size": "20px", "text-align": "left", "margin": "8px"},
                                   "icon": {"color": "yellow", "font-size": "20px"},
                                   "nav-link-selected": {"background-color": "#9457eb"}})


# Menu Page
if selected == "Menu":
    st.title(":red[**AIRBNB ANALYSIS**]")
    st.markdown('''This project aims to analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, 
                   develop interactive geospatial visualizations, and create dynamic plots to gain insights into pricing variations, 
                   availability patterns, and location-based trends.''')
    st.subheader(":red[ABOUT]")
    st.markdown('''Airbnb is a platform that connects Hosts and guests who want to host anything, anywhere, 
                   and guests who want to enjoy everything, everywhere. It began in 2008 when two designers with 
                   extra space hosted three travelers looking for a place to stay. Airbnb is an American San Francisco-based company 
                   operating an online marketplace for short- and long-term homestays and experiences. The company acts as a broker 
                   and charges a commission from each booking. The company was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia.
                   Airbnb is the most well-known company for short-term housing rentals.''')


# Airbnb Analysis Page
if selected == "Airbnb Analysis":

    x = st.selectbox(":blue[**Country**]", options = df_new["Country"].unique(), key = "country")
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([":blue[**Map**]", ":blue[**Top Types**]", ":blue[**Top Listing**]", 
                                                        ":blue[**Least Listing**]", ":blue[**Top Host**]", 
                                                        ":blue[**Cancellation Policy**]", ":blue[**Top Countries**]"])
    

    with tab1:
        col11,col12 = st.columns(2)
        with col11:
            st.header(f"**:violet[Map for {x}]**")
        with col12:
            st.selectbox(":blue[**Types**]", options = ["All", "Property_type", "Room_type", "Bed_type"], key = "type1")
        geo_mapping(x)
        

    with tab2:  
        y = st.selectbox(":blue[**Types**]", options = ["Property_type", "Room_type", "Bed_type"], key = "type")
        col21,col22 = st.columns(2)
        with col21:
            st.plotly_chart(top_types_by_avg_price(y), use_container_width = True)      
        with col22:
            st.plotly_chart(top_types_by_avg_ratings(y), use_container_width = True)


    with tab3:
        col31,col32 = st.columns(2)
        with col31:
            st.selectbox(":blue[**select**]", options = ["Price", "Ratings", "Accommodates", "Availability_365days", "Availability_90days",      
                                                         "Availability_60days", "Availability_30days"], key = "listing")  
        with col32:
            st.selectbox(":blue[color bar]", options = ["Price", "Ratings"], key = "pr_l")
        st.plotly_chart(top_10_listing(x), use_container_width = True)
        

    with tab4:
        st.plotly_chart(least_10_listing_by_price(x), use_container_width = True)
    

    with tab5:
        col51, col52 = st.columns(2)
        with col51:
            st.selectbox(":blue[**select**]", options = ["Price", "Ratings", "Accommodates","Availability_365days","Availability_90days", 
                                          "Availability_60days", "Availability_30days"], key = "host")
        with col52:
            st.selectbox(":blue[color bar]", options = ["Price", "Ratings"], key = "pr_h")
        st.plotly_chart(top_10_host(x), use_container_width = True)


    with tab6:
        col61,col62 = st.columns(2)
        with col61:
            st.plotly_chart(cancellation_policy_by_avg_price(x), use_container_width = True)
        with col62:
            st.plotly_chart(cancellation_policy_by_avg_ratings(x), use_container_width = True)


    with tab7:
        col71,col72 = st.columns(2)
        with col71:
             st.plotly_chart(country_by_avg_listing_price(), use_container_width = True)
        with col72:
             st.plotly_chart(country_by_avg_listing_ratings(), use_container_width = True)



# -----------------------x------------------------x-------------------------x-------------------------x---------------------x--------------------x--------------------------------