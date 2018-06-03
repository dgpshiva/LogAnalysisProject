#!/usr/bin/env python2

import psycopg2

dbName = "news"


def execute_query(query):
    """execute_query takes an SQL query as a parameter,
        executes the query and returns the results as a list of tuples.
        args:
            query - (string) an SQL query statement to be executed.

        returns:
            A list of tuples containing the results of the query.
    """
    try:
        conn = psycopg2.connect(database=dbName)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def getTopThreeMostPopularArticles():
    """Prints to console the top three most viewed articles from the news database.
       The articles are displayed in descending order of their popularity.
    """
    query = '''
                SELECT title, views
                FROM articles
                INNER JOIN
                    (SELECT path, count(path) AS views
                    FROM log
                    GROUP BY log.path) AS log
                ON log.path = '/article/' || articles.slug
                ORDER BY views DESC
                LIMIT 3;
            '''
    rows = execute_query(query)
    print "Top Three Most Popular Articles:"
    for title, NumberOfViews in rows:
        print('{0:<35} - {1:>12} views'.format(title, NumberOfViews))
    print "\n"


def mostPopularArticleAuthors():
    """Prints to console the authors and the number of views their articles got.
       The authors are displayed in descending order of the number of views.
    """
    query = '''
                SELECT authors.name AS name,
                sum(TitleAndNumberOfViews.views)
                AS TotalViewPerAuthor
                FROM authors
                INNER JOIN articles
                ON authors.id = articles.author
                INNER JOIN
                (
                    SELECT title, views
                    FROM articles
                    INNER JOIN
                        (SELECT path, count(path) AS views
                            FROM log
                            GROUP BY log.path) AS log
                        ON log.path = '/article/' || articles.slug
                ) AS TitleAndNumberOfViews
                ON articles.title = TitleAndNumberOfViews.title
                GROUP BY authors.name
                ORDER BY TotalViewPerAuthor DESC;
            '''
    rows = execute_query(query)
    print "Most Popular Article Authors:"
    for name, TotalViewPerAuthor in rows:
        print('{0:<30} - {1:>12} views'.format(name, TotalViewPerAuthor))
    print "\n"


def lotOfErrorsDays():
    """Prints to console the days on which
       more than 1% of requests lead to errors.
    """
    query = '''
                SELECT to_char(date, 'FMMonth DD, YYYY'),
                ROUND(errorPercentage, 2)
                FROM(
                    SELECT time::date AS date,
                    100 * (COUNT(*) FILTER (WHERE status = '404 NOT FOUND') /
                    COUNT(*)::numeric) AS errorPercentage
                FROM log
                GROUP BY time::date
                    ) s
                WHERE errorPercentage > 1
                ORDER BY errorPercentage, date;
            '''
    rows = execute_query(query)
    print "Days with error rate greater than 1%:"
    for errorDate, errorPercentage in rows:
        print('{0:<30} - {1:>12} %'.format(errorDate, errorPercentage))
    print "\n"


if __name__ == '__main__':
    getTopThreeMostPopularArticles()
    mostPopularArticleAuthors()
    lotOfErrorsDays()
