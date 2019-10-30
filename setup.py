from setuptools import setup

version = '0.19'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
])

install_requires = [
    'BeautifulSoup',
    'Django',
    'django-extensions',
    'django-nose',
    'translations',
    'django-appconf',
    'django-autoslug',
    'django-braces',
    'django-crispy-forms',
    'djangorestframework',
    'factory_boy',
    'lizard-auth-client',
    'mercurial',
    'six',
    'requests',
    'chardet',
    'certifi',
    'transifex-client',
],

tests_require = [
    'nose',
    'coverage',
    'mock',
    'factory_boy',
]

setup(name='model-databank',
      version=version,
      description=("Model databank is used for holding reference information "
          "about water management models, versions and variants."),
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Programming Language :: Python',
                   'Framework :: Django',
                   ],
      keywords=[],
      author='Sander Smits',
      author_email='sander.smits@nelen-schuurmans.nl',
      url='',
      license='GPL',
      packages=['model_databank'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'test': tests_require},
      entry_points={
          'console_scripts': [
          ]},
      )
