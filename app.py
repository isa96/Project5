from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib
from helper import *

matplotlib.use('Agg')

app = Flask(__name__)

data = load_data()

@app.route("/")
def index():
	percent_fraud = float(pd.crosstab(index=data['fraud_reported'], columns='count', normalize=True).loc['Y','count']*100)
	fraud_loss = pd.crosstab(index=data['fraud_reported'], columns='Total', values=data['total_claim_amount'], aggfunc='sum').loc['Y','Total']
	average_claim = data.total_claim_amount.mean()
	 
	card_data = dict(
		percent_fraud = f'{percent_fraud}%',
		fraud_loss = f'US$ {fraud_loss:,}',
		average_claim = f'US$ {average_claim:,}'
		)

	# generate plot
	plot_age_res = plot_age(data)
	plot_premium_res = plot_premium(data)
	plot_incident_res = plot_incident(data)
	plot_report_res = plot_report(data)

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_age_res=plot_age_res,
		plot_premium_res=plot_premium_res,
		plot_incident_res=plot_incident_res,
		plot_report_res=plot_report_res
		)


if __name__ == "__main__": 
    app.run(debug=True)
