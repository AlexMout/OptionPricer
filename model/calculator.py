from model import graph_generator
from scipy.stats import norm
import math

class BlackScholes:
    __oneDay = 1/365
    # *********************** D1 & D2 **********************
    @classmethod
    def __d1(cls,S,K,R,T,Vol):
        """Class method so that the method has the access to the other methods inside the class without being forced
            to call BlackScholes.My_function() but with cls.My_function()"""
        return (math.log(S/K)+(R+(Vol**2)/2)*T)/(Vol*math.sqrt(T))

    @classmethod
    def __d2(cls,S,K,R,T,Vol):
        return cls.__d1(S,K,R,T,Vol)-Vol*math.sqrt(T)

    # *********************** PRICE FORMULAS **********************
    @classmethod
    def call_price(cls,S,K,R,T,Vol):
        """Return the price of a vanilla call"""
        price = S*norm.cdf(cls.__d1(S,K,R,T,Vol))-K*math.exp(-R*T)*norm.cdf(cls.__d2(S,K,R,T,Vol))
        return round(price,3)

    @classmethod
    def call_spread_price(cls,S,K1,K2,R,T,Vol,isbull):
        if isbull:
            return cls.call_price(S,K1,R,T,Vol)-cls.call_price(S,K2,R,T,Vol)
        return -cls.call_price(S, K1, R, T, Vol) + cls.call_price(S, K2, R, T, Vol)

    @classmethod
    def put_spread_price(cls,S,K1,K2,R,T,Vol,isbull):
        if isbull:
            return -cls.put_price(S,K2,R,T,Vol)+cls.put_price(S,K1,R,T,Vol)
        return cls.put_price(S,K2,R,T,Vol)-cls.put_price(S,K1,R,T,Vol)

    @classmethod
    def put_price(cls,S,K,R,T,Vol):
        """Return the price of a vanilla put"""
        price = -S*norm.cdf(-cls.__d1(S,K,R,T,Vol))+K*math.exp(-R*T)*norm.cdf(-cls.__d2(S,K,R,T,Vol))
        return round(price,3)

    @classmethod
    def call_digital_price(cls,S,K,R,T,Vol):
        return round(math.exp(-R*T)*norm.cdf(cls.__d2(S,K,R,T,Vol)),3)

    @classmethod
    def put_digital_price(cls,S,K,R,T,Vol):
        return round(math.exp(-R*T)*norm.cdf(-cls.__d2(S,K,R,T,Vol)),3)

    @classmethod
    def straddle_price(cls,S,K,R,T,Vol):
        return cls.call_price(S,K,R,T,Vol)+cls.put_price(S,K,R,T,Vol)

    @classmethod
    def strangle_price(cls,S,K1,K2,R,T,Vol):
        return cls.put_price(S,K1,R,T,Vol)+cls.call_price(S,K2,R,T,Vol)

    @classmethod
    def risk_rev_price(cls,S,K1,K2,R,T,Vol):
        return -cls.put_price(S,K1,R,T,Vol)+cls.call_price(S,K2,R,T,Vol)

    @classmethod
    def calendar_price(cls,S,K,R,T1,T2,Vol):
        return -cls.call_price(S,K,R,T1,Vol)+cls.call_price(S,K,R,T2,Vol)

    # *********************** DELTA FORMULAS **********************
    @classmethod
    def call_delta(cls,S,K,R,T,Vol):
        delta = norm.cdf(cls.__d1(S,K,R,T,Vol))
        return round(delta,3)

    @classmethod
    def call_spread_delta(cls,S,K1,K2,R,T,Vol,isbull):
        if isbull:
            return cls.call_delta(S,K1,R,T,Vol) - cls.call_delta(S,K2,R,T,Vol)
        return -cls.call_delta(S,K1,R,T,Vol) + cls.call_delta(S,K2,R,T,Vol)

    @classmethod
    def put_delta(cls,S,K,R,T,Vol):
        delta = norm.cdf(cls.__d1(S,K,R,T,Vol))-1
        return round(delta,3)

    @classmethod
    def put_spread_delta(cls,S,K1,K2,R,T,Vol,isbull):
        if isbull:
            return - cls.put_delta(S,K2,R,T,Vol) + cls.put_delta(S,K1,R,T,Vol)
        return cls.put_delta(S, K2, R, T, Vol) - cls.put_delta(S, K1, R, T, Vol)

    @classmethod
    def call_digital_delta(cls,S,K,R,T,Vol):
        return round((norm.pdf(cls.__d2(S,K,R,T,Vol))/(S*Vol*math.sqrt(T)))*math.exp(-R*T),3)

    @classmethod
    def put_digital_delta(cls,S,K,R,T,Vol):
        return round(-cls.call_digital_delta(S,K,R,T,Vol),3)

    @classmethod
    def straddle_delta(cls,S,K,R,T,Vol):
        return cls.call_delta(S,K,R,T,Vol)+cls.put_delta(S,K,R,T,Vol)

    @classmethod
    def strangle_delta(cls,S,K1,K2,R,T,Vol):
        return cls.put_delta(S,K1,R,T,Vol)+cls.call_delta(S,K2,R,T,Vol)

    @classmethod
    def risk_rev_delta(cls,S,K1,K2,R,T,Vol):
        return -cls.put_delta(S, K1, R, T, Vol) + cls.call_delta(S, K2, R, T, Vol)

    @classmethod
    def calendar_delta(cls,S,K,R,T1,T2,Vol):
        return -cls.call_delta(S,K,R,T1,Vol)+cls.call_delta(S,K,R,T2,Vol)

    # *********************** GAMMA FORMULAS **********************
    @classmethod
    def gamma(cls,S,K,R,T,Vol):
        gamma = (1/(S*Vol*math.sqrt(T)))*norm.pdf(cls.__d1(S,K,R,T,Vol))
        return round(gamma,3)

    @classmethod
    def call_spread_gamma(cls,S,K1,K2,R,T,Vol,isbull):
        if isbull:
            return cls.gamma(S,K1,R,T,Vol)-cls.gamma(S,K2,R,T,Vol)
        return -cls.gamma(S,K1,R,T,Vol)+cls.gamma(S,K2,R,T,Vol)

    @classmethod
    def put_spread_gamma(cls,S,K1,K2,R,T,Vol,isbull):
        if isbull:
            return - cls.gamma(S,K2,R,T,Vol) + cls.gamma(S,K1,R,T,Vol)
        return cls.gamma(S,K2,R,T,Vol) - cls.gamma(S,K1,R,T,Vol)

    @classmethod
    def call_digital_gamma(cls,S,K,R,T,Vol):
        return round((math.exp(-R*T)*norm.pdf(cls.__d2(S,K,R,T,Vol))*cls.__d1(S,K,R,T,Vol))/(S**2*Vol**2*T),3)

    @classmethod
    def put_digital_gamma(cls,S,K,R,T,Vol):
        return round(-cls.call_digital_gamma(S,K,R,T,Vol),3)

    @classmethod
    def straddle_gamma(cls,S,K,R,T,Vol):
        return 2*cls.gamma(S,K,R,T,Vol)

    @classmethod
    def strangle_gamma(cls,S,K1,K2,R,T,Vol):
        return cls.gamma(S,K1,R,T,Vol)+cls.gamma(S,K2,R,T,Vol)

    @classmethod
    def risk_rev_gamma(cls,S,K1,K2,R,T,Vol):
        return -cls.gamma(S, K1, R, T, Vol) + cls.gamma(S, K2, R, T, Vol)

    @classmethod
    def calendar_gamma(cls, S, K, R, T1, T2, Vol):
        return -cls.gamma(S, K, R, T1, Vol) + cls.gamma(S, K, R, T2, Vol)

    # *********************** VEGA FORMULAS **********************
    @classmethod
    def vega(cls,S,K,R,T,Vol):
        vega = S*math.sqrt(Vol)*norm.pdf(cls.__d1(S,K,R,T,Vol))
        return round(vega,3)

    @classmethod
    def call_spread_vega(cls,S,K1,K2,R,T,Vol,isbull):
        if isbull:
            return cls.vega(S,K1,R,T,Vol) - cls.vega(S,K2,R,T,Vol)
        return - cls.vega(S,K1,R,T,Vol) + cls.vega(S,K2,R,T,Vol)

    @classmethod
    def call_digital_vega(cls,S,K,R,T,Vol):
        return round(-math.exp(-R*T)*cls.__d1(S,K,R,T,Vol)*norm.pdf(cls.__d2(S,K,R,T,Vol))/Vol,3)

    @classmethod
    def put_spread_vega(cls,S,K1,K2,R,T,Vol,isbull):
        if isbull:
            return - cls.vega(S,K2,R,T,Vol) + cls.vega(S,K1,R,T,Vol)
        return cls.vega(S,K2,R,T,Vol) - cls.vega(S,K1,R,T,Vol)

    @classmethod
    def put_digital_vega(cls,S,K,R,T,Vol):
        return round(-cls.call_digital_vega(S,K,R,T,Vol),3)

    @classmethod
    def straddle_vega(cls,S,K,R,T,Vol):
        return 2*cls.vega(S,K,R,T,Vol)

    @classmethod
    def strangle_vega(cls,S,K1,K2,R,T,Vol):
        return cls.vega(S,K1,R,T,Vol)+cls.vega(S,K2,R,T,Vol)

    @classmethod
    def risk_rev_vega(cls, S, K1, K2, R, T, Vol):
        return -cls.vega(S, K1, R, T, Vol) + cls.vega(S, K2, R, T, Vol)

    @classmethod
    def calendar_vega(cls, S, K, R, T1, T2, Vol):
        return -cls.vega(S, K, R, T1, Vol) + cls.vega(S, K, R, T2, Vol)

    # *********************** THETA FORMULAS **********************
    @classmethod
    def call_theta(cls,S,K,R,T,Vol):
        d2 = cls.__d2(S,K,R,T,Vol)
        theta = -(K*Vol*norm.pdf(d2)*math.exp(-R*T))/(2*math.sqrt(T)) - R*K*norm.cdf(d2)*math.exp(-R*T)
        return round(theta,3)

    @classmethod
    def call_spread_theta(cls,S,K1,K2,R,T,Vol,isbull):
        if isbull:
            return cls.call_theta(S,K1,R,T,Vol) - cls.call_theta(S,K2,R,T,Vol)
        return - cls.call_theta(S,K1,R,T,Vol) + cls.call_theta(S,K2,R,T,Vol)

    @classmethod
    def call_digital_theta(cls,S,K,R,T,Vol):
        disc_factor = math.exp(-R*T)
        d1 = cls.__d1(S,K,R,T,Vol)
        d2 = cls.__d2(S,K,R,T,Vol)
        return round(R*disc_factor*norm.cdf(d2)+disc_factor*norm.pdf(d2)*((d1/(2*T)) - (R/(Vol*math.sqrt(T)))),3)

    @classmethod
    def put_theta(cls,S,K,R,T,Vol):
        d1 = cls.__d1(S, K, R, T, Vol)
        d2 = cls.__d2(S, K, R, T, Vol)
        theta = R*K*math.exp(-R*T)*norm.cdf(-d2) - S*norm.pdf(d1)*Vol/(2*math.sqrt(T))
        return round(theta,3)

    @classmethod
    def put_spread_theta(cls,S,K1,K2,R,T,Vol,isbull):
        if isbull:
            return -cls.put_theta(S,K2,R,T,Vol) + cls.put_theta(S,K1,R,T,Vol)
        return cls.put_theta(S,K2,R,T,Vol) - cls.put_theta(S,K1,R,T,Vol)

    @classmethod
    def put_digital_theta(cls,S,K,R,T,Vol):
        return round(-R*math.exp(-R*T) - cls.call_digital_theta(S,K,R,T,Vol),3)

    @classmethod
    def straddle_theta(cls,S,K,R,T,Vol):
        return cls.call_theta(S,K,R,T,Vol)+cls.put_theta(S,K,R,T,Vol)

    @classmethod
    def strangle_theta(cls,S,K1,K2,R,T,Vol):
        return cls.put_theta(S,K1,R,T,Vol)+cls.call_theta(S,K2,R,T,Vol)

    @classmethod
    def risk_rev_theta(cls, S, K1, K2, R, T, Vol):
        return -cls.put_theta(S, K1, R, T, Vol) + cls.call_theta(S, K2, R, T, Vol)

    @classmethod
    def calendar_theta(cls, S, K, R, T1, T2, Vol):
        return -cls.call_theta(S, K, R, T1, Vol) + cls.call_theta(S, K, R, T2, Vol)

    # *********************** PAYOFF GRAPH CALLERS **********************
    @classmethod
    def payoff_lists(cls, S, K, R, T, Vol, call_price, put_price):
        """Return a tuple : (list of strikes, list of Y curve , list of title)"""
        return graph_generator.Plotter.get_payoff_lists((cls.call_price, cls.put_price)
                                                        , K, R, T, Vol,cls.__oneDay,
                                                        ["Call", "Put"],
                                                        (call_price, put_price))

    @classmethod
    def payoff_call_spread(cls,K1,K2,R,T,Vol,bull_price,bear_price):
        return graph_generator.Plotter.get_payoff_strategy((cls.call_spread_price,cls.call_spread_price,cls.call_spread_price,cls.call_spread_price),
                                                                  ((K1,K2,R,T,Vol,True),(K1,K2,R,cls.__oneDay,Vol,True),(K1,K2,R,T,Vol,False),(K1,K2,R,cls.__oneDay,Vol,False)),
                                                                  ["Bull Sp.","Bear Sp."],
                                                                  (bull_price,bull_price, bear_price,bear_price),
                                                                  (K1+K2)/2)

    @classmethod
    def payoff_put_spread(cls, K1, K2, R, T, Vol, bull_price, bear_price):
        return graph_generator.Plotter.get_payoff_strategy((cls.put_spread_price, cls.put_spread_price,cls.put_spread_price, cls.put_spread_price),
                                                                  ((K1, K2, R, T, Vol, True),(K1, K2, R, cls.__oneDay, Vol, True),
                                                                   (K1, K2, R, T, Vol, False),(K1, K2, R, cls.__oneDay, Vol, False)),
                                                                  ["Bull Spread","Bear Spread"],
                                                                 (bull_price,bull_price, bear_price,bear_price),
                                                                  (K1 + K2) / 2)

    @classmethod
    def payoff_digital_graph(cls, S, K, R, T, Vol, call_price, put_price):
        return graph_generator.Plotter.get_payoff_lists((cls.call_digital_price, cls.put_digital_price)
                                                         , K, R, T, Vol,cls.__oneDay,
                                                         ["Digital Call", "Digital Put"],
                                                         (call_price, put_price))

    @classmethod
    def straddle_payoff_graph(cls,S,K,R,T,Vol,straddle_price):
        return graph_generator.Plotter.get_payoff_lists((cls.straddle_price,)
                                                         , K, R, T, Vol,cls.__oneDay,
                                                         ["Straddle"],
                                                         (straddle_price,))

    @classmethod
    def strangle_payoff_graph(cls,S,K1,K2,R,T,Vol,price):
        return graph_generator.Plotter.get_payoff_strategy([cls.strangle_price,cls.strangle_price]
                                                         , [[K1,K2, R, T, Vol],[K1,K2, R, cls.__oneDay, Vol]],
                                                         ["Strangle"],
                                                         [price,price],(K1+K2)/2)

    @classmethod
    def risk_rev_payoff_graph(cls, S, K1, K2, R, T, Vol,price):
         return graph_generator.Plotter.get_payoff_strategy([cls.risk_rev_price,cls.risk_rev_price]
                                                                  , [[K1, K2, R, T, Vol],[K1, K2, R, cls.__oneDay, Vol]],
                                                                  ["Risk Reversal"],
                                                                  [price,price], (K1 + K2) / 2)

    @classmethod
    def calendar_payoff_graph(cls, S, K, R, T1, T2, Vol,price):
        return graph_generator.Plotter.get_payoff_strategy([cls.calendar_price,cls.calendar_price], [[K, R, T1, T2, Vol],[K, R, cls.__oneDay,  T2-T1+cls.__oneDay, Vol]],
                                                           ["Calendar Spread"],
                                                           [price,price], K)

    # *********************** GREEKS GRAPH CALLERS **********************
    @classmethod
    def greeks_graph(cls,S,K,R,T,Vol):
        list_greeks = (cls.gamma,cls.gamma,cls.call_delta,cls.put_delta,cls.call_theta,cls.put_theta,cls.vega,cls.vega)
        list_title = ["Call Gamma","Put Gamma","Call Delta","Put Delta","Call Theta","Put Theta","Call Vega","Put Vega"]
        return graph_generator.Plotter.get_graph_greeks(list_greeks,K,R,T,Vol,cls.__oneDay,list_title)

    @classmethod
    def greeks_digital_graph(cls,S,K,R,T,Vol):
        list_greeks = (
        cls.call_digital_gamma, cls.put_digital_gamma, cls.call_digital_delta, cls.put_digital_delta, cls.call_digital_theta, cls.put_digital_theta, cls.call_digital_vega, cls.put_digital_vega)
        list_title = [
        "Digital Call Gamma", "Digital Put Gamma", "Digital Call Delta", "Digital Put Delta", "Digital Call Theta", "Digital Put Theta","Digital Call Vega", "Digital Put Vega"]
        return graph_generator.Plotter.get_graph_greeks(list_greeks, K, R, T, Vol,cls.__oneDay, list_title)

    @classmethod
    def call_spread_greeks_graph(cls,K1,K2,R,T,Vol):
        list_greeks = (
        cls.call_spread_gamma, cls.call_spread_gamma, cls.call_spread_delta, cls.call_spread_delta, cls.call_spread_theta, cls.call_spread_theta, cls.call_spread_vega, cls.call_spread_vega)
        list_title = [
        "Bull Gamma", "Bear Gamma", "Bull Delta", "Bear Delta", "Bull Theta", "Bear Theta" , "Bull Vega", "Bear Vega"]
        return graph_generator.Plotter.get_graph_strategy_greeks(list_greeks, ((K1,K2,R,T,Vol,True),(K1,K2,R,cls.__oneDay,Vol,True),(K1,K2,R,T,Vol,False),(K1,K2,R,cls.__oneDay,Vol,False)), list_title,(K1+K2)/2)

    @classmethod
    def put_spread_greeks_graph(cls,K1,K2,R,T,Vol):
        list_greeks = (
            cls.put_spread_delta, cls.put_spread_delta, cls.put_spread_gamma, cls.put_spread_gamma,
            cls.put_spread_vega, cls.put_spread_vega, cls.put_spread_theta, cls.put_spread_theta)
        list_title = [
            "Bull Gamma", "Bear Gamma", "Bull Delta", "Bear Delta", "Bull Theta",
            "Bear Theta" ,"Bull Vega", "Bear Vega"]

        return graph_generator.Plotter.get_graph_strategy_greeks(list_greeks, (
        (K1, K2, R, T, Vol, True),(K1, K2, R, cls.__oneDay, Vol, True), (K1, K2, R, T, Vol, False),(K1, K2, R, cls.__oneDay, Vol, False)), list_title, (K1 + K2) / 2)

    @classmethod
    def straddle_greeks_graph(cls, S, K, R, T, Vol):
        list_greeks = (cls.straddle_gamma, cls.straddle_delta, cls.straddle_theta, cls.straddle_vega)
        list_title = ["Gamma","Delta", "Theta", "Vega"]
        return graph_generator.Plotter.get_graph_strategy_greeks_one_leg(list_greeks, ((K, R, T, Vol),(K, R, cls.__oneDay, Vol)), list_title, K)

    @classmethod
    def strangle_greeks_graph(cls, S, K1, K2, R, T, Vol):
        list_greeks = (cls.strangle_gamma,cls.strangle_delta, cls.strangle_theta, cls.strangle_vega)
        list_title = ["Gamma", "Delta", "Theta", "Vega"]
        return graph_generator.Plotter.get_graph_strategy_greeks_one_leg(list_greeks, ((K1, K2, R, T, Vol),(K1, K2, R, cls.__oneDay, Vol)), list_title,
                                                                          (K1 + K2) / 2)

    @classmethod
    def risk_rev_greeks_graph(cls, S, K1, K2, R, T, Vol):
        list_greeks = (cls.risk_rev_gamma,cls.risk_rev_delta, cls.risk_rev_theta,cls.risk_rev_vega)
        list_title = ["Gamma", "Delta","Theta","Vega"]
        return graph_generator.Plotter.get_graph_strategy_greeks_one_leg(list_greeks, ((K1, K2, R, T, Vol),(K1, K2, R, cls.__oneDay, Vol)), list_title,
                                                                          (K1 + K2) / 2)

    @classmethod
    def calendar_greeks_graph(cls, S, K, R, T1, T2, Vol):
        list_greeks = (cls.calendar_gamma, cls.calendar_delta, cls.calendar_theta, cls.calendar_vega)
        list_title = ["Gamma", "Delta", "Theta", "Vega"]
        return graph_generator.Plotter.get_graph_strategy_greeks_one_leg(list_greeks, ((K, R, T1, T2, Vol),(K, R, cls.__oneDay, T2-T1+cls.__oneDay, Vol)), list_title,K)
