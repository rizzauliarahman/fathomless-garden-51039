from flask import Flask, render_template, jsonify
import mainTrain as mt
from rq import Queue
from worker import conn


app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/training')
def training():
    q = Queue(connection=conn)

    mt.retrain()
    status = 1

    return jsonify(result=status, id=622)


if __name__ == '__main__':
    app.run()
