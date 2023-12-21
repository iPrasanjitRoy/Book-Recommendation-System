from flask import Flask, render_template, request
import pickle
import numpy as np

popular_df = pickle.load(open("popular.pkl", "rb"))
pt = pickle.load(open("pt.pkl", "rb"))
books = pickle.load(open("books.pkl", "rb"))
similarity_scores = pickle.load(open("similarity_scores.pkl", "rb"))

app = Flask(__name__)


@app.route("/")
def index():
    return render_template(
        "index.html",
        book_name=list(popular_df["Book-Title"].values),
        author=list(popular_df["Book-Author"].values),
        image=list(popular_df["Image-URL-M"].values),
        votes=list(popular_df["num_ratings"].values),
        rating=list(popular_df["avg_rating"].values),
    )


@app.route("/recommend")
def recommend_ui():
    book_names = [book_title.title() for book_title in pt.index]
    return render_template("recommend.html", book_names=book_names)


@app.route("/recommend_books", methods=["POST"])
def recommend():
    user_input = request.form.get("user_input")

    # Check If User Input Is In The Dataframes Index
    if user_input not in pt.index:
        # Handle The Case Where User Input Is Not Found
        return render_template("recommend.html", error_message="Book Not Found")

    index = np.where(pt.index == user_input)[0][0]

    similar_items = sorted(
        list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True
    )[1:101]

    data = []
    for i in similar_items:
        temp_df = books[books["Book-Title"] == pt.index[i[0]]]
        item = [
            temp_df["Book-Title"].values[0],
            temp_df["Book-Author"].values[0],
            temp_df["Image-URL-M"].values[0],
        ]
        data.append(item)

    return render_template("recommend.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
