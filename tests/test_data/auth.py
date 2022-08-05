from src.models.db_models import User

TESTUSER = User(
 id='32dea17d-7b0c-4639-8c4e-e4be818e8aaf',
 login='existing_user',
 password='$2b$12$drtHEL5.JqF6qd.mftDMjuBaaEAmB611L1DzBis5CeeMAYqiUcTd6', # password
 # role_id='7c57fc66-f431-4dd6-a8e8-67e3da20cd7c'
)

NEWUSER = User(
 id='32dea17d-7b0c-4639-8c4e-e4be818e8aaf',
 login='new_user',
 password='not_important',
 # role_id='7c57fc66-f431-4dd6-a8e8-67e3da20cd7c'
)



