#############################
# Dashborad for data visualization using streamlit
# Author: Ricardo Barbosa de Almeida Campos
#############################

## Required Libraries
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import MarkerCluster
import geopandas
import plotly.express as px
import math


## Page Configuration


def dashboard_initialization():
    st.set_page_config(layout='wide')
    st.title("AirBnb New York City House Marketing Analysis")
    st.markdown("Dashboard for data visualization regarding AirBnb in the city of New York")

    st.header("Data Overview")
    st.markdown("General Data Visualization")

    return None


## Function description
def load_transform_data(url):
    df = pd.read_csv(url)

    # Drop both 'last_review', 'reviews_per_month' because it has a lot of missing values
    df.drop(columns=['last_review', 'reviews_per_month'], inplace=True)

    return df


def statistical_filter_creation(df):
    # All the widgets will be created according the Streamlit documentation
    # To designate a widget to the sidebar the st.sidebar prefix must be used before the widget name

    # Filter responsible for selecting which columns will be selected in the 'Ordered Values' table
    variable_filter = st.sidebar.multiselect("Variable Selection", df.columns,
                                             default=None)
    # Select which variable wil sorted in the 'Ordered Values' table
    ordering_filter = st.sidebar.multiselect("Ordering Selection", df.columns,
                                             default=None)

    # Select if the ordering tin the previous table will be 'Ascending' or 'Descending'
    ordering_sequence = st.sidebar.radio("Ordering", ('Ascending', 'Descending'))

    # Select the Features that will be reference when aggregating the data on both `Aggregated Values` and the last
    # table
    feature_agg_filter = st.sidebar.multiselect("Feature Aggregation Selection",
                                                ['room_type', 'neighbourhood_group', 'host_id', 'neighbourhood'],
                                                default='room_type')

    return  variable_filter, ordering_filter, ordering_sequence, feature_agg_filter


def feature_filter_creation(df):
    st.sidebar.title("Feature Options")

    # Create the filter that will select the Feature that will be used in the Counting Number of Selected Feature plot
    feature_filter = st.sidebar.selectbox('Feature', ['room_type', 'neighbourhood', 'neighbourhood_group'])

    # Create a filter that will select the type aggregation used in the last plot. If it will be
    # average, maximum or minimum
    aggregate_analysis_filter = st.sidebar.radio("Type of Aggregate Analysis", ('Maximum', 'Minimum', 'Average'))

    return feature_filter, aggregate_analysis_filter


@st.cache(allow_output_mutation=True)
def data_filtering(df, variable_filter):

    if (variable_filter != []):

        filtered_df = df.loc[:, variable_filter]

    else:
        filtered_df = df.copy()

    return filtered_df


def ordering_dataframe(df, ordering_filter, ordering_sequence_filter):
    # First, checks if the variable selected to be sorted is inside the current dataframe.
    # If not, nothing will be performed. If is inside, check if the sorting order is
    # ascending or descending and the sort the dataframe,

    if (df.columns.isin(ordering_filter).sum()):

        ordering_variable = df.columns[df.columns.isin(ordering_filter)][0]

        if (ordering_sequence_filter == 'Ascending'):

            #ordered_df = df.rename_axis('MyIdx').sort_values(by=['number_of_reviews', 'MyIdx'], ascending=[True, True])
            ordered_df = df.sort_values(by=ordering_variable, ascending=True)

        else:

            ordered_df = df.sort_values(by=ordering_variable, ascending=False)

    else:

        ordered_df = df.copy()

    return ordered_df


def data_feature(df):
    # The column profitability will be generated according the formula presented inside the lambda function. If
    # 'availability_365' equals zero, the following cell will be set with a None value.
    df['profitability'] = df.apply(
        lambda x: (x['price'] * ((x['minimum_nights']+1) * (x['number_of_reviews']))) / (math.sqrt(x['availability_365']))
        if (x['availability_365'] != 0) else None, axis=1)

    # The column return_investment will be generated according the formula presented inside the lambda function. If
    # 'price' equals zero, the following cell will be set with a None value.
    df['return_investment'] = df.apply(
        lambda x: 1000000 / (x['price'] * (x['minimum_nights'] + 1)) if x['price'] != 0
        else None, axis=1)

    # Convert the id and host_id columns to string, since they are categorical values
    df[['id', 'host_id']] = df[['id', 'host_id']].astype(str)

    return None


def statiscal_analysis_tables(data, agg_df, ordered_df):
    c1, c2 = st.columns((1, 1))

    c1.title('Aggregated Values')
    c1.dataframe(agg_df, width=5000, height=600)

    c2.title('Ordered Values')
    c2.dataframe(ordered_df, width=1200, height=600)

    # Inject CSS with Markdown
    st.title('Data Description')
    st.dataframe(data.describe().T, width=1200)

    return None


def portifolio_density_map(df):
    #  Create a folium map with the initial point being the average value for latitude and longitude
    m1 = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], width="%100", height="%100")
    # Create a folium cluster object
    mCluster = MarkerCluster(name="house density").add_to(m1)

    # iterate the dataframe to all the locations in the cluster marker object
    # Only price will be shown in the marker
    for index, row in df.iterrows():
        folium.Marker(location=[row['latitude'], row['longitude']],
                      popup="U${0}.".format(
                          row['price'])).add_to(
            mCluster)

    # Add the cluster object to the folium map
    folium.LayerControl().add_to(m1)

    # Plot the map using a method designed to plot folium maps in the streamlit plataform
    st.data = st_folium(m1, key='fig1', width=2000)


def print_density_maps(df, sample_number):
    # Sample the number os points specified in the sample_number variable
    # since the database is too large and will take a lot of time to load
    df = df.sample(n=sample_number, random_state=1)

    st.title('Portfolio Density')
    portifolio_density_map(df)

    return None


