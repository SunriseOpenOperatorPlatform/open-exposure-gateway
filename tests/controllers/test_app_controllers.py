import pytest

from edge_cloud_management_api.controllers.app_controllers import get_app


@pytest.mark.parametrize("app_id, x_correlator, expected", [
    (1, None, "do some magic!"),
    (2, "123", "do some magic!"),
])
def test_get_app(app_id, x_correlator, expected):
    """
    Test the get_app controller.
    """
    result = get_app(app_id, x_correlator)
    assert result == expected

