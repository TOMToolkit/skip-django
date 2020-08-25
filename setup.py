from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='skip-django',
    description='Django Plotly Dash app for SCiMMA-Skip',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://scimma.org',
    author='SCiMMA',
    author_email='dcollom@lco.global',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics'
    ],
    keywords=['scimma', 'astronomy', 'astrophysics', 'cosmology', 'science', 'fits', 'observatory'],
    packages=find_packages(),
    use_scm_version=True,
    setup_requires=['setuptools_scm', 'wheel'],
    install_requires=[
        'django==3.1',
        'django_plotly_dash==1.4.2',
        'dash-bootstrap-components==0.10.3',
        'whitenoise==5.2.0',
        'dpd-static-support',
        'django-bootstrap4',
        'requests'
    ],
    extras_require={
    },
    include_package_data=True,
)
