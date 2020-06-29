from flask import Flask, redirect, url_for, request,render_template
from elasticsearch import Elasticsearch
from sinling import SinhalaTokenizer,preprocess, word_joiner,word_splitter





app = Flask(__name__)
tokenizer = SinhalaTokenizer()
es = Elasticsearch()
hits=[]
lyrcs_list=[]
dic={
      ""


}

# @app.route('/success/<name>')
# def success(name):
#    return 'welcome %s' % name

# @app.route('/search',methods = ['POST', 'GET'])
# print(word_splitter.split("මම ගැයූ ගී"))
@app.route('/',methods = ['GET'])
def main():
      return render_template('ui.html')

@app.route('/',methods = ['POST'])
def search():
      query_request= request.form["query"].strip()
      affix=word_splitter.split(query_request)["affix"]
      result = es.search(index="lyrics", doc_type="doc",body={  "query": {"match" : { "genere": affix}}})
      hits = result["hits"]["hits"]
      
      boosted_query_for_artist= es.search(index="lyrics", doc_type="doc",body={
             {"query" : {
                  "multi_match" : {
                        "query" : result,
                        "fields" : [ "artist^3","lyrics by" ,"music by","lyrics","name" ]
                  }
    }
}


      })

      

      if(len(hits)==0):
            return render_template('ui.html', result = "No search result exists")
      lyrcs_list=[lyrics["_source"] for lyrics in hits ]
      return render_template('ui.html', results = lyrcs_list)

#    else:
#       user = request.args.get('nm')
#       return redirect(url_for('success',name = user))

if __name__ == '__main__':
   app.run(debug = True)