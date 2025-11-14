from datetime import date, timedelta


def clean_isbn(isbn: str) -> str:
    # remove hyphens and spaces
    isbn = isbn.replace("-", "").replace(" ", "")
    return isbn


def calculate_return_date(start_date: date, return_days: int) -> date:
    # validate day if the day < 0
    if return_days < 0:
        raise ValueError("Days must be greater than 0")

    # set non working days so 5 and 6
    non_working_days = [5, 6]

    # set the needed data to get the correct return date
    days_left = return_days
    return_date = start_date
    while days_left > 0:
        return_date += timedelta(days=1)
        # check if the day is a non working day
        if return_date.weekday() in non_working_days:
            # if it is a non working day, subtract 1 day
            days_left -= 1
    return return_date
