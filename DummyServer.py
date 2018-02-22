from flask  import Flask, request, jsonify
from ast    import literal_eval

app = Flask(__name__)

sensorData = {
        'nodeID'    :'',
        'dataType'  :'',
        'timestamp' :'',
        'data'      :''

    }

@app.route('/init', methods=['GET', 'POST'])
def nodeInit():
    content = request.json
    if content['nodeID'] == '': content['nodeID'] = 'nodeX'
    print content['nodeID']
    return jsonify(content)

@app.route('/Temp', methods=['POST'])
def nodeTemp():
    content = request.json
    sensorData = {
        'nodeID'    :content['nodeID'],
        'dataType'  :content['dataType'],
        'timestamp' :content['timestamp'],
        'data'      :content['data']
    }
    return jsonify(sensorData), 201


if __name__ == '__main__':
    app.run(debug = True)