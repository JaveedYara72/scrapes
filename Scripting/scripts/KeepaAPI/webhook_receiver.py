from flask import Flask, abort, request


# setting up the app
app = Flask(__name__)


@app.route('/',methods = ['POST'])
def getWebhook():
    if request.method == 'POST':
        print("received data", request.json)
        return 'success',200
    else:
        abort(400)

if __name__ == "__main__":
    app.run()