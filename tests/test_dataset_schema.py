from src.validation.schema_validator import validate_required_columns


def test_required_columns_validation_success():
    columns = [
        'player_name',
        'team',
        'points',
        'rebounds',
        'assists'
    ]

    assert validate_required_columns(columns) is True
