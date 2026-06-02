import os

from setuptools import find_packages, setup

package_name = 'suave_rebetmc'


def package_files(directory):
    data_files = []
    for path, dirs, files in os.walk(directory):
        dirs[:] = [directory for directory in dirs if directory != '__pycache__']
        files = [filename for filename in files if not filename.endswith('.pyc')]
        data_files.append((
            os.path.join('share', package_name, path),
            [os.path.join(path, filename) for filename in files],
        ))
    return data_files


setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ] + package_files('config') + package_files('launch') + package_files('models'),
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Gustavo Rezende',
    maintainer_email='g.rezendesilva@tudelft.nl',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
