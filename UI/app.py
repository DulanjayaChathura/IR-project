from flask import Flask, redirect, url_for, request,render_template
from elasticsearch import Elasticsearch
from sinling import SinhalaTokenizer,preprocess, word_joiner,word_splitter
import json




app = Flask(__name__)
tokenizer = SinhalaTokenizer()
es = Elasticsearch()
hits=[]
lyrcs_list=[]
processed_query_request=""

music_by_list=["සංගීත","අධ්‍යක්ෂණය","තනු","රචනය","ලියන ලද","ලියපු"]
lyrics_by_list=["රචිත", "රචනය","ලියන","ලියූ"]
genere_list =["පැරණි","ඉල්ලීම","චිත්‍රපට","ක්ලැසික්","පොප්ස්","කැලිප්සෝ","ගෝල්ඩන් ඕල්ඩීස්","යුගල","පොප්","උද්වේගකර"]
key_list =["major","minor"]
artist_list=["ගේ","ගැයූ","ගායනා කල","ගායනා කරන","ගයන","කිව්ව",]
# possetion_list=["","","",]

popular_list=["ජනප්‍රිය","හොඳම","ප්‍රසිද්ධ","ප්‍රකට","ජනප්‍රියතම","සුපිරි","ජනප්‍රියම",'සුප්‍රකට',"හොඳ"]

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
      query=[]
      is_rating_query=False
      numeric_value=0
      query_request= request.form["query"].strip().lower()
      processed_query_request=""
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
      if(any(("ගේ" in x or x in artist_list) for x in token_list)):
            boosting_list.append("artist^2")
      if(any(x in popular_list for x in token_list)):
            token_list = [i for i in token_list if i not in popular_list] 
            is_rating_query= True
      if(any(x.isnumeric() for x in token_list)):
            for x in token_list:
                  if (x.isnumeric()):
                        print(x)
                        token_list.remove(x)
                        numeric_value=int(x)

      # = [ if (lyrics_by in token_list) else "lyrics by"for lyrics_by in  lyrics_by_list][0]
      # boosting_list[4] = ["music by^3" if (music_by in token_list) else "music by"for music_by in  music_by_list][0]
      # boosting_list[5] = ["key^3" if (music_by in token_list) else "key"for music_by in  music_by_list][0]

      
      # affix=word_splitter.split(query_request)["affix"]

      processed_query_request =" ".join([word_splitter.split(item)["base"] if len(item)>5 else item for item in token_list]) 

      # result = es.search(index="lyrics", doc_type="doc",body={  "query": {"match" : { "genere": affix}}})

      boosting_list=list(dict.fromkeys(boosting_list))
      print(numeric_value)

      print(query_request) 
      print(token_list)
      print(processed_query_request)
      print(boosting_list)
      print(is_rating_query)
      if(len(processed_query_request)==0):
            query= {"query" : {
                  "match_all" :{}
             }
            }
      else:
            query= {"query" : {
                        "multi_match" : {
                              "query" : processed_query_request,
                              "fields" : boosting_list
                        }
                  }
            }
      # if(len(boosting_list)==0):
      #        boosting_list=["name", "artist","genere","lyrics by","music by","key","lyrics" ]  

      if(is_rating_query):
            query["sort"]=[{'views':'desc'}]
      if(numeric_value !=0):
            query["size"] = numeric_value


      boosted_query= es.search(index="lyrics", doc_type="doc",body=json.dumps(query))

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