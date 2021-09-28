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
import filecmp
import pytest
import re
import shutil
import uuid
from pathlib import Path
from pinout import manager
import os


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
        # sub hrefs
        id = re.compile(r"(?<=href=\"#).+(?=\")")
        data = re.sub(id, re_sub_ids, data)
        # write modified file data to testfile
        dest.write_text(data)
    return dest


@pytest.mark.parametrize(
    "module_path, ref_path",
    [
        ("resources.diagram_image", "./resources/diagram_image.svg"),
        ("resources.diagram_export", "resources/diagram_export.svg"),
        ("..samples.clip_path.diagram", "../samples/clip_path/diagram.svg"),
    ],
)
def test_output_against_reference(tmp_path, module_path, ref_path):
    # Export a temp file in same location as reference:
    # Required for relative links to be identical.
    ref_path = Path(ref_path)

    tempsvg = ref_path.parent / "temp_" + (str(uuid.uuid4()) + ".svg")
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
