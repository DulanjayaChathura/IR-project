from flask import Flask, redirect, url_for, request,render_template
from elasticsearch import Elasticsearch


app = Flask(__name__)
es = Elasticsearch()
hits=[]
lyrcs_list=[]

# @app.route('/success/<name>')
# def success(name):
#    return 'welcome %s' % name

# @app.route('/search',methods = ['POST', 'GET'])

@app.route('/',methods = ['GET'])
def main():
      return render_template('ui.html')

@app.route('/',methods = ['POST'])
def search():

      result = es.search(index="lyrics", doc_type="doc",body={  "query": {"match" : { "genere": request.form['query']}}})
      hits = result["hits"]["hits"]
      if(len(hits)==0):
            return render_template('ui.html', result = "No search result exists")
      lyrcs_list=[lyrics["_source"] for lyrics in hits ]
      return render_template('ui.html', results = lyrcs_list)

#    else:
#       user = request.args.get('nm')
#       return redirect(url_for('success',name = user))

if __name__ == '__main__':
   app.run(debug = True)