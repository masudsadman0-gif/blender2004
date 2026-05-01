from setuptools import setup, find_packages

setup(
    name="autonimation",
    version="0.1.0",
    description="Elite autonomous AI pipeline director and expert Python developer for the bpy API.",
    author="Autonimation",
    py_modules=["autonimation"],
    install_requires=[
        "numpy",
        "scipy"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics :: 3D Modeling",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.10",
)
