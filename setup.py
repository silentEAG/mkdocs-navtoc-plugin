from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='mkdocs-navtoc-plugin',
    version='0.0.1',
    author='SilentE',
    description='Generates a navigation for pages',
    long_description=long_description,
    url='https://github.com/silentEAG/mkdocs-navtoc-plugin',
    license='MIT',
    python_requires='>=3.5',
    install_requires=[
        'mkdocs>=1'
    ],
    entry_points={
        'mkdocs.plugins': [
            'navtoc = plugin:NavTocPlugin'
        ]
    },
    include_package_data=True,
    package_data={
        'plugin': [
            'templates/*.html',
            'css/*.css'
        ]
    }
)