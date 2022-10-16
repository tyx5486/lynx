from flask import Flask, render_template, request
from config.secret import host_args
import pandas as pd
import mysql.connector
from waitress import serve

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", page_text="Welcome!")


@app.route("/query", methods=['GET', 'POST'])
def query():

    # get header, connect to database and run query
    query = request.headers.get("query")
    conn = mysql.connector.connect(**host_args)
    df = pd.read_sql(query, conn)

    # decoding any columns where type is bytearray
    for col in df.select_dtypes([object]).columns:
        df[col] = df[col].where(df[col].apply(type) == bytes, df[col].str.decode('utf-8'))

    data = df.to_dict()

    conn.close()

    return data, 200


@app.route("/most_outdated", methods=['GET', 'POST'])
def most_outdated():

    # get argument and connect to database
    category = request.args.get("category")  # ?category=
    conn = mysql.connector.connect(**host_args)

    # search the wiki_most_outdated_top_ten first, returns a result if category is top ten category
    query_top_ten = f"""   
    SELECT * 
    FROM wiki_info 
    WHERE page_id = (
        SELECT most_outdated_page 
        FROM wiki_most_outdated_top_ten 
        WHERE page_category = '{category}'
    )
    AND category = '{category}'
    ;"""
    df_top_ten = pd.read_sql(query_top_ten, conn)

    # if above query returns a result implies category is top ten category
    if len(df_top_ten) > 0:
        template = render_template(
            "table.html",
            tables=[df_top_ten.T.to_html()],
            titles=df_top_ten.columns.values,
            page_text=f"Most Oudated Page for top ten category: {category}",
        )

    # when category is top ten category, compute the results on the fly instead
    else:
        query_other = f"""  
        SELECT * 
        FROM wiki_info 
        WHERE page_id = (
            SELECT DISTINCT FIRST_VALUE(page_id) OVER (PARTITION BY page_category ORDER BY page_outdated_duration DESC)
            FROM wiki_page_links
            WHERE page_category = '{category}'
        )
        AND category = '{category}'
        ;"""
        df_other = pd.read_sql(query_other, conn)

        # if query returns a result, the category exists
        if len(df_other) > 0:
            template = render_template(
                "table.html",
                tables=[df_other.T.to_html()],
                titles=df_other.columns.values,
                page_text=f"Most Oudated Page for category: {category}",
            )

        # the category does not exists
        else:
            template = render_template("index.html", page_text="Category not found.")

    conn.close()

    return template


if __name__ == "__main__":
    # use waitress which is a production-quality pure-Python WSGI server
    serve(app, host='0.0.0.0', port=5000)
