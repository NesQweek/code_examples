import pandas as pd

def supports_params(df, strong_support, other_supports):

    colors_list_h = []
    linewidths_list_h = []
    hlines = []

    for freq in df['Frequency']:

        for close_ in df[df['Frequency'] == freq]['Close'].values:

            if freq in strong_support:
                colors_list_h.append('red')
                hlines.append(close_)
                linewidths_list_h.append(2)

            # elif freq in other_supports:
            #     colors_list_h.append('orange')
            #     hlines.append(close_)
            #     linewidths_list_h.append(0.1)
            else: pass

    unique_values = {}
    for i in range(len(hlines)):
        if hlines[i] not in unique_values:
            unique_values[hlines[i]] = (colors_list_h[i], linewidths_list_h[i])

    # Преобразуем словарь обратно в списки
    hlines = list(unique_values.keys())
    colors_list_h = [unique_values[value][0] for value in hlines]
    linewidths_list_h = [unique_values[value][1] for value in hlines]

    assert len(colors_list_h)==len(hlines), 'Разный размер списков'

    return colors_list_h, linewidths_list_h, hlines


def indicators_params(df, strong_support, other_supports, alert_date):

    colors_list_v = []
    linewidths_list_v = []
    vlines = []


    for index, row in df.iterrows():
        if row['pattern'] == 1:

            vlines.append(row.name)
            colors_list_v.append('green')
            linewidths_list_v.append(0.1)

    unique_values = {}
    for i in range(len(vlines)):
        if vlines[i] not in unique_values:
            unique_values[vlines[i]] = (colors_list_v[i], linewidths_list_v[i])

    # Преобразуем словарь обратно в списки
    vlines = list(unique_values.keys())
    colors_list_v = [unique_values[value][0] for value in vlines]
    linewidths_list_v = [unique_values[value][1] for value in vlines]

    if alert_date is not None: # debug
        vlines.append(alert_date)
        colors_list_v.append('orange')
        linewidths_list_v.append(5)

    assert len(colors_list_v)==len(vlines), 'Разный размер списков'

    return colors_list_v, linewidths_list_v, vlines


def my_alerts_params(strong_conditions, medium_conditions, strong_support, other_supports, alert_date):

    colors_list_v = []
    linewidths_list_v = []
    vlines = []


    for index, row in strong_conditions.iterrows():

        vlines.append(row.name)
        colors_list_v.append('green')
        linewidths_list_v.append(3)


    for index, row in medium_conditions.iterrows():

        vlines.append(row.name)
        colors_list_v.append('#00FF7F')
        linewidths_list_v.append(2)


    vlines.append(alert_date)
    colors_list_v.append('orange')
    linewidths_list_v.append(5)

    assert len(colors_list_v)==len(vlines), 'Разный размер списков'

    return colors_list_v, linewidths_list_v, vlines



def get_style():
    binance_dark = {
        "base_mpl_style": "dark_background",
        "marketcolors": {
            "candle": {"up": "#3dc985", "down": "#ef4f60"},  
            "edge": {"up": "#3dc985", "down": "#ef4f60"},  
            "wick": {"up": "#3dc985", "down": "#ef4f60"},  
            "ohlc": {"up": "green", "down": "red"},
            "volume": {"up": "#247252", "down": "#82333f"},  
            "vcedge": {"up": "green", "down": "red"},  
            "vcdopcod": False,
            "alpha": 1,
        },
        "mavcolors": ("#ad7739", "#a63ab2", "#62b8ba"),
        "facecolor": "#1b1f24",
        "gridcolor": "#2c2e31",
        "gridstyle": "--",
        "y_on_right": True,
        "rc": {
            "axes.grid": True,
            "axes.grid.axis": "y",
            "axes.edgecolor": "#474d56",
            "axes.titlecolor": "red",
            "figure.facecolor": "#161a1e",
            "figure.titlesize": "x-large",
            "figure.titleweight": "semibold",
        },
        "base_mpf_style": "binance-dark",
    }

    return binance_dark