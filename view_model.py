import datetime as dt
from model import calculator
from flask import render_template

class View_Model():
    def __init__(self,dict_values):
        self.strategy = dict_values["strategy"]
        self.type = dict_values["type"]
        self.spot = float(dict_values["spot"])
        self.strike = float(dict_values["strike"])
        self.strike2 = dict_values["strike2"] if dict_values["strike2"] == "" else float(dict_values["strike2"])
        self.maturity = dict_values["maturity"]
        self.maturity2 = dict_values.get("maturity2","")
        self.volatility = float(dict_values["volatility"])
        self.interest_rate = float(dict_values["interest_rate"])

    def get_price(self):
        """Returns the render template with the good html page given the strategy selected"""
        self.dict_results = dict()
        self.__getTimeToMaturity() #timeToMaturity is accessible

        # ***** The HTML page to display is different as the case may be *****

        if self.strategy == "Vanilla":
            self.__getVanillaResults()
            rows = (
                ("Price",self.dict_results["call_price"],self.dict_results["put_price"]),
                ("Delta", self.dict_results["call_delta"], self.dict_results["put_delta"]),
                ("Gamma", self.dict_results["call_gamma"], self.dict_results["put_gamma"]),
                ("Vega", self.dict_results["call_vega"], self.dict_results["put_vega"]),
                ("Theta", self.dict_results["call_theta"], self.dict_results["put_theta"])
            )
            return render_template("dashboard.html",
                           title="Dashboard",
                           page_title="Dashboard",
                           strike=self.dict_results["payoff_lists"][0],
                           payoff=self.dict_results["payoff_lists"][1],
                           titles=self.dict_results["payoff_lists"][2],
                           greeks=self.dict_results["greeks_lists"][1],
                           greeks_titles=self.dict_results["greeks_lists"][2],
                           isOneLeg="false",
                           input_names=["Spot","Strike","Maturity","Volatility"],
                           inputs=[self.spot,self.strike,round(self.timeToMaturity,3),self.volatility],
                           columns_name=["Call","Put"],
                           rows = rows)

        elif self.strategy in ["Call Spread","Put Spread"]:
            self.__getCallSpreadResults() if self.strategy == "Call Spread" else self.__getPutSpreadResults()
            rows = (
                ("Price", self.dict_results["bull_price"], self.dict_results["bear_price"]),
                ("Delta", self.dict_results["bull_delta"], self.dict_results["bear_delta"]),
                ("Gamma", self.dict_results["bull_gamma"], self.dict_results["bear_gamma"]),
                ("Vega", self.dict_results["bull_vega"], self.dict_results["bear_vega"]),
                ("Theta", self.dict_results["bull_theta"], self.dict_results["bear_theta"])
            )

            col_names = ["Bull Call Spread", "Bear Call Spread"] if self.strategy == "Call Spread" else ["Bull Put Spread", "Bear Put Spread"]

            return render_template("dashboard.html",
                                   title="Dashboard",
                                   page_title="Dashboard",
                                   strike=self.dict_results["payoff_lists"][0],
                                   payoff=self.dict_results["payoff_lists"][1],
                                   titles=self.dict_results["payoff_lists"][2],
                                   greeks=self.dict_results["greeks_lists"][1],
                                   greeks_titles=self.dict_results["greeks_lists"][2],
                                   isOneLeg="false",
                                   input_names=["Spot", "Strike 1","Strike 2", "Maturity", "Volatility"],
                                   inputs=[self.spot, self.strike,self.strike2, round(self.timeToMaturity, 3), self.volatility],
                                   columns_name=col_names,
                                   rows=rows)

        elif self.strategy == "Digital":
            self.__getDigitalResults()
            rows = (
                ("Price", self.dict_results["call_price"], self.dict_results["put_price"]),
                ("Delta", self.dict_results["call_delta"], self.dict_results["put_delta"]),
                ("Gamma", self.dict_results["call_gamma"], self.dict_results["put_gamma"]),
                ("Vega", self.dict_results["call_vega"], self.dict_results["put_vega"]),
                ("Theta", self.dict_results["call_theta"], self.dict_results["put_theta"])
            )
            return render_template("dashboard.html",
                                   title="Dashboard",
                                   page_title="Dashboard",
                                   strike=self.dict_results["payoff_lists"][0],
                                   payoff=self.dict_results["payoff_lists"][1],
                                   titles=self.dict_results["payoff_lists"][2],
                                   greeks=self.dict_results["greeks_lists"][1],
                                   greeks_titles=self.dict_results["greeks_lists"][2],
                                   isOneLeg="false",
                                   input_names=["Spot", "Strike", "Maturity", "Volatility"],
                                   inputs=[self.spot, self.strike, round(self.timeToMaturity, 3), self.volatility],
                                   columns_name=["Call", "Put"],
                                   rows=rows)

        elif self.strategy == "Straddle":
            self.__getStraddleResults()
            rows = (
                ("Price", self.dict_results["straddle_price"]),
                ("Delta", self.dict_results["straddle_delta"]),
                ("Gamma", self.dict_results["straddle_gamma"]),
                ("Vega", self.dict_results["straddle_vega"]),
                ("Theta", self.dict_results["straddle_theta"])
            )
            return render_template("dashboard.html",
                                   title="Dashboard",
                                   page_title="Dashboard",
                                   strike=self.dict_results["payoff_lists"][0],
                                   payoff=self.dict_results["payoff_lists"][1],
                                   titles=self.dict_results["payoff_lists"][2],
                                   greeks=self.dict_results["greeks_lists"][1],
                                   greeks_titles=self.dict_results["greeks_lists"][2],
                                   isOneLeg="true",
                                   input_names=["Spot", "Strike", "Maturity", "Volatility"],
                                   inputs=[self.spot, self.strike, round(self.timeToMaturity, 3), self.volatility],
                                   columns_name=["Straddle"],
                                   rows=rows)

        elif self.strategy == "Strangle":
            self.__getStrangleResults()
            rows = (
                ("Price", self.dict_results["strangle_price"]),
                ("Delta", self.dict_results["strangle_delta"]),
                ("Gamma", self.dict_results["strangle_gamma"]),
                ("Vega", self.dict_results["strangle_vega"]),
                ("Theta", self.dict_results["strangle_theta"])
            )
            return render_template("dashboard.html",
                                   title="Dashboard",
                                   page_title="Dashboard",
                                   strike=self.dict_results["payoff_lists"][0],
                                   payoff=self.dict_results["payoff_lists"][1],
                                   titles=self.dict_results["payoff_lists"][2],
                                   greeks=self.dict_results["greeks_lists"][1],
                                   greeks_titles=self.dict_results["greeks_lists"][2],
                                   isOneLeg="true",
                                   input_names=["Spot", "Strike","Strike 2", "Maturity", "Volatility"],
                                   inputs=[self.spot, self.strike,self.strike2, round(self.timeToMaturity, 3), self.volatility],
                                   columns_name=["Strangle"],
                                   rows=rows)

        elif self.strategy == "Risk Reversal":
            self.__getRiskRevResults()
            rows = (
                ("Price", self.dict_results["risk_rev_price"]),
                ("Delta", self.dict_results["risk_rev_delta"]),
                ("Gamma", self.dict_results["risk_rev_gamma"]),
                ("Vega", self.dict_results["risk_rev_vega"]),
                ("Theta", self.dict_results["risk_rev_theta"])
            )
            return render_template("dashboard.html",
                                   title="Dashboard",
                                   page_title="Dashboard",
                                   strike=self.dict_results["payoff_lists"][0],
                                   payoff=self.dict_results["payoff_lists"][1],
                                   titles=self.dict_results["payoff_lists"][2],
                                   greeks=self.dict_results["greeks_lists"][1],
                                   greeks_titles=self.dict_results["greeks_lists"][2],
                                   isOneLeg="true",
                                   input_names=["Spot", "Strike", "Strike 2", "Maturity", "Volatility"],
                                   inputs=[self.spot, self.strike, self.strike2, round(self.timeToMaturity, 3),
                                           self.volatility],
                                   columns_name=["Risk Reversal"],
                                   rows=rows)

        elif self.strategy == "Calendar Spread":
            self.__getCalendarResults()
            rows = (
                ("Price", self.dict_results["calendar_price"]),
                ("Delta", self.dict_results["calendar_delta"]),
                ("Gamma", self.dict_results["calendar_gamma"]),
                ("Vega", self.dict_results["calendar_vega"]),
                ("Theta", self.dict_results["calendar_theta"])
            )
            return render_template("dashboard.html",
                                   title="Dashboard",
                                   page_title="Dashboard",
                                   strike=self.dict_results["payoff_lists"][0],
                                   payoff=self.dict_results["payoff_lists"][1],
                                   titles=self.dict_results["payoff_lists"][2],
                                   greeks=self.dict_results["greeks_lists"][1],
                                   greeks_titles=self.dict_results["greeks_lists"][2],
                                   isOneLeg="true",
                                   input_names=["Spot", "Strike", "Maturity 1", "Maturity 2", "Volatility"],
                                   inputs=[self.spot, self.strike, round(self.timeToMaturity, 3),round(self.timeToMaturity2,3),
                                           self.volatility],
                                   columns_name=["Calendar Spread"],
                                   rows=rows)

        #TODO : Strategies :

        elif self.strategy == "Asian":
            pass

        elif self.strategy == "Barrier":
            pass

        elif self.strategy == "Lookback":
            pass

    def __getVanillaResults(self):
        variables = [self.spot,self.strike,self.interest_rate,self.timeToMaturity,self.volatility]

        self.dict_results["call_price"] = calculator.BlackScholes.call_price(*variables)
        self.dict_results["put_price"] = calculator.BlackScholes.put_price(*variables)
        self.dict_results["call_delta"] = calculator.BlackScholes.call_delta(*variables)
        self.dict_results["put_delta"] = calculator.BlackScholes.put_delta(*variables)
        self.dict_results["call_gamma"] = calculator.BlackScholes.gamma(*variables)
        self.dict_results["put_gamma"] = calculator.BlackScholes.gamma(*variables)
        self.dict_results["call_vega"] = calculator.BlackScholes.vega(*variables)
        self.dict_results["put_vega"] = calculator.BlackScholes.vega(*variables)
        self.dict_results["call_theta"] = calculator.BlackScholes.call_theta(*variables)
        self.dict_results["put_theta"] = calculator.BlackScholes.put_theta(*variables)
        self.dict_results["payoff_lists"] = calculator.BlackScholes.payoff_lists(*variables,self.dict_results["call_price"],self.dict_results["put_price"])
        self.dict_results["greeks_lists"] = calculator.BlackScholes.greeks_graph(*variables)

    def __getCallSpreadResults(self):
        variables = (self.spot, self.strike,self.strike2, self.interest_rate, self.timeToMaturity, self.volatility)
        self.dict_results["bull_price"] = calculator.BlackScholes.call_spread_price(*variables,isbull=True)
        self.dict_results["bear_price"] = calculator.BlackScholes.call_spread_price(*variables,isbull=False)
        self.dict_results["bull_delta"] = calculator.BlackScholes.call_spread_delta(*variables,isbull=True)
        self.dict_results["bear_delta"] = calculator.BlackScholes.call_spread_delta(*variables,isbull=False)
        self.dict_results["bull_gamma"] = calculator.BlackScholes.call_spread_gamma(*variables,isbull=True)
        self.dict_results["bear_gamma"] = calculator.BlackScholes.call_spread_gamma(*variables,isbull=False)
        self.dict_results["bull_vega"] = calculator.BlackScholes.call_spread_vega(*variables,isbull=True)
        self.dict_results["bear_vega"] = calculator.BlackScholes.call_spread_vega(*variables,isbull=False)
        self.dict_results["bull_theta"] = calculator.BlackScholes.call_spread_theta(*variables,isbull=True)
        self.dict_results["bear_theta"] = calculator.BlackScholes.call_spread_theta(*variables,isbull=False)
        self.dict_results["payoff_lists"] = calculator.BlackScholes.payoff_call_spread(*variables[1:],self.dict_results["bull_price"],self.dict_results["bear_price"])
        self.dict_results["greeks_lists"] = calculator.BlackScholes.call_spread_greeks_graph(*variables[1:])

    def __getPutSpreadResults(self):
        variables = (self.spot, self.strike, self.strike2, self.interest_rate, self.timeToMaturity, self.volatility)
        self.dict_results["bull_price"] = calculator.BlackScholes.put_spread_price(*variables, isbull=True)
        self.dict_results["bear_price"] = calculator.BlackScholes.put_spread_price(*variables, isbull=False)
        self.dict_results["bull_delta"] = calculator.BlackScholes.put_spread_delta(*variables, isbull=True)
        self.dict_results["bear_delta"] = calculator.BlackScholes.put_spread_delta(*variables, isbull=False)
        self.dict_results["bull_gamma"] = calculator.BlackScholes.put_spread_gamma(*variables, isbull=True)
        self.dict_results["bear_gamma"] = calculator.BlackScholes.put_spread_gamma(*variables, isbull=False)
        self.dict_results["bull_vega"] = calculator.BlackScholes.put_spread_vega(*variables, isbull=True)
        self.dict_results["bear_vega"] = calculator.BlackScholes.put_spread_vega(*variables, isbull=False)
        self.dict_results["bull_theta"] = calculator.BlackScholes.put_spread_theta(*variables, isbull=True)
        self.dict_results["bear_theta"] = calculator.BlackScholes.put_spread_theta(*variables, isbull=False)
        self.dict_results["payoff_lists"] = calculator.BlackScholes.payoff_put_spread(*variables[1:],
                                                                                             self.dict_results[
                                                                                                 "bull_price"],
                                                                                             self.dict_results[
                                                                                                 "bear_price"])
        self.dict_results["greeks_lists"] = calculator.BlackScholes.put_spread_greeks_graph(*variables[1:])

    def __getDigitalResults(self):
        variables = [self.spot, self.strike, self.interest_rate, self.timeToMaturity, self.volatility]

        self.dict_results["call_price"] = calculator.BlackScholes.call_digital_price(*variables)
        self.dict_results["put_price"] = calculator.BlackScholes.put_digital_price(*variables)
        self.dict_results["call_delta"] = calculator.BlackScholes.call_digital_delta(*variables)
        self.dict_results["put_delta"] = calculator.BlackScholes.put_digital_delta(*variables)
        self.dict_results["call_gamma"] = calculator.BlackScholes.call_digital_gamma(*variables)
        self.dict_results["put_gamma"] = calculator.BlackScholes.put_digital_gamma(*variables)
        self.dict_results["call_vega"] = calculator.BlackScholes.call_digital_vega(*variables)
        self.dict_results["put_vega"] = calculator.BlackScholes.put_digital_vega(*variables)
        self.dict_results["call_theta"] = calculator.BlackScholes.call_digital_theta(*variables)
        self.dict_results["put_theta"] = calculator.BlackScholes.put_digital_theta(*variables)
        self.dict_results["payoff_lists"] = calculator.BlackScholes.payoff_digital_graph(*variables,
                                                                                       self.dict_results["call_price"],
                                                                                       self.dict_results["put_price"])
        self.dict_results["greeks_lists"] = calculator.BlackScholes.greeks_digital_graph(*variables)

    def __getStraddleResults(self):
        variables = [self.spot, self.strike, self.interest_rate, self.timeToMaturity, self.volatility]

        self.dict_results["straddle_price"] = calculator.BlackScholes.call_price(*variables)+calculator.BlackScholes.put_price(*variables)
        self.dict_results["straddle_delta"] = calculator.BlackScholes.call_delta(*variables)+calculator.BlackScholes.put_delta(*variables)
        self.dict_results["straddle_gamma"] = calculator.BlackScholes.gamma(*variables)+calculator.BlackScholes.gamma(*variables)
        self.dict_results["straddle_vega"] = calculator.BlackScholes.vega(*variables)+calculator.BlackScholes.vega(*variables)
        self.dict_results["straddle_theta"] = calculator.BlackScholes.call_theta(*variables)+calculator.BlackScholes.put_theta(*variables)
        self.dict_results["payoff_lists"] = calculator.BlackScholes.straddle_payoff_graph(*variables,
                                                                                       self.dict_results["straddle_price"])
        self.dict_results["greeks_lists"] = calculator.BlackScholes.straddle_greeks_graph(*variables)

    def __getStrangleResults(self):
        variables = [self.spot, self.strike,self.strike2, self.interest_rate, self.timeToMaturity, self.volatility]

        self.dict_results["strangle_price"] = calculator.BlackScholes.strangle_price(*variables)
        self.dict_results["strangle_delta"] = calculator.BlackScholes.strangle_delta(*variables)
        self.dict_results["strangle_gamma"] = calculator.BlackScholes.strangle_gamma(*variables)
        self.dict_results["strangle_vega"] = calculator.BlackScholes.strangle_vega(*variables)
        self.dict_results["strangle_theta"] = calculator.BlackScholes.strangle_theta(*variables)
        self.dict_results["payoff_lists"] = calculator.BlackScholes.strangle_payoff_graph(*variables,
                                                                                       self.dict_results["strangle_price"])
        self.dict_results["greeks_lists"] = calculator.BlackScholes.strangle_greeks_graph(*variables)

    def __getRiskRevResults(self):
        variables = [self.spot, self.strike, self.strike2, self.interest_rate, self.timeToMaturity, self.volatility]

        self.dict_results["risk_rev_price"] = calculator.BlackScholes.risk_rev_price(*variables)
        self.dict_results["risk_rev_delta"] = calculator.BlackScholes.risk_rev_delta(*variables)
        self.dict_results["risk_rev_gamma"] = calculator.BlackScholes.risk_rev_gamma(*variables)
        self.dict_results["risk_rev_vega"] = calculator.BlackScholes.risk_rev_vega(*variables)
        self.dict_results["risk_rev_theta"] = calculator.BlackScholes.risk_rev_theta(*variables)
        self.dict_results["payoff_lists"] = calculator.BlackScholes.risk_rev_payoff_graph(*variables,
                                                                                                self.dict_results[
                                                                                                    "risk_rev_price"])
        self.dict_results["greeks_lists"] = calculator.BlackScholes.risk_rev_greeks_graph(*variables)

    def __getCalendarResults(self):
        variables = (self.spot, self.strike, self.interest_rate, self.timeToMaturity,self.timeToMaturity2, self.volatility)
        self.dict_results["calendar_price"] = calculator.BlackScholes.calendar_price(*variables)
        self.dict_results["calendar_delta"] = calculator.BlackScholes.calendar_delta(*variables)
        self.dict_results["calendar_gamma"] = calculator.BlackScholes.calendar_gamma(*variables)
        self.dict_results["calendar_vega"] = calculator.BlackScholes.calendar_vega(*variables)
        self.dict_results["calendar_theta"] = calculator.BlackScholes.calendar_theta(*variables)
        self.dict_results["payoff_lists"] = calculator.BlackScholes.calendar_payoff_graph(*variables,self.dict_results["calendar_price"])
        self.dict_results["greeks_lists"] = calculator.BlackScholes.calendar_greeks_graph(*variables)

    def __getTimeToMaturity(self):
        """Computes the time to maturity in year given the real maturity date in format dd/mm/yyyy"""
        maturity = dt.datetime.strptime(self.maturity,"%d/%m/%Y").date()
        today = dt.date.today()
        self.timeToMaturity = (maturity-today).days/365 #In years

        if self.maturity2 != "":
            maturity = dt.datetime.strptime(self.maturity2, "%d/%m/%Y").date()
            self.timeToMaturity2 = (maturity - today).days / 365  # In years
