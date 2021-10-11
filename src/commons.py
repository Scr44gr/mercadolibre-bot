

def get_maximum_rows(sheet_object):
    """Temporal fix to row count in openpyxl

    [Source](https://stackoverflow.com/questions/46569496/openpyxl-max-row-and-max-column-wrongly-reports-a-larger-figure)

    """
    rows = 0
    for _, row in enumerate(sheet_object, 1):
        if not all(col.value is None for col in row):
            rows += 1
    return rows