def feature_counting(df, feature_filter):

    st.title("Features Counting Plot")
    # Select only the variables to be ploted
    feat_df = df.loc[:, feature_filter]
    st.header('Counting Number of Selected Feature')
    # Use the plotly express library to plot the histogram of the selected data
    # The plot will de ordered from the highest count to the lowest
    fig_3 = px.histogram(feat_df, x=feature_filter).update_xaxes(categoryorder="total descending")
    # Use the streamlit method for ploty plot and set for the whole vertical space
    st.plotly_chart(fig_3, use_container_width=True)

    return None


def data_aggregaton(df, feature_selection, ordering_sequence_filter):
    # Create a empty dataframe
    agg_df = pd.DataFrame()

    # If variable to perform the aggregation is 'host_id', only perform the count of the variable
    # and then sort the value according the Ordering widget.

    if feature_selection == ['host_id']:

        if ordering_sequence_filter == 'Descending':

            agg_df = df[feature_selection].value_counts(ascending=False)

        else:
            agg_df = df[feature_selection].value_counts(ascending=True)

    # If the feature selection variable is not empty aggregate the function on the selected
    # variables. If it is empty, aggregate according the 'room_type', 'neighbourhood_group', 'host_id'
    # features.
    elif feature_selection != []:

        agg_df = df.groupby(feature_selection).size().reset_index()

        # Rename the column to count
        agg_df.rename(columns={0: 'Count'}, inplace=True)

    else:

        agg_df = df.groupby(['room_type', 'neighbourhood_group', 'host_id']).size().reset_index()

        # Rename the column to count
        agg_df.rename(columns={0: 'Count'}, inplace=True)



    return agg_df


def price_feature_distribution(df, feature_filter, aggregate_analysis):

    # Select only the columns to be aggregated
    selected_df = df[['price', 'minimum_nights', 'number_of_reviews', 'neighbourhood_group',
                      'calculated_host_listings_count', 'availability_365', 'room_type', 'neighbourhood','host_id', 'profitability', 'return_investment']]

    # if the filter is not empty, aggregate on the selected columns. If empty, only aggregate on
    # 'neighbourhood_group' and 'neighbourhood' columns.
    if (feature_filter != []):

        # Based on the aggregate_analysis variable, select if the aggregation will use the
        # maximum, minimum or average values.
        if aggregate_analysis == 'Maximum':

            aggregated_df = selected_df.groupby(feature_filter).max().reset_index()

        elif aggregate_analysis == 'Minimum':

            aggregated_df = selected_df.groupby(feature_filter).min().reset_index()

        else:

            aggregated_df = selected_df.groupby(feature_filter).mean().reset_index()

    else:

        if aggregate_analysis == 'Maximum':

            aggregated_df = selected_df.groupby(['neighbourhood_group', 'neighbourhood']).max().reset_index()

        elif aggregate_analysis == 'Minimum':

            aggregated_df = selected_df.groupby(['neighbourhood_group', 'neighbourhood']).min().reset_index()

        else:

            aggregated_df = selected_df.groupby(['neighbourhood_group', 'neighbourhood']).mean().reset_index()

    st.dataframe(aggregated_df)

    return None


def available_selection(df, available_selection):
    # Depending on the available_selection variable, the available listings will be selected or not.
    if available_selection == 'Yes':

        # If the listing is unavailable, the 'availability_365' variable will set to 0.
        available_df = df.loc[df['availability_365'] != 0, :]

    else:

        available_df = df.copy()

    # Perform the data feature step and create new columns
    data_feature(available_df)
    # Print the dataframe for checking
    st.dataframe(available_df)
    st.write(available_df.shape)

    return available_df

def create_available_filter():

    st.sidebar.title("Filtering Options")

    # Filter responsible for selecting the rooms which are not available
    available_filter = st.sidebar.radio("Only Select Available Listings", ('Yes', 'No'))

    return available_filter

# Main Code
if __name__ == "__main__":
    # This function is responsible to print the first lines in  the webpage and set page format configuration to wyde
    dashboard_initialization()

    # Load the CSV file containing the data and drop the columns that will not be used in this project
    data_frame = load_transform_data(r"AB_NYC_2019.csv")
    available_filter = create_available_filter()
    # Function that returns the dataframe including or not only the available listings
    available_df = available_selection(data_frame, available_filter)

    # Create the filters that will be used to filter the Data Overview, Aggregated Values, Ordered Values
    # and Data Description table. The interactive widgets will be located in the left.
    variable_filter, ordering_filter, ordering_sequence_filter, feature_selection = statistical_filter_creation(
        available_df)
    # Create the feature filters for the Counting Number of Selected Feature plot and the following table
    feature_filter, aggregate_analysis_filter = feature_filter_creation(available_df)


    # Function that returns the filtered dataframe according the variable selection filter
    filtered_df = data_filtering(available_df, variable_filter)
    # Returns the ordered the dataframe that will be shown in the Ordered Values table
    df_ordered = ordering_dataframe(filtered_df, ordering_filter, ordering_sequence_filter)
    # Returns the aggregated dataframe according the Feature Aggregation Selection and
    # ordering widget
    agg_df = data_aggregaton(available_df, feature_selection, ordering_sequence_filter)

    # Print the 'Aggregated Values', 'Ordered Values', 'Data Description' tables
    statiscal_analysis_tables(available_df, agg_df, df_ordered)
    # Plot the density map
    print_density_maps(available_df, 500)
    # Print the  distribution plot for the selected feature variables
    feature_counting(available_df, feature_filter)
    # Aggregate for the numerical variables and print the table
    price_feature_distribution(available_df, feature_selection, aggregate_analysis_filter)
