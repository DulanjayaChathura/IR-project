from flask import Flask, redirect, url_for, request,render_template
from elasticsearch import Elasticsearch
from sinling import SinhalaTokenizer,preprocess, word_joiner,word_splitter





app = Flask(__name__)
tokenizer = SinhalaTokenizer()
es = Elasticsearch()
hits=[]
lyrcs_list=[]
processed_query_request=""

music_by_list=["සංගීත","අධ්‍යක්ෂණය","තනු"]
lyrics_by_list=["රචිත", "රචනය","ලියන","ලියූ"]
genere_list =["පැරණි","ඉල්ලීම","චිත්‍රපට","ක්ලැසික්","පොප්ස්","කැලිප්සෝ","ගෝල්ඩන් ඕල්ඩීස්","යුගල","පොප්","උද්වේගකර"]
key_list =["major","minor"]
artist_list=["ගේ","ගැයූ","ගායනා කල","ගායනා කරන"]
# possetion_list=["","","",]

popular_list=["ජනප්‍රිය","හොඳම","ප්‍රසිද්ධ","ප්‍රකට","ජනප්‍රියතම"]

# ["name", "artist","genere","lyrics by","music by","key","lyrics" ]  
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
      boosting_list=[]
      is_rating_query=False 
      query_request= request.form["query"].strip().lower()
      
      token_list=tokenizer.tokenize(query_request)
      
      
      # boosting_list[1] = ["artist^3" if ("ගේ" in artist) else "artist" for artist in  token_list][0]
      # boosting_list[2] = ["genere^3" if (genere in token_list) else "genere" for genere in  genere_list][0]

      if(any(x in genere_list for x in token_list)):
            boosting_list.append("genere^2")
      if(any(x in lyrics_by_list for x in token_list)):
            boosting_list.append("lyrics by^2")
      if(any(x in music_by_list for x in token_list)):
            boosting_list.append("music by^2")
      if(any(x in key_list for x in token_list)):
            boosting_list.append("key^2")
      if(any(x in artist_list for x in token_list)):
            boosting_list.append("artist^2")
      if(any(x in popular_list for x in token_list)):
            is_rating_query= True

      # = [ if (lyrics_by in token_list) else "lyrics by"for lyrics_by in  lyrics_by_list][0]
      # boosting_list[4] = ["music by^3" if (music_by in token_list) else "music by"for music_by in  music_by_list][0]
      # boosting_list[5] = ["key^3" if (music_by in token_list) else "key"for music_by in  music_by_list][0]

      # affix=word_splitter.split(query_request)["affix"]
     
      processed_query_request=" ".join([word_splitter.split(item)["base"] for item in token_list]) 
      # result = es.search(index="lyrics", doc_type="doc",body={  "query": {"match" : { "genere": affix}}})

      boosting_list=list(dict.fromkeys(boosting_list))
      print(query_request) 
      print(token_list)
      print(processed_query_request)
      print(boosting_list) 
      boosted_query= es.search(index="lyrics", doc_type="doc",body=
             {"query" : {
                  "multi_match" : {
                        "query" : processed_query_request,
                        "fields" : boosting_list
                  }
      }
      }


      )

      hits = boosted_query["hits"]["hits"]

      if(len(hits)==0):
            return render_template('ui.html', result = "No search result exists")
      lyrcs_list=[lyrics["_source"] for lyrics in hits ]
      return render_template('ui.html', results = lyrcs_list)

#    else:
#       user = request.args.get('nm')
#       return redirect(url_for('success',name = user))

if __name__ == '__main__':
   app.run(debug = True)