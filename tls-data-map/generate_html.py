# -*- coding: utf-8 -*-
"""
@author: Matheus Boni Vicari (matheus.boni.vicari@gmail.com)
"""

import os
import folium
import pandas as pd
from folium.plugins import MarkerCluster
from StringIO import StringIO
import requests


def scrap_gsheet(gsheet_key):

    """
    Function to scrap data from a Google spreadsheet.

    Parameters
    ----------
    gsheet_key: str
        Spreadsheet key from Google Sheet service.

    Returns
    -------
    df: pandas.DataFrame
        Information from Google spreadsheet.

    """

    # Creating request from spreadsheet link. Outputs spreadsheet in csv
    # data format.
    r = requests.get('https://docs.google.com/spreadsheet/ccc?key=%s&\
output=csv' % gsheet_key)

    # Converting spreadsheet content 'r.content' into a pandas.DataFrame.
    df = pd.read_csv(StringIO(r.content))

    return df


def generate_map(df):

    """
    Function to generate .html of a leafletjs map containing data from a
    pandas.DataFrame.

    Parameters
    ----------
    df: pandas.DataFrame
        Dataframe with information to map

    """

    # Generating a standard leafletjs map.
    m = folium.Map([0, 0], zoom_start=2)

    # Initializing marker_cluster instance to cluster markers that are too
    # close.
    marker_cluster = MarkerCluster().add_to(m)

    # Looping over rows in df.
    for index, row in df.iterrows():
        # Converting 'row' to a DataFrame. This step seems redundant, but
        # necessary as variable 'row' has type pandas.Series.
        df = pd.DataFrame(row)

        # Generating html code from 'df'.
        html = df.to_html()

        # Generating popup of information in 'html'
        popup = folium.Popup(html)

        # Adding marker to map using latitude ('SITE_LAT') and longitude
        # ('SITE_LONG') information to set location and 'popup' as popup
        # (on-click) information.
        folium.Marker([row['SITE_LAT'], row['SITE_LONG']],
                      popup=popup).add_to(marker_cluster)

    # Saving html file 'plot_sites.html' into folder '../html'.
    m.save(os.path.join('../html', 'plot_sites.html'))





if __name__ == "__main__":

    # Example gsheet_key to test code.
    gsheet_key = '1V9zpygdkf26GWpmLzfnyB_xDYWvBkNMqG_Dh74xIDuo'
    # Scraping data into df.
    df = scrap_gsheet(gsheet_key)
    # Generating map.
    generate_map(df)
