from setuptools import setup

setup(
    name="OctoPrint-SurfaceMapper",
    version="0.1.0",
    author="Your Name",
    description="An OctoPrint plugin for surface mapping.",
    packages=["octoprint_surfacemapper"],
    entry_points={
        "octoprint.plugin": [
            "surfacemapper = octoprint_surfacemapper"
        ]
    },
    install_requires=[],
    python_requires='>=3.7',
)
