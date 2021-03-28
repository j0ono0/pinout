import pkg_resources

def duplicate(resource_name='get started'):
    """pinout includes some sample projects. These can be duplicated to the working directory and used in conjunction with the official tutorial.

    Current projects:

        + 'get started'
        + 'full sample'

    :param resource_name: Name of sample project. Defaults to 'get started'.
    :type resource_name: string
    """

    resources = {
        'get started': [
            'get_started/sample_diagram.py',
            'get_started/sample_hardware_board.png',
            'get_started/sample_styles.css'
        ],
        'full sample':[
            'sample_full/sample_full_pinout.py',
            'sample_full/sample_full_pinout_hardware.png',
            'sample_full/sample_full_pinout_styles.css'
        ]
    }

    files = ['sample_diagram.py','sample_hardware_board.png', 'sample_styles.css']
    resource_package = __name__
    for filename in resources[resource_name]:
        resource_path = '/'.join(('resources', filename))
        data = pkg_resources.resource_string(resource_package, resource_path)
        with open(filename, 'wb') as f:
            f.write(data)
        print(f'{filename} duplicated.')

        