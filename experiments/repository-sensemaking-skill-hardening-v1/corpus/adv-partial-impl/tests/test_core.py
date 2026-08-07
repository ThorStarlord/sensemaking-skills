import pytest

def test_generate_report():
    from core import generate_report
    with pytest.raises(NotImplementedError):
        generate_report('x')
