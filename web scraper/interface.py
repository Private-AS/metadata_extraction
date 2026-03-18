import json
from flask import Flask, render_template

with open("dane2.json") as f:
    dane = json.load(f)

for i in dane[0]["Tags"].keys():
    print (dane[0]["Tags"][i], end=" ")


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", content = dane)

if __name__ == "__main__":
    app.run()