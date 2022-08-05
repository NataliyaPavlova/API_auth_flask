from src.models.db_models import Role

TEST_ROLES = [
    Role(
        id='00000000-0000-0000-0000-000000000000',
        title='test_role #1',
        created='2021-06-16T21:14:09.221999',
        modified='2021-06-16T21:14:09.221999',
    ),
    Role(
        id='10000000-0000-0000-0000-000000000000',
        title='test_role #2',
        created='2021-06-16T21:14:09.221999',
        modified='2021-06-16T21:14:09.221999',
    ),
    Role(
        id='20000000-0000-0000-0000-000000000000',
        title='test_role #3',
        created='2021-06-16T21:14:09.221999',
        modified='2021-06-16T21:14:09.221999',
    ),
]

TEST_ROLES_RESPONSE = [
    {
        'id': item.id,
        'title': item.title,
        'created': item.created,
        'modified': item.modified,
    } for item in TEST_ROLES
]
