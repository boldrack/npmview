import pytest
from npmview import request_metadata, NpmData, Npm404Exception


def test_existent_package():
    metadata = request_metadata('tiny-tarball')
    assert metadata is not None

def test_nonexistent_package():
    with pytest.raises(Npm404Exception):
        request_metadata('randompackagethatdontexist')




