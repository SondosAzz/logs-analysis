# -*- coding: utf-8 -*-
#!/usr/bin/env python
import datetime
import psycopg2
import sys


DBNAME = "news"

question1 = "1.What are the most popular three articles of all time?"
question2 = "2. Who are the most popular article authors of all time?"
question3 = "3. On which days did more than 1% of requests lead to errors?"


def wfile(Question, result):
    file = open("results.txt", "w")
    n = datetime.datetime.now()
    file.write(Question+"\n")
    for t in result:
        if Question == question3:
            file.write('"' + str(t[0])+'"' + " -- " + str(t[1])+" % errors \n")
        else:
            file.write('"' + str(t[0])+'"' + " -- " + str(t[1])+" views \n")

    file.write("retrieved on %s \n\n" % n)
    file.close()


def Question1():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    t = ("200 OK", '/', '/article/')
    query = """ select title, count(path) as views
    from log, articles
    where status = %s AND path != %s
    group by path, slug, title
    having path = CONCAT(%s, articles.slug)
    order by views desc limit 3"""
    c.execute(query, t)
    result = c.fetchall()
    db.close()
    wfile(question1, result)


def Question2():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    query = ("""select name , sum(views) as v
    from viewstable
    group by name
    order by v desc;""")
    c.execute(query)
    result = c.fetchall()
    db.close()
    wfile(question2, result)


def Question3():
    """3. On which days did more than 1% of requests lead to errors?"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    query = ("""select date , round(perc::numeric, 2)
    from errorperc
    where perc >= 1;
     """)
    c.execute(query)
    result = c.fetchall()
    db.close()
    wfile(question3, result)


if __name__ == '__main__':
    v = sys.version.split(" ")
    v = v[0]
    print("Python version: %s " % v)
    Question1()
    Question2()
    Question3()
    print ("Updated successfully")
