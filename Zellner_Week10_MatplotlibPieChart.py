"""
**********************************************************************
Description: This program imports stock values in a portfolio from a JSON
file. Different date lists are created to associate with the stock prices.
A pie chart is created for the stock performance. The chart
is then saved as a .png file to view by the user.

Author: Katie Zellner
Last Revision: 3/14/2019
**********************************************************************
"""

# imports
import json
import pygal
from matplotlib.dates import date2num
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime
from random import randint


#create class Stock
class Stock(object):

    def __init__(self, investor_id, name, open_val, high, low, close, date_string, volume):
        self.investor_id = investor_id
        self.name = name
        self.open = open_val
        self.high = high
        self.low = low
        self.close = close
        self.date = datetime.strptime(date_string, '%d-%b-%y').date()
        self.volume = volume
        self.stock_performance_list = []
        self.stock_date_list = []

    def add_stock_performance(self, close_val, purchase_date):
        self.stock_date_list.append(purchase_date)
        self.stock_performance_list.append(close_val)


#Create class investor
class Investor(object):

    stock_dict = dict()

    def __init__(self, name):
        self.investor_id = randint(1, 10000000)
        self.name = name

    def read_stocks_from_file(self, file_name):
        with open(file_name) as f:
            data_set = json.load(f)
            for row in data_set:
                name = row["Symbol"]
                date_string = row["Date"]
                open_val = row["Open"]
                high = row["High"]
                low = row["Low"]
                close = float(row["Close"])
                volume = row["Volume"]

                stock = Stock(self.investor_id, name, open_val, high, low, close, date_string, volume)

                if name not in self.stock_dict:
                    self.stock_dict[name] = {'stock': stock}

                self.stock_dict[name]['stock'].add_stock_performance(stock.close, stock.date)

    def graph_data(self):
        matplot_file_name = "{}_portfolio_chart.png".format(self.name.replace(" ", "_"))

       
        for stock_name in self.stock_dict:
            stock = self.stock_dict[stock_name]['stock']
            stock_performance = stock.stock_performance_list
            dates = date2num(stock.stock_date_list)
            name = stock.name
			
			
			#create list of colors
			colors = ["#E13F29", "#D69A80", "#D63B59", "#AE5552", "#CB5C3B", "#EB8076", "#96624E", "#D67B58"]
			#create pie chart
            plt.pie(stock_performance, labels=stock, shadow=false, colors=colors, explode=(0,0,0,0,0,0,0,0.15), startangle=90, autopct='%1.1f%%',)
            plt.axis('equal')
            
            

        plt.legend()
        plt.savefig(matplot_file_name)
        
        #print graph creation success messages
        print("Successfully wrote pie chart to PNG file: {0}".format(matplot_file_name))
  


if __name__ == "__main__":
    # Input Section
    user_name = input("Enter your name:")

    stock_file_name = 'AllStocks.json'

    #read stocks from file
    investor = Investor(user_name)
    try:
        investor.read_stocks_from_file(stock_file_name)
    except IOError:
        print("Investment holdings could not be read from file!")

    try:
        investor.graph_data()
    except Exception as e:
        print(e)
