##########################################################
#
# pinout tests
#
# Use a user-defined temporary directory if
# you have problems with multiple harddrives (like I do):
#
# >>> pytest --basetemp=temp
#
##########################################################

from pinout import manager


def test_image(tmp_path):
    # This test required a manual check to ensure the
    # ouputted file matches the reference file

    dest = tmp_path / "diagram_image.svg"

    manager.export_diagram(
        "resources.diagram_image",
        dest,
        overwrite=True,
    )

    assert True


def test_export_location(tmp_path):
    dest = tmp_path / "diagram_export.svg"

    manager.export_diagram(
        "resources.diagram_export",
        dest,
        overwrite=True,
    )

    assert dest.exists()
