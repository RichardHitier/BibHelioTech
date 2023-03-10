#
# Various tests to check configuration and pytest fixtures
#
from bht_config import yml_settings
from web.models import Paper


def test_configuration(app):
    """
    GIVEN the flask app create pattern
    WHEN an instance is created
    THEN check configuration
    """
    assert "resources-tests" in app.config["BHT_RESOURCES_DIR"]


def test_paper_for_test(paper_for_test):
    """
    GIVEN the Paper class
    WHEN an instance is created
    THEN check attributes
    """
    assert type(paper_for_test) is Paper
    assert paper_for_test.has_cat
    assert paper_for_test.has_pdf
    assert not paper_for_test.cat_in_db
    assert "105194angeo282332010_bibheliotech_V1.txt" in paper_for_test.cat_path


def test_yml_configuration():
    """
    GIVEN a yml config file
    WHEN some parameter is read
    THEN check it returns awaited value
    """
    assert "DATA/Paper" in yml_settings["BHT_PAPERS_DIR"]
