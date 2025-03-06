from setuptools import setup

setup(
    name="hfetch",
    version="1.0.0",
    py_modules=["hfetch"],
    install_requires=[
        "colorama>=0.4.6",
        "psutil>=5.9.0",
        "distro>=1.8.0; platform_system=='Linux'",
        "GPUtil>=1.4.0; platform_system=='Windows'"
    ],
    entry_points={
        'console_scripts': [
            'hfetch=hfetch:main',
        ],
    },
    author="hteam",
    description="A system information display tool inspired by neofetch",
    python_requires=">=3.6"
)
