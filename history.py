import csv
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter, DayLocator
from matplotlib.ticker import FormatStrFormatter


def write_amount(path, amount):
    with open(path, "a") as ofile:
        writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow((datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), amount))


def get_graph(path):
    list = []
    with open(path) as ifile:
        reader = csv.reader(ifile)
        for row in reader:
            if len(row) == 2:
                t = tuple([datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S"), row[1]])
                list.append(t)
        print(list)
        years = YearLocator()  # every year
        months = MonthLocator()  # every month
        days = DayLocator()
        yFormatter = FormatStrFormatter('%d')
        yearsFmt = DateFormatter('%d-%m-%Y')
        dates = [(i[0]) for i in list]
        values = [(int(i[1])) for i in list]
        fig, ax = plt.subplots()
        ax.plot_date(dates, values, '-')

        # format the ticks
        # ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(yearsFmt)
        ax.xaxis.set_minor_locator(days)
        ax.autoscale_view()

        ax.yaxis.set_major_formatter(yFormatter)

        ax.fmt_xdata = DateFormatter('%Y-%m-%d')

        # tidy up the figure
        ax.grid(True)
        ax.legend(loc='right')
        ax.set_title('Number of Pocket items')
        ax.set_xlabel('Date')
        ax.set_ylabel('Articles')

        plt.savefig('img.png')
        return "img.png"
