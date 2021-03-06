import os

import flask
from flask import request, jsonify, Response
from waitress import serve
from app_impl import get_categories, do_search, get_surah_in_categorie

app = flask.Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))
def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)
@app.route('/Home', methods=['GET'])
def Home():
    return index()
@app.route('/Search', methods=['GET'])
def Search():
    return index()
@app.route('/Search/<s>', methods=['GET'])
def Searchs(s):
    return index()
@app.route('/home', methods=['GET'])
def home():
    print("index")
    result=get_categories()
    return jsonify(result)
@app.route('/', methods=['GET'])
def index():
    content = get_file('index.html')
    return Response(content, mimetype="text/html")
@app.route('/category', methods=['GET'])
def search_by_category():
    id=None
    try:
        id=int(request.args['id'])
    except:
        return ("invalid id "+str(request.args.get('id') )) , 404

    result = get_surah_in_categorie(id)
    return jsonify(result)
@app.route('/search', methods=['GET'])
def search():
    title = ""
    location = ""
    if 'text' in request.args:
        title = request.args['text']


    if not (title ) :
      return "search text  must be provided",404

    try:
        result = do_search(title)
        return jsonify(result)
    except Exception as e:
        return  str(e), 404

print("server ...")

if __name__ == '__main__':
    print("running server")
    app.secret_key = "i am bad"
    serve(app,listen='*:5000')
    #app.run(debug=True, host='0.0.0.0',port=4000)