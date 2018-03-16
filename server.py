from flask import Flask, redirect,render_template, request
import json
import view_model as vm

app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template("index.html",page_title="Pricer")

@app.route("/get_price",methods=['POST'])
def get_price():
    dict_args = {}
    dict_args['strategy'] = request.form.get("strategy","Vanilla")
    dict_args['type'] =  request.form.get("type","European")
    dict_args['spot'] = request.form.get("spot",0)
    dict_args['strike'] = request.form.get("strike",0)
    dict_args['strike2'] = request.form.get("strike2",0)
    dict_args['maturity'] = request.form.get("maturity")
    dict_args['maturity2'] = request.form.get("maturity2",0)
    dict_args['volatility'] = request.form.get("volatility",0.2)
    dict_args['interest_rate'] = request.form.get("interest_rate",0)

    #The get_price() method from View_Model returns a render_template with the good html page
    return vm.View_Model(dict_args).get_price()

if __name__ == "__main__":
    app.run(debug=True)