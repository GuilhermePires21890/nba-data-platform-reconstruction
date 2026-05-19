REQUIRED_COLUMNS = [
    'player_name',
    'team',
    'points',
    'rebounds',
    'assists'
]


def validate_required_columns(dataframe_columns):
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in dataframe_columns
    ]

    if missing_columns:
        raise ValueError(
            f'Missing required columns: {missing_columns}'
        )

    return True
