
import datetime

def get_pushshift_data(after, before, sub, keyword):
  url = 'https://api.pushshift.io/reddit/search/submission/?&after='+str(after)+'&before='+str(before)+'&subreddit='+str(sub)+'&q='+str(keyword)

  print(url)
  return(url)

beginYear = input("What year do you want to begin searching reddit from?: ")
beginMonth = input("What month of that year? (In number - 12): ")
beginDay = input("And day?: ")
endYear = input("Now for the end year of your time search?: ")
endMonth = input("Ending month?: ")
endDay = input("Finally, the last day of your searching time?: ")

beginYear = int(beginYear)
beginMonth = int(beginMonth)
beginDay = int(beginDay)
endYear = int(endYear)
endMonth = int(endMonth)
endDay = int(endDay)

timeStart = datetime.datetime(beginYear, beginMonth, beginDay, 0, 0).timestamp()
timeEnd = datetime.datetime(endYear, endMonth, endDay, 0, 0).timestamp()

timeStart = int(timeStart)
timeEnd = int(timeEnd)

sub = input("What subreddit would you like to seach in?: ")
keyword = input("What keyword are you searching for?: ")

get_pushshift_data(timeStart, timeEnd, sub, keyword)
