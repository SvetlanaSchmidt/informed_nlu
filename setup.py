from setuptools import setup, find_packages

setup(
    name="informed_nlu",
    version="0.1",
    author="Maren Pielka",
    packages=find_packages(),
    install_requires=[
        "datasets",
        #"fluidml",  # install from source (branch run-info-access)
        "pytorch-lightning",
        "pyarrow==6.0.1",
        "pyyaml",
        "scikit-learn",
        "tiktoken",
        "torch>=1.8.1",  # old: 1.7.0
        "tqdm",
        "transformers",
        "wandb",
        "tensorboard",
        "pandas",
        "openai",
        "openpyxl",
        "metadict",
        "numpy",
        "rich",
        "markdown",
        "requests",
    ],
    extras_require={"jupyter": ["jupyterlab", "jupyter_contrib_nbextensions"]},
)
