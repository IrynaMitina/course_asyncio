"""run it with:   % python -m pytest test_with_pytest.py """
import pytest
from unittest.mock import AsyncMock, patch
from service import get_user_name


@pytest.mark.asyncio
async def test_get_user_name():
    with patch("service.fetch_user", new_callable=AsyncMock) as mock_fetch_user:  # mock db calls
        mock_fetch_user.return_value = {"id": 1, "name": "Bob"}
        result = await get_user_name(user_id=1)
        assert result == "Bob"
        mock_fetch_user.assert_awaited_once_with(1)
