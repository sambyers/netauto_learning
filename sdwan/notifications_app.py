from flask import Flask, request


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello This is the sdwan notifications app!'

@app.route('/api/notifications', methods=['POST'])
def notifications():
    data = request.get_json()
    return {"result": "Notification processed successfully"} 

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8080)