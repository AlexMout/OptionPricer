import plotly as plt
import plotly.graph_objs as go
from plotly import tools
import numpy as np

class Plotter:
    @staticmethod
    def get_payoff_lists(list_payoff,K,R,T,Vol,oneDay,list_title,list_price):
        X = Plotter.__get_strike_list(K)
        Y_list = []
        for payoff, price in zip(list_payoff, list_price):
            Y = list(map(lambda x: payoff(x, K, R, T, Vol) - price, X))
            Y_maturity = list(map(lambda x: payoff(x, K, R, oneDay, Vol) - price, X))

            Y_list.append(Y)
            Y_list.append(Y_maturity)
        return (X,Y_list,list_title)

    @staticmethod
    def get_payoff_strategy(list_payoff,list_of_listparameters,list_title,list_price,middle_strike):
        X = Plotter.__get_strike_list(middle_strike)

        list_Y = []
        for payoff, list_parameters, price in zip(list_payoff, list_of_listparameters, list_price):
            Y = list(map(lambda x: payoff(x, *list_parameters) - price, X))
            list_Y.append(Y)

        return (X,list_Y,list_title)

    @staticmethod
    def get_graph_greeks(list_greeks_functions, K, R, T, Vol,oneDay, list_title):
        X = Plotter.__get_strike_list(K)

        list_Y = []
        for greek in list_greeks_functions:
            Y = list(map(lambda x: greek(x, K, R, T, Vol), X))
            Y_maturity = list(map(lambda x: greek(x, K, R, oneDay, Vol), X))

            list_Y.append(Y)
            list_Y.append(Y_maturity)

        return (X,list_Y,list_title)

    @staticmethod
    def get_graph_strategy_greeks(list_greeks_functions, list_of_listparameters, list_title, middle_strike):
        X = Plotter.__get_strike_list(middle_strike)

        list_Y = []
        count = 0
        for greek in list_greeks_functions:
            Y = list(map(lambda x: greek(x, *list_of_listparameters[count]), X))
            count+=1
            Y_maturity = list(map(lambda x: greek(x, *list_of_listparameters[count]), X))
            list_Y.append(Y)
            list_Y.append(Y_maturity)
            count = count + 1 if count==1 else 0
        return (X,list_Y,list_title)

    @staticmethod
    def get_graph_strategy_greeks_one_leg(list_greeks_functions, list_parameters, list_title, middle_strike):
        X = Plotter.__get_strike_list(middle_strike)

        list_Y = []
        for greek in list_greeks_functions:
            Y = list(map(lambda x: greek(x, *list_parameters[0]), X))
            Y_maturity = list(map(lambda x: greek(x, *list_parameters[1]), X))
            list_Y.append(Y)
            list_Y.append(Y_maturity)

        return (X,list_Y,list_title)

    @staticmethod
    def __get_strike_list(K):
        return list(np.linspace(K*0.7,K*1.3,100))
