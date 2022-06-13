import argparse
import datetime
import json
import requests
import pandas as pd
from pprint import pprint
from time import sleep


url = 'https://api.pushshift.io/reddit/search/submission/'


def get_pushshift_data(after, before, sub, keyword):
   response = requests.get(url, params={
       "after": after, "before": before, "subreddit": sub, "q": keyword, "size": 500})
   response.raise_for_status()
   return response.json()


# Create ArgumentParser object to allow for CLI arguments
parser = argparse.ArgumentParser(description='Get gig-worker data from Reddit')
parser.add_argument('json_files', metavar='files', type=str,
                   nargs='+', help='the json files to be parsed')

# Parse CLI arguments into an object
args = parser.parse_args()

# Iterate over the JSON files inputted
for file in args.json_files:
   with open(file, 'r') as f:

       # Open each file and load the contents into a dictionary
       data_dict = json.load(f)
       begin_year = data_dict["beginYear"]
       begin_month = data_dict["beginMonth"]
       begin_day = data_dict["beginDay"]
       end_year = data_dict["endYear"]
       end_month = data_dict["endMonth"]
       end_day = data_dict["endDay"]

       time_start = datetime.datetime(
           begin_year, begin_month, begin_day, 0, 0).timestamp()
       time_end = datetime.datetime(
           end_year, end_month, end_day, 0, 0).timestamp()

       sub = data_dict["sub"]
       keyword = data_dict["keyword"]

       posts = get_pushshift_data(
           int(time_start), int(time_end), sub, keyword)["data"]
       entries = []

       for post in posts:
           entries.append(post)

           request_start = datetime.datetime.now()
           try:
               request = requests.get('https://api.pushshift.io/reddit/search/comment/',
                                      params={"link_id": post["id"], "sort": "score:desc", "size": 500})
               replies = request.json()["data"]
           except Exception as e:
               print("Request exception: {e}")
               replies = []

           elapsed = (datetime.datetime.now() - request_start).total_seconds()
           if elapsed < 1:
               sleep(1.01 - elapsed)

           entries.extend(replies)

       for entry in entries:
           entry["permalink"] = "https://www.reddit.com"+entry["permalink"]

       desired_columns = ["author", "title", "subreddit",
                          "num_comments", "score", "selftext", "body", "permalink"]

       whole_df = pd.DataFrame.from_records(entries)
       for column_name in desired_columns:
           if column_name not in whole_df:
               whole_df[column_name] = ""

       specific_columns_df = whole_df[desired_columns]

       file_to_save = data_dict["csvFileToSave"]
       specific_columns_df.to_csv(file_to_save)
       print(specific_columns_df)
