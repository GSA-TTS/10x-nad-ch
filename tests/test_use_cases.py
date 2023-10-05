from nad_ch.use_cases import get_greeting


def test_get_greeting():
    expected_result = "Hello!"

    actual_result = get_greeting()

    assert actual_result == expected_result
