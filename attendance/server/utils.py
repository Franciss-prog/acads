from datetime import date, timedelta


def clean_isbn(isbn: str) -> str:
    # remove hyphens and spaces
    isbn = isbn.replace("-", "").replace(" ", "")
    return isbn


def calculate_return_date(start_date: date, return_days: int) -> date:
    # Validate input
    if return_days < 0:
        raise ValueError("Days must be greater than 0")

    # Weekend days: 5 = Saturday, 6 = Sunday
    non_working_days = [5, 6]

    days_added = 0
    return_date = start_date

    while days_added < return_days:
        return_date += timedelta(days=1)

        # Only count this day if it's NOT a weekend
        if return_date.weekday() not in non_working_days:
            days_added += 1

    return return_date
