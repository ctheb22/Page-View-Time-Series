import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=[0], index_col='date')

# Clean data
df = df.loc[(df['value'] >= df['value'].quantile(.025)) & (df['value'] <= df['value'].quantile(.975))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots()
    fig.set_size_inches(15, 5)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.plot(df.index, df['value'], 'r-')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    dfbp = df.copy()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    dfbp['month'] = dfbp.index.month
    dfbp['month'] = dfbp['month'].apply(lambda x: months[x - 1])
    dfbp['month'] = pd.Categorical(dfbp['month'], categories=months)
    dfbp['year'] = dfbp.index.year

    # Copy and modify data for monthly bar plot
    df_bar = pd.pivot_table(data=dfbp, values='value', index='year', columns='month', aggfunc='mean')

    ax = df_bar.plot(kind='bar')
    fig = ax.get_figure()
    fig.set_size_inches(10, 5)

    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    plt.legend()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axs = plt.subplots(1,2)
    ax1 = axs[0]
    ax2 = axs[1]
    fig.set_size_inches(15,7)

    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    sns.boxplot(ax=ax1, data=df_box, x='year', y='value')
    sns.boxplot(ax=ax2, data=df_box, x='month', y='value',
                order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig