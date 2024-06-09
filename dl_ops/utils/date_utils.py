from datetime import date
from datetime import datetime
from datetime import timedelta

def days_after_given_date(start_date, end_date=None, format="%m-%d-%Y"):
    """
    This function takes a start date as a string in the format 'YYYY-MM-DD' and returns a list of dates
    in the same format for each day from the start date until today (exclusive of start date).
    """
    start_date = datetime.strptime(start_date, format)
    end_date = datetime.strptime(end_date, format) if end_date else datetime.now()
    if end_date < start_date:
        return []
    
    num_days = (end_date - start_date).days
    dates = [(start_date + timedelta(days=i)).strftime(format) for i in range(1, num_days + 1)]

    return dates


def get_date_format_positions(format):
    # Initial positions
    m_pos, d_pos, y_pos, H_pos, M_pos, S_pos = [-1] * 6
    idx = 0
    for i in range(len(format) - 1):
        if format[i] == '%':
            if format[i + 1] == 'm':
                m_pos = idx
            elif format[i + 1] == 'd':
                d_pos = idx
            elif format[i + 1] == 'Y':
                y_pos = idx
            elif format[i + 1] == 'H':
                H_pos = idx
            elif format[i + 1] == 'M':
                M_pos = idx
            elif format[i + 1] == 'S':
                S_pos = idx
            
            idx += 1

    return m_pos, d_pos, y_pos, H_pos, M_pos, S_pos

def datetimefday(day:str, format='%m-%d-%Y'):
    pos = get_date_format_positions(format)
    m, d, y = pos[:3]
    date = day.split('-')
    m, d, y = [int(date[i]) for i in pos if i !=-1]

    return datetime(month=m, day=d, year=y)
    
    
def now_str():
    return datetime.now().strftime('%Y-%m-%d %H-%M-%S')



if __name__ == '__main__':
    d = datetimefday(day='04-09-2024')
    print(d)