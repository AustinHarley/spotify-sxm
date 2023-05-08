import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='spotify-sxm',
    version='0.0.1',
    author='Austin Harley',
    author_email='austin@daviscourt.io',
    description='Testing installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/AustinHarley/spotify-sxm',
    # project_urls = {
    #     "Bug Tracker": "https://github.com/mike-huls/toolbox/issues"
    # },
    license='',
    packages=['spotify-sxm/'],
    install_requires=['spotipy','slack_sdk'],
)