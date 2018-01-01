#!/usr/bin/env python2

import psycopg2

dbName = "news"


def getTopThreeMostPopularArticles():
    conn = psycopg2.connect(database=dbName)
    cursor = conn.cursor()
    query = '''
        SELECT title, count(*) AS NumberOfViews
        FROM articles
        INNER JOIN SuccessfulllyReadArticlesView
        ON articles.slug = SuccessfulllyReadArticlesView.slug
        GROUP BY title
        ORDER BY NumberOfViews DESC
        LIMIT 3;
            '''
    cursor.execute(query)
    rows = cursor.fetchall()
    print "Top Three Most Popular Articles:"
    for row in rows:
        print "\"" + str(row[0]) + "\" - " + str(row[1]) + " views"
    print "\n"
    conn.close()


def mostPopularArticleAuthors():
    conn = psycopg2.connect(database=dbName)
    cursor = conn.cursor()
    query = '''
        SELECT authors.name,
        sum(TitleAndNumberOfViews.NumberOfViews)
        AS TotalViewPerAuthor
        FROM authors
        INNER JOIN articles
        ON authors.id = articles.author
        INNER JOIN
        (
            SELECT title, count(*) AS NumberOfViews
            FROM articles
            INNER JOIN SuccessfulllyReadArticlesView
            ON articles.slug = SuccessfulllyReadArticlesView.slug
            GROUP BY title
        ) AS TitleAndNumberOfViews
        ON articles.title = TitleAndNumberOfViews.title
        GROUP BY authors.name
        ORDER BY TotalViewPerAuthor DESC;
            '''
    cursor.execute(query)
    rows = cursor.fetchall()
    print "Most Popular Article Authors:"
    for row in rows:
        print str(row[0]) + " - " + str(row[1]) + " views"
    print "\n"
    conn.close()


def lotOfErrorsDays():
    conn = psycopg2.connect(database=dbName)
    cursor = conn.cursor()
    query = '''
        SELECT
        to_char(dateAndTotalCounts.theDate, 'Mon DD, YYYY'),
        (CAST (errorCounts AS FLOAT)/CAST(totalCounts AS FLOAT)) * 100
        AS errorPercentage
        FROM
        (
            SELECT time::timestamp::date AS theDate,
                    count(*) AS errorCounts
            FROM log
            WHERE status != '200 OK'
            GROUP BY time::timestamp::date
        ) AS dateAndErrorCounts
        INNER JOIN
        (
            SELECT time::timestamp::date AS theDate, count(*)
            AS totalCounts
            FROM log
            GROUP BY time::timestamp::date
        ) AS dateAndTotalCounts
        ON dateAndErrorCounts.theDate = dateAndTotalCounts.theDate
        WHERE
        (CAST (errorCounts AS FLOAT)/CAST(totalCounts AS FLOAT))*100 > 1
        ORDER BY
        (CAST (errorCounts AS FLOAT)/CAST(totalCounts AS FLOAT))*100 DESC,
        dateAndTotalCounts.theDate;
            '''
    cursor.execute(query)
    rows = cursor.fetchall()
    print "Days with error rate greater than 1%:"
    for row in rows:
        print str(row[0]) + " - " + str(row[1]) + "% errors"
    print "\n"
    conn.close()


getTopThreeMostPopularArticles()
mostPopularArticleAuthors()
lotOfErrorsDays()
