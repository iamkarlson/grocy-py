import pytest

from grocy.data_models.user import User


class TestUsers:
    @pytest.mark.vcr
    def test_get_user_by_id_valid(self, grocy):
        user = grocy.users.get(user_id=1)
        assert isinstance(user, User)
        assert user.id == 1
        assert user.display_name == "Demo User"
        assert user.username == "Demo User"

        user = grocy.users.get(user_id=3)
        assert isinstance(user, User)
        assert user.id == 3
        assert user.display_name == "Demo User 3"
        assert user.username == "Demo User 3"

    @pytest.mark.vcr
    def test_get_users_valid(self, grocy):
        users = grocy.users.list()

        assert len(users) == 4
        user = users[0]
        assert isinstance(user, User)
