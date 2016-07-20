import setuptools

setuptools.setup(
    name='mezzanine-shortcodes',
    description=(
        "A Mezzanine package for adding buttons and menus to the richtext "
        "editor by simply decorating a python function."),
    url='https://github.com/ryneeverett/mezzanine-shortcodes',
    author='Ryne Everett',
    author_email='ryneeverett@gmail.com',
    license='BSD',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        'beautifulsoup4',
        'mezzanine',
    ],
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
)
