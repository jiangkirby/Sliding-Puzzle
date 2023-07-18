import datetime
import inspect

def log_error(error):
    '''
    Function: log_error
        Logs errors in text file with exact date and time
    Parameters:
        error -- exact error to append to error text file
    Does not return anything
    '''
    with open("error_log.txt", "a") as error_log:
        date = datetime.datetime.now()
        error = f"{date.strftime('%a')} {date.strftime('%b')} " + \
                f"{date.strftime('%d')} {date.strftime('%H')}:" + \
                f"{date.strftime('%M')}:{date.strftime('%S')} " + \
                f"{date.strftime('%Y')}: Error: " + error + \
                f" LOCATION: Game.{inspect.stack()[1][3]}()\n"
        error_log.write(error)
