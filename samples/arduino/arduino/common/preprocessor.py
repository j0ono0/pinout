# An attempt to keep style/config separate from content
from copy import deepcopy
from .arduino_components import PlbStart, PlbEnd, Plb


# Generator function that applies pinlabel configurations to label data
def pinlabel_preprocessor(pinlabel_set):
    for row in pinlabel_set:

        if len(row) == 1:
            # Single label row config
            row[0] = (
                *row[0],
                {"body": Plb(width=80, height=20, x=0, y=0, corner_radius=10)},
            )
        else:
            # Default label config
            row = [
                (name, tag, {"body": Plb(width=80, height=20, x=2, y=0)})
                for (name, tag) in row
            ]

            # Row start and end labels
            row[0] = (
                row[0][0],
                row[0][1],
                {"body": PlbStart(x=0, y=0, width=80, height=20)},
            )
            row[-1] = (
                row[-1][0],
                row[-1][1],
                {"body": PlbEnd(x=2, y=0, width=80, height=20)},
            )

            # Order dependent labels
            if row[0][1] == "digital" and row[1][1] == "analog":
                row[0] = (
                    row[0][0],
                    row[0][1],
                    {"body": PlbStart(x=0, y=0, width=50, height=20)},
                )
                row[1] = (
                    row[1][0],
                    row[1][1],
                    {"body": Plb(width=30, height=20, x=0, y=0)},
                )

            # Tag specific labels
            for i, label in enumerate(row):
                name, tag = label[:2]
                if "show-leader" in tag:
                    row[i] = (
                        name,
                        tag,
                        {"body": PlbEnd(x=84, y=0, width=80, height=20)},
                    )

        yield row
