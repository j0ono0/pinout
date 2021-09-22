from pinout import manager


def test_image():

    manager.export_diagram(
        "resources.diagram_image",
        "../output/diagram_image.svg",
        overwrite=True,
    )

    assert True
