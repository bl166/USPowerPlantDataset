'''
This script generates a brief pie chart report of the dataset based on the metadata.
It plots the distribution of power plants by their general fuel types.

Author: Boning Li
Email: boning.li@duke.edu

Developed for Duke Data+ 2017: Electricity Access
Aug 03, 2017
'''


import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import operator
import json

# not showing the percentage if it is no larger than 1%
def my_autopct(pct):
    return ('%.1f%%' % pct) if pct > 1 else ''

# plot pie chart
def pieplot(t_dict):
    # non repeating color scheme
    color = sns.color_palette("husl", len(t_dict))

    # labels and values
    labs = t_dict.keys()
    vals = list(t_dict.values())

    # figure and plot
    f = plt.figure()
    ax = f.add_subplot(111,aspect=1)
    plt.pie(vals,labels=labs,autopct=my_autopct,colors=color)

    # title and legend
    ax.set_title('U.S. Power Plants Categoried by Fuel')
    ax.legend(bbox_to_anchor=(0,0.5))

    plt.show()

# data report
def report():
    with open('uspp_metadata.geojson','r') as f:
        values = json.load(f)['features']
    g_type = np.array([item['properties']['fossil_fuel'] if item['properties']['fossil_fuel'] else 'UNKNOWN' for item in values]) # general fuel type
    g_categories = np.unique(g_type)

    # create type dictionary
    t_dict = {}
    for cat in g_categories:
        t_dict[cat] = np.sum(g_type==cat)
    t_dict_s = sorted(t_dict.items(), key=operator.itemgetter(1), reverse=True)
    t_dict = dict(t_dict_s)
    print(t_dict)

    pieplot(t_dict)


if __name__ == '__main__':
    try:
        report()
    except:
        print('Error! Please check the metadata')
