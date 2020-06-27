from flask import Flask, render_template, request, redirect, url_for
import tickgraph
from bokeh.embed import components

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        tkr=request.form['ticker']
        script, div = tickgraph.get_a_graph(tkr)
        # script, div = components(p)
        # return render_template('stock.html')
        return render_template('out.html', script=script, div=div)
    else:
        return render_template('frontpg.html')

if __name__ == '__main__':
     app.debug=True
     app.run(port=33507)



 



