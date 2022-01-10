# Third party imports
import os
from pymongo import MongoClient
import datetime as dt
from tabulate import tabulate

# Local application imports
if os.path.exists('settings.py'):
    from settings import mongodb_string

# Connect to MongoDB and set the database variables
client = MongoClient(mongodb_string)
db = client.supportStats
stats = db.stats


def human_date(date):
    """
    * Converts the date to a prettier, more readable date.
    * @arg(obj) date -- the date object from choose_date().
    * @return(str) human_date -- pretty date string, e.g. "Wednesday, 05 May 2021"
    """
    human_date = date.strftime('%A, %d %B %Y')
    return human_date


def choose_date():
    """
    * Asks the user which date to input/view stats for.
    * Converts input to a date object and runs human_date().
    * @return(obj) date_obj -- the date object.
    * @return(str) date_readable -- pretty date string returned from human_date().
    """
    date_str = input('Date (format: YYYY-MM-DD): ')
    date_obj = dt.datetime.strptime(date_str, '%Y-%m-%d')
    date_readable = human_date(date_obj)
    return date_obj, date_readable


def proceed(user_input):
    """
    * Handles the user input from a yes/no question.
    * @return(bool) -- True for y, False for n.
    """
    if user_input == 'y':
        return True
    elif user_input == 'n':
        return False
    elif user_input != 'y' and proceed != 'n':
        print('Incorrect input. Please type "y" or "n".')


def user_continue(arg):
    """
    * Asks the user if they'd like view or input more stats.
    * @return(bool) proceed_yes_no -- True for yes, False for no.
    """
    user_input = input(f'Would you like to {arg} more stats (y/n)? ')
    proceed_yes_no = proceed(user_input)
    return proceed_yes_no


def generate_daily_stats(date, stats_dict):
    """
    * Create a table of stats for the given date.
    * @arg(obj) date -- the date object passed from stats_daily().
    * @arg(dict) stats_dict -- the dict of stats from the database, passed from stats_daily().
    """
    key_list = ['No. of tickets advanced: ', 'No. of ticket public comments: ', 'No. of tickets solved: ',
                'Incoming ticket queue: ', 'Handoff ticket queue: ', 'Total chats: ', 'Chat wait time: ', 'Chat CSAT: ']
    # Convert the stats_dict values to a list.
    stats_list = list(stats_dict.values())
    # Remove the MongoDB ID and date from the list.
    stats_list = stats_list[2:]
    # Merge the key_list and stats_list to a list of lists to be compatible with tabulate.
    table_list = [list(x) for x in zip(key_list, stats_list)]

    # Generate header to include the date.
    title = f'Stats for {date}'
    print('-' * len(title))
    print(title)
    print('-' * len(title))

    # Print the list as a table.
    print(tabulate(table_list, tablefmt="fancy_grid"))


def generate_weekly_stats(date, key_list, stats_list):
    """
    * Create a table of stats for the given week.
    * @arg(obj) date -- the date object passed from stats_weekly().
    * @arg(list) key_list -- the list of keys from the aggregator, passed from stats_weekly().
    * @arg(list) stats_list -- the list of stats from the database, passed from stats_weekly().
    """
    # Convert the stats values to floats to help table alignment and round ratio value.
    stats_list = [float(x) for x in stats_list]
    stats_list = [round(x, 1) for x in stats_list]
    # Merge the key_list and stats_list to a list of lists to be compatible with tabulate.
    table_list = [list(x) for x in zip(key_list, stats_list)]

    # Generate header to include the date.
    title = f'Stats for week commencing {date}'
    print('-' * len(title))
    print(title)
    print('-' * len(title))

    # Print the list as a table.
    print(tabulate(table_list, tablefmt="fancy_grid", numalign="decimal"))


def stats_aggregator(start_date, end_date):
    stats = db.stats.aggregate([
        {
            # Fetch the documents between the week starting and ending dates.
            '$match': {
                'date': {
                    '$gte': start_date,
                    '$lte': end_date
                }
            }
        }, {
            # Group the data and calculate the column totals.
            '$group': {
                '_id': 'null',
                'Total tickets advanced': {
                    '$sum': '$t_advanced'
                },
                'Total ticket public comments': {
                    '$sum': '$t_pub_comments'
                },
                'Total tickets solved': {
                    '$sum': '$t_solved'
                },
                'Total chats': {
                    '$sum': '$c_total'
                },
                'Average ticket public comments per day': {
                    '$avg': '$t_pub_comments'
                },
                'Average tickets solved per day': {
                    '$avg': '$t_solved'
                },
                'Average chats per day': {
                    '$avg': '$c_total'
                },
                'Average chat wait time': {
                    '$avg': '$c_wait'
                },
                'Average chat CSAT for the week': {
                    '$avg': '$c_csat'
                }
            }
        }, {
            # Forward the totals through the pipeline and include the comments per solve ratio.
            '$project': {
                'Total tickets advanced': 1,
                'Total ticket public comments': 1,
                'Total tickets solved': 1,
                'Total chats': 1,
                'Average ticket public comments per day': 1,
                'Average tickets solved per day': 1,
                'Average chats per day': 1,
                'Average chat wait time': 1,
                'Average chat CSAT for the week': 1,
                'Average public comments per ticket solved': {
                    '$divide': [
                        '$Average ticket public comments per day', '$Average tickets solved per day'
                    ]
                }
            }
        }
    ])

    return stats