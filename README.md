# Logs Analysis

## About 
this is project is a part of the Udacity Full Stack Web Developer Nanodegree Program. The project will interact with the database newsdata.sql and save the result into a file results.txt. code was written following on *PEP8 style guide*
results file will contain answers of the following:
* What are the most popular three articles of all time?
* Who are the most popular article authors of all time?
* On which days did more than 1% of requests lead to errors?


## To Run
In  order to run this project you need:
1.  make sure to install virtual machine such as virtual box, Vagrant, Python2 and PostgreSQL
2. Clone/download this repository 
3. download the data [newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

### The database includes three tables:

* The authors table.
* The articles table.
* The log table.

## What Is Next?
1. cd to the directory and run ```vagrant up``` and ```vagrant ssh```
2. load the data by running ```psql -d news -f newsdata.sql``` in the command line
3. run the newsdb.py in the commandline using ```python newsdb.py```
4. Python version will be printed in the command line and resutls.txt file will be updated. 

## Views Used
* sqltest view
```sql
CREATE VIEW sqltest
    as
    select name,count(path) as views
    from authors, articles, log
    where articles.author = authors.id and status = '200 OK' and path != '/'
    group by  articles.author, authors.id, path, slug, authors.name
    having path = CONCAT('/article/', articles.slug)
    order by views desc;
  ```  
* OKtable view
```sql
CREATE VIEW OKtable
as
select  count(status) as Cok, to_char(log.time, 'Month,DD YYYY') as date
from log
where status ='200 OK'
group by date
order by date;
  ``` 
* errortable view
```sql
CREATE VIEW errortable
as
select  count(status) as Cerror, to_char(log.time, 'Month,DD YYYY') as date
from log
where status !='200 OK'
group by date
order by date;
  ```  
 * errorperc view
```sql
CREATE VIEW errorperc
as
select  oktable.date , Cerror /(Cerror + cok):: double precision* 100.0 as perc
from oktable ,errortable
where oktable.date = errortable.date;
  ```   
    

