import pkg_resources

def duplicate():
    files = ['sample_diagram.py','sample_hardware_board.png', 'sample_styles.css']
    resource_package = __name__
    for filename in files:
        resource_path = '/'.join(('resources', filename))
        data = pkg_resources.resource_string(resource_package, resource_path)
        with open(filename, 'wb') as f:
            f.write(data)
        print(f'{filename} duplicated.')

        