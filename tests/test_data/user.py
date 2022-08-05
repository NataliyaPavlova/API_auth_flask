TEST_USERS = [
    {
        'id': '00000000-0000-0000-0000-000000000000',
        'login': 'test_user #1',
        'password': 'test_password',
        'created': '2021-06-16T21:14:09.221999',
        'modified': '2021-06-16T21:14:09.221999',
        'role_id': '00000000-0000-0000-0000-000000000001',
        'role_title': 'Test role #1',
    },
    {
        'id': '10000000-0000-0000-0000-000000000000',
        'login': 'test_user #2',
        'password': 'test_password',
        'created': '2021-06-16T21:14:09.221999',
        'modified': '2021-06-16T21:14:09.221999',
        'role_id': '00000000-0000-0000-0000-000000000002',
        'role_title': 'Test role #2',
    },
    {
        'id': '20000000-0000-0000-0000-000000000000',
        'login': 'test_user #3',
        'password': 'test_password',
        'created': '2021-06-16T21:14:09.221999',
        'modified': '2021-06-16T21:14:09.221999',
        'role_id': '00000000-0000-0000-0000-000000000001',
        'role_title': 'Test role #1',
    },
]

TEST_USERS_RESPONSE = [
    {
        'id': item['id'],
        'login': item['login'],
        'password': item['password'],
        'created': item['created'],
        'modified': item['modified'],
        'role_title': item['role_title'],
    } for item in TEST_USERS
]
