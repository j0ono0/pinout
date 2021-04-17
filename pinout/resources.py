import pkg_resources


def duplicate(resource_name="quick_start"):
    """pinout includes some sample projects. These can be duplicated to the working directory and used in conjunction with the official tutorial.

    Current projects:

        + 'quick_start'
        + 'full_sample'

    :param resource_name: Name of sample project. Defaults to 'quick_start'.
    :type resource_name: string
    """

    resources = {
        "config": [("config.yaml")],
        "quick_start": [
            ("quick_start", "quick_start_config.yaml"),
            ("quick_start", "quick_start_hardware.png"),
            ("quick_start", "quick_start_pinout.py"),
            ("quick_start", "quick_start_styles.css"),
        ],
        "full_sample": [
            ("full_sample", "full_sample_config.yaml"),
            ("full_sample", "full_sample_hardware.png"),
            ("full_sample", "full_sample_pinout.py"),
            ("full_sample", "full_sample_styles.css"),
        ],
    }

    resource_package = __name__
    for path in resources[resource_name]:
        resource_path = "/".join(("resources", *path))
        data = pkg_resources.resource_string(resource_package, resource_path)
        filename = path[-1]
        with open(filename, "wb") as f:
            f.write(data)
        print(f"{filename} duplicated.")
