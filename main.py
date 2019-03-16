from flask import Flask, render_template, jsonify
import mainTrain as mt


app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/training')
def training():
    mt.main()
    status = 1

    return jsonify(result=status, id=622)


if __name__ == '__main__':
    app.run()
