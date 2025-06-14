from flask import Flask, request
from flask_cors import CORS
import main as cj
import astar as algo
import json
import time

app = Flask(__name__)
CORS(app)


@app.route('/calculate', methods=['GET'])
def home():
    raw_input = request.args.get('pntdata').split(',')

    inputSourceLoc = (float(raw_input[0]), float(raw_input[1]))
    inputDestLoc = (float(raw_input[2]), float(raw_input[3]))

    mappedSourceLoc = cj.getKNN(inputSourceLoc)
    mappedDestLoc = cj.getKNN(inputDestLoc)

    # Start timing
    start_time = time.time()
    
    path = algo.aStar(mappedSourceLoc, mappedDestLoc)
    finalPath, cost = cj.getResponsePathDict(path, mappedSourceLoc, mappedDestLoc)
    
    # Calculate execution time
    execution_time = time.time() - start_time

    print("Length of the path(km): " + str(cost))
    print("Time taken (seconds): " + str(execution_time))
    
    # Add execution time to the response
    response = {
        "path": finalPath,
        "cost": cost,
        "execution_time": execution_time
    }
    
    return json.dumps(response)


if __name__ == "__main__":
    app.run(debug=True, port=5000)