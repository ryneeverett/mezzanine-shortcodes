import setuptools

setuptools.setup(
    name='mezzanine-shortcodes',
    packages=setuptools.find_packages(),
    install_requires=[
        'beautifulsoup4',
        'mezzanine',
    ],
)
