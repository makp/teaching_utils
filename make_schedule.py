from datetime import datetime, timedelta
import os


DATE_FORMAT = '%m-%d-%y'


def list_all_dates(first, last, weekdays=[0, 2]):
    """
    Generate a list of dates between `first` and `last` that fall on
    specified `weekdays`.

    :param first: Start date as a string in 'mm-dd-yy' format.
    :param last: End date as a string in 'mm-dd-yy' format.
    :param weekdays: A list of integers representing weekdays where
    Monday is 0 and Sunday is 6.

    :return: A list of dates in 'mm-dd-yy' format.
    """
    # Convert str to datetime objects
    start_date = datetime.strptime(first, DATE_FORMAT)
    end_date = datetime.strptime(last, DATE_FORMAT)

    lst_days = []

    current_day = start_date
    while current_day <= end_date:
        if current_day.weekday() in weekdays:
            lst_days.append(current_day.strftime(DATE_FORMAT))
        current_day += timedelta(days=1)

    return lst_days


def file_name_to_export(lst, output_dir):
    """
    Generate a filename based on the first date in the list.

    :param lst: A list of dates.
    :param output_dir: The directory where the CSV file will be saved.

    :return: A string representing the filename.
    """
    first_date = datetime.strptime(lst[0], '%m-%d-%y')
    first_month = first_date.strftime('%m')
    year = first_date.strftime('%y')

    terms = {'08': 'Fall', '01': 'Spring', '02': 'Spring'}
    term = terms.get(first_month, '')

    file_name = "teachingDates" + term + year + ".csv"

    return os.path.join(output_dir, file_name)


def export_file(lst, output_dir="."):
    file_name = file_name_to_export(lst, output_dir)
    with open(file_name, 'w') as f:
        f.write(', '.join(lst))
