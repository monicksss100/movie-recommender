from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

app = Flask(__name__)

# Load API key safely
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_movie_recommendations(movie_name):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful movie recommendation assistant."},
            {"role": "user", "content": f"Recommend 5 movies similar to {movie_name}, just list the titles."}
        ],
        max_tokens=200
    )
    recommendations = response["choices"][0]["message"]["content"].strip().split("\n")
    return [rec.strip("-•1234567890. ") for rec in recommendations if rec.strip()]

@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = []
    if request.method == "POST":
        movie_name = request.form["movie"]
        recommendations = get_movie_recommendations(movie_name)
    return render_template("index.html", recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)
