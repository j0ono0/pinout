##########################################################
#
# pinout tests (with coverage reporting)
#
# Use a user-defined temporary directory if
# you have problems with multiple harddrives (like I do):
#
# >>> coverage run -m pytest --basetemp=temp
#
# Build coverage html report
#
# >>> coverage html
#
##########################################################
import filecmp
import pytest
import re
import shutil
import uuid
from pathlib import Path
from pinout import manager
from pinout import config_manager


def re_sub_ids(re_m):
    id = re_m.group(0).split("_")
    id = "unique_id_replaced-for-testing_" + id[-1]
    return id


def mk_test_file(src, dest):

    shutil.copyfile(src, dest)
    with src.open() as f:
        data = f.read()
        # sub ids
        id = re.compile(r"(?<=id=\").+(?=\")")
        data = re.sub(id, re_sub_ids, data)
        # sub href anchor links
        id = re.compile(r"(?<=href=\"#).+(?=\")")
        data = re.sub(id, re_sub_ids, data)
        # sub clip-path urls
        id = re.compile(r"(?<=clip-path=\"url\(#).+(?=\")")
        data = re.sub(id, re_sub_ids, data)
        # write modified file data to testfile
        dest.write_text(data)
    return dest


@pytest.mark.parametrize(
    "module_path, ref_path",
    [
        # Components
        (
            "./resources/diagram_export.py",
            "./resources/diagram_export.svg",
        ),
        (
            "./resources/diagram_mm_units.py",
            "./resources/diagram_mm_units.svg",
        ),
        (
            "./resources/diagram_image.py",
            "./resources/diagram_image.svg",
        ),
        (
            "./resources/diagram_mm_2Columns.py",
            "./resources/diagram_mm_2Columns.svg",
        ),
        (
            "./resources/diagram_mm_2Rows.py",
            "./resources/diagram_mm_2Rows.svg",
        ),
        # Samples
        (
            "../samples/teensy_4.0/pinout_diagram.py",
            "../samples/teensy_4.0/teensy_4.0_front_pinout_diagram.svg",
        ),
        (
            "../samples/arduino/arduino/uno/arduino_uno.py",
            "../samples/arduino/pinout_arduino_uno_rev3.svg",
        ),
        (
            "../samples/arduino/arduino/rp2040/arduino_nano_rp2040_connect.py",
            "../samples/arduino/pinout_arduino_nano_rp2040_connect.svg",
        ),
        (
            "../samples/attiny85/attiny85.py",
            "../samples/attiny85/pinout_attiny85.svg",
        ),
        (
            "../samples/clip_path/pinout_diagram.py",
            "../samples/clip_path/diagram.svg",
        ),
        (
            "../samples/full_sample/pinout_diagram.py",
            "../samples/full_sample/pinout_diagram.svg",
        ),
        (
            "../samples/panel_layout/panel_layout.py",
            "../samples/panel_layout/panel_layout.svg",
        ),
        (
            "../samples/panel_layout/populated_layout.py",
            "../samples/panel_layout/populated_layout.svg",
        ),
        (
            "../samples/pci-express/pinout_x1.py",
            "../samples/pci-express/pinout_x1.svg",
        ),
        (
            "../samples/section_pullout/pinout_diagram.py",
            "../samples/section_pullout/diagram_section_pullout.svg",
        ),
    ],
)
def test_output_against_reference(tmp_path, module_path, ref_path):
    # Config requires reloading between tests to  to ensure
    # is in default state.
    config_manager.init()

    module_path = Path(module_path)
    ref_path = Path(ref_path)

    # Export a temp file in same location as reference:
    # Required for relative links to be identical.
    tempsvg = ref_path.parent / f"temp_pytest_{str(uuid.uuid4())}.svg"
    manager.export_diagram(
        module_path,
        tempsvg,
        overwrite=True,
    )

    # Create files for comparison. Unique ids are converted to match
    file1 = mk_test_file(tempsvg, tmp_path / f"test_file.svg")
    file2 = mk_test_file(ref_path, tmp_path / f"ref_file.svg")

    # Remove temp file
    tempsvg.unlink()

    # Test files are identical
    assert filecmp.cmp(file1, file2, shallow=False)
