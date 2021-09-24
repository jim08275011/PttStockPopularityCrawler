import requests
import lxml
import sqlite3
import twstock
import localDb
from bs4 import BeautifulSoup
from datetime import date


def get_comment_content(url,date):
    result = []
    stock_page = requests.get(url)
    stock_soup = BeautifulSoup(stock_page.content,"html.parser")
    article = stock_soup.find_all(lambda tag: tag.name == "a" and date in tag.text)

    if(len(article) == 0):
        raise Exception("The crawler cannot find the article based on the date {0}".format(date))

    art_URL = "https://www.ptt.cc/" + article[0]['href']
    art_page = requests.get(art_URL)
    art_soup = BeautifulSoup(art_page.content,"html.parser")
    result = art_soup.findAll("span", {"class": "f3 push-content"})
    return result

def get_matching_comments(comments_list):
    result = dict()
    if(len(comments_list) ==0):
        raise Exception("The input of the function is null or empty.")

    stocks_list =[ v.name for k,v in twstock.twse.items()]
    for stock in stocks_list:
        matching = [comment.text.replace(": ","") for comment in comments_list if stock in comment.text]
        if len(matching) != 0:
            result[stock] = matching
    return result


def main():
    try:
        url = "https://www.ptt.cc/bbs/Stock/index.html"
        today = date.today().strftime("%Y/%m/%d")
        comments_list = get_comment_content(url,today)
        # stock_comment = stock:[comment1,comment2...]
        stock_comments = get_matching_comments(comments_list)
        db = localDb.sqliteDb("C:\\db\\mydb.db")
        for stock,comments in stock_comments.items():
            table_name = '{0}-{1}'.format(today,stock)
            # Record the table name in the main table TWStock 
            db.insert(table_name,"TW_Stock","table_name")
            # Create the stock table
            db.create_stock_table(table_name)
            # Insert the acquired comments into its stock table
            db.insert(comments,table_name,"comment")
        db.commit()
        db.close()
    except Exception as ex:
        print("There is error in the code. Error msg={0}".format(ex))



if __name__=='__main__':
    main()



