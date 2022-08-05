from src.models.db_models import Permission

TEST_PERMISSIONS = [
    Permission(
        id='00000000-0000-0000-0000-000000000000',
        title='test_permission #1',
        created='2021-06-16T21:14:09.221999',
        modified='2021-06-16T21:14:09.221999',
    ),
    Permission(
        id='10000000-0000-0000-0000-000000000000',
        title='test_permission #2',
        created='2021-06-16T21:14:09.221999',
        modified='2021-06-16T21:14:09.221999',
    ),
    Permission(
        id='20000000-0000-0000-0000-000000000000',
        title='test_permission #3',
        created='2021-06-16T21:14:09.221999',
        modified='2021-06-16T21:14:09.221999',
    ),
]

TEST_PERMISSIONS_RESPONSE = [
    {
        'id': item.id,
        'title': item.title,
        'created': item.created,
        'modified': item.modified,
    } for item in TEST_PERMISSIONS
]
