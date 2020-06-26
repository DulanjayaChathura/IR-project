from flask import Flask, redirect, url_for, request,render_template
app = Flask(__name__)

# @app.route('/success/<name>')
# def success(name):
#    return 'welcome %s' % name

# @app.route('/search',methods = ['POST', 'GET'])

@app.route('/',methods = ['GET'])
def main():
      return render_template('ui.html', result = dict)

@app.route('/',methods = ['POST'])
def search():
   if request.method == 'GET':
      query = request.form['query']
      return redirect(url_for('/',search_result = search_result))

#    else:
#       user = request.args.get('nm')
#       return redirect(url_for('success',name = user))

if __name__ == '__main__':
   app.run(debug = True)