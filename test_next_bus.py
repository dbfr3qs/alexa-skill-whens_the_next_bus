import unittest
from unittest import mock
import json
from next_bus import get_next_bus, get_hour, get_minutes

def _mock_response(
        status=200,
        content="CONTENT",
        json_data=None,
        raise_for_status=None):
    """
    since we typically test a bunch of different
    requests calls for a service, we are going to do
    a lot of mock responses, so its usually a good idea
    to have a helper function that builds these things
    """
    mock_resp = mock.Mock()
    # mock raise_for_status call w/optional error
    mock_resp.raise_for_status = mock.Mock()
    if raise_for_status:
        mock_resp.raise_for_status.side_effect = raise_for_status
    # set status code and content
    mock_resp.status_code = status
    mock_resp.content = content
    # add json data if provided
    if json_data:
        mock_resp.json = mock.Mock(
            return_value=json_data
        )
    return mock_resp

@mock.patch('requests.get')
def test_get_next_bus(mock_get):
    with open('fixture.json', 'r') as f:
        resp_json = json.load(f)
        mock_resp = _mock_response(json_data=resp_json)
        mock_get.return_value = mock_resp

        result = get_next_bus()
        assert resp_json['Services'][0] == result

        assert resp_json['Services'][0]['ExpectedDeparture'] == '2018-07-06T13:33:03+12:00'

def test_get_hour():
    with open('fixture.json', 'r') as f:
        services = json.load(f)
        d_time = services['Services'][0]['ExpectedDeparture']
        hour = get_hour(d_time)
        assert hour == 1

def test_get_minutes():
    with open('fixture.json', 'r') as f:
        services = json.load(f)
        d_time = services['Services'][0]['ExpectedDeparture']
        minutes = get_minutes(d_time)
        assert minutes == 33

        d_time = '2018-07-06T13:02:00+12:00'
        minutes = get_minutes(d_time)
        assert minutes == "oh 2"

        d_time = '2018-07-06T13:00:00+12:00'
        minutes = get_minutes(d_time)
        assert minutes == "oh clock"