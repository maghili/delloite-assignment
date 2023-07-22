

from flask import Flask, request
from bucket import Bucket
import pandas as pd
import json
import psycopg2

app = Flask(__name__)


def get_gender_ids():
    query = """
    select 
        id as gender_id, 
        gender_type
    from gender;
    """
    connection = psycopg2.connect()
    cursor = connection.cursor()
    results = cursor.query(query)
    return pd.DataFrame(results.fetchall())

def process(bucket, path):
    bkt = Bucket(bucket)
    file = bkt.bucket/path
    if file.exists():
        data = pd.read_excel(file, engine='openpyxl')
    else:
        raise FileNotFoundError
    
    gender_ids = get_gender_ids()
    full_data = pd.merge(left=data, right=gender_ids, left_on="gender", right_on="gender_type")
    person = full_data[["first_name", "last_name", "gender_id", "email"]].rename({"first_name": "name", "last_name": "lastname"})
    # TODO: there can be some data cleaning based on the format of the email, and ip using regex package
    with psycopg2.connect() as connection:
        cursor = connection.cursor()
        cursor.query("create temporary table temp_table select * from person where false;")
        person.to_sql("temp_table", connection, index=False, if_exists='append')
        cursor.query("""
                     insert into person (name, lastname, email, gender_id)
                     select name, lastname, email, gender_id from temp_table
                     on conflict (email) do
                        update set name = excluded.name,
                        lastname = exluded.lastname,
                        gender_id = exluded.gender_id
                     """)
        #TODO: 1. upsert to person_ip table

        


@app.route('/', methods=["POST"])
def main():
    json_payload = request.json
    path = json_payload.get("path")
    bucket = json_payload.get("bucket")

    if not path:
        raise FileNotFoundError
    
    process(bucket, path)

    return 200, "success"



if __name__ == "__main__":
    app.run(debug=True)