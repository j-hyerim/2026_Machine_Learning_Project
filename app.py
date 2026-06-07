from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run")
def run_code():
    df = pd.read_csv("most_viewed_videos_1000.csv")
    print(df.head())
    
    result = "실행완료"
    return result

if __name__ == "__main__":
    app.run(debug=True, port=8080)