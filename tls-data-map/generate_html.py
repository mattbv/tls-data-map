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


def create_html(base_file, df):

    base = gen_html_base(base_file)
    script = gen_html_script(df)

    html = base + script + u'\n\n</script>'

    # Saving html file 'plot_sites.html' into folder '../html'.
    with open(os.path.join('../docs', 'index.html'), 'w') as f:
        f.write(html)


def gen_html_base(base_file):

    with open(base_file, 'r') as f:
        base = f.read()

    return base


def gen_html_script(df):

    map_str = gen_map_str(0, 0, 2)
    clusters_str = gen_clusters_str(df, 'Year')

    return map_str + clusters_str


def gen_map_str(Lat, Long, zoom, minZoom=2, maxZoom=18):

    html_str = (u"""\tvar tiles = L.tileLayer('http://{s}.tile.osm.org\
/{z}/{x}/{y}.png',\n\t\t\t{maxZoom: %s,\n\tminZoom:%s,\n\t\t\tattribution: \
'&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors, \
Points &copy 2012 LINZ'\n\t\t}),\n\t\tlatlng = L.latLng(%s, %s);\n\n\tvar \
map = L.map('map', {center: latlng, zoom: %s, layers: [tiles]});\n\n"""
                % (maxZoom, minZoom, Lat, Long, zoom))

    return html_str


def gen_marker_str(m, g, Lat, Long, title):

    html_str = (u"""\tmarker%s = L.marker([%s, %s], { title: '%s'});\
                \n\tmarker%s.addTo(group%s);\n""" %
                (m, Lat, Long, title, m, g))

    return html_str


def gen_clusters_str(df, var):

    groups = df.groupby(var)

    html_str = u"""\tvar mcg = L.markerClusterGroup(),\n"""

    for y, d in groups:
        html_str += (u"""\t\tgroup%s = L.featureGroup.subGroup(mcg),\n""" %
                     y)

    html_str += (u"""\t\tcontrol = L.control.layers(null, null,\
{ collapsed: false }),\n\t\ti, a, title, marker;\n\n\tmcg.addTo(map);\n\n""")

    for y, d in groups:
        for index, row in d.iterrows():
            row_df = pd.DataFrame(row)
            marker_html = gen_marker_str(index, y, row['long'],
                                         row['lat'], row['Location'])
            html_str += marker_html
            html_str += gen_popup_str(index, row_df)

    html_str += '\n'

    for y, d in groups:
        html_str += gen_Overlay_str(y)

    html_str += u'\n\tcontrol.addTo(map);\n\n'

    for y, d in groups:
        html_str += gen_addTomap_str(y)

    return html_str


def gen_Overlay_str(g):
    return (u"""\tcontrol.addOverlay(group%s, '%s');\n""" % (g, g))


def gen_addTomap_str(g):
    return (u"""\tgroup%s.addTo(map)\n""" % g)


def gen_popup_str(index, df, maxWidth=300):

    index = str(index)

    html_table = df.to_html()
    html_table = "".join(html_table.splitlines())

    pop_html = (u"\tvar popup%s = L.popup({maxWidth: '%s'});\n\t\tvar html%s \
= $('<div id=""html%s"" style=""width: 100.0%%; height: 100.0%%;"">%s\
</div>')[0];\n\t\tpopup%s.setContent(html%s);\n\tmarker%s.bindPopup\
(popup%s);\n\n" % (index, maxWidth, index, index, html_table, index, index,
                   index, index))

    return pop_html


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
        folium.Marker([row['long'], row['lat']],
                      popup=popup).add_to(marker_cluster)

    # Saving html file 'plot_sites.html' into folder '../html'.
    m.save(os.path.join('../docs', 'index.html'))


if __name__ == "__main__":

    # Example gsheet_key to test code.
    gsheet_key = '1igSlhqWOov5NUL8UTCuq9k5weeDH1Grc7ChnWvibyCk'
    # Scraping data into df.
    df = scrap_gsheet(gsheet_key)
    # Generating map.
    base_file = '../html/base.html'

    # Generating map.
    create_html(base_file, df)
