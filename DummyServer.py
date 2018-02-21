from flask  import Flask, request, jsonify
from ast    import literal_eval

app = Flask(__name__)

@app.route('/init', methods=['GET', 'POST'])
def nodeInit():
    content = request.json
    print content['NODE_IP']
    if content['NODE_ID'] == '': content['NODE_ID'] = 'nodeX'
    print content['NODE_ID']
    
    return jsonify(content)

if __name__ == '__main__':
    app.run(debug = True)