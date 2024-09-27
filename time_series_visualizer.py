import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
from matplotlib.ticker import FuncFormatter
register_matplotlib_converters()

df = pd.read_csv('fcc-forum-pageviews.csv')
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

corte_cima = df['value'].quantile(0.975)
top_cima = df[df['value'] >= corte_cima]

corte_baixo = df['value'].quantile(0.025)
top_baixo = df[df['value'] <= corte_baixo]

df_top= pd.concat([top_baixo, top_cima])

remover = df_top.index
df = df.drop(remover, axis=0)

def draw_line_plot():

    def cem_mil(x, pos):
        return f'{x * 1e0:.0f}'
    
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['value'])
    plt.gca().yaxis.set_major_formatter(FuncFormatter(cem_mil))
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')

    fig = plt.gcf()
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    
    df_bar = df.copy()

    def cem_mil(Y, pos):
      return f'{Y * 1e0:.0f}'
    
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    df_agrupado= df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    meses = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_agrupado= df_agrupado[meses]

    df_agrupado.plot(kind='bar', figsize=(10, 5))
    plt.title('Average Page Views per Month')
    plt.gca().yaxis.set_major_formatter(FuncFormatter(cem_mil))
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')
    
    fig = plt.gcf()
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box['date']]
    df_box['month'] = [d.strftime('%b') for d in df_box['date']]
    df_box['value'] = df_box['value'].astype(float)

    
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    df_box['month'] = pd.Categorical(df_box['month'], categories=month_order, ordered=True)

    fig, ax = plt.subplots(1, 2, figsize=(20, 8))

    sns.boxplot(
        data=df_box,
        x="year",
        y="value",
        ax=ax[0]
    )
    ax[0].set_title("Year-wise Box Plot (Trend)")
    ax[0].set_xlabel("Year")
    ax[0].set_ylabel("Page Views")

    sns.boxplot(
        data=df_box,
        x="month",
        y="value",
        ax=ax[1]
    )
    ax[1].set_title("Month-wise Box Plot (Seasonality)")
    ax[1].set_xlabel("Month")
    ax[1].set_ylabel("Page Views")

    fig.savefig('box_plot.png')
    return fig