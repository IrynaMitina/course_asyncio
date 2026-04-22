"""run it with:   % python -m unittest test_with_unittest.py"""
import unittest
from unittest.mock import AsyncMock, patch
from service import get_user_name


class TestGetUser(unittest.IsolatedAsyncioTestCase):
    async def test_get_user_name(self):
        # mock db calls with AsyncMock
        with patch("service.fetch_user", new_callable=AsyncMock) as mock_fetch_user:
            mock_fetch_user.return_value = {"id": 1, "name": "Bob"}
            result = await get_user_name(user_id=1)
            self.assertEqual(result, "Bob")
            mock_fetch_user.assert_awaited_once_with(1)
