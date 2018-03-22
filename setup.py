from distutils.core import setup
import versioneer

setup(
    # Application name:
    name="crypto-nlp",

    # Version number (initial):
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),

    # Application author details:
    author="ak",
    author_email="",

    # Packages
    packages=["crypto-nlp"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="ankoller.com",

    #
    # license="LICENSE.txt",
    description="nlp of crypto language",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "appnope==0.1.0",
        "attrs==17.4.0",
        "decorator==4.2.1",
        "python-dotenv==0.8.2",
        "ipython==6.2.1",
        "ipython-genutils==0.2.0",
        "jedi==0.11.1",
        "nltk==3.2.5",
        "parso==0.1.1",
        "pexpect==4.4.0",
        "pickleshare==0.7.4",
        "pluggy==0.6.0",
        "praw==5.3.0",
        "prompt-toolkit==1.0.15",
        "ptyprocess==0.5.2",
        "py==1.5.2",
        "Pygments==2.2.0",
        "pytest==3.4.2",
        "simplegeneric==0.8.1",
        "six==1.11.0",
        "textblob==0.15.1",
        "traitlets==4.3.2",
        "wcwidth==0.1.7",
    ],
)
