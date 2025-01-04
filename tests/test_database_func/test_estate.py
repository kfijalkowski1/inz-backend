from code.database.declarations.estate import get_all_estates, get_user_estate_info


def test_get_all_estates(mocked_session):
    estates = get_all_estates(mocked_session)
    assert len(estates) == 2
    assert estates[0].name == "Test Estate"
    assert estates[1].name == "Test Estate 2"

def test_get_user_estate_info(mocked_session):
    estate = get_user_estate_info(mocked_session, "2")
    assert estate.name == "Test Estate"
    assert estate.description == "Test Estate Description"

