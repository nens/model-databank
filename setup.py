from setuptools import setup

version = '0.1dev'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
])

install_requires = [
    'Django',
    'South',
    'django-extensions',
    'django-nose',
    'translations',
    'django-autoslug',
    'django-staticfiles >= 1.0',
    'factory_boy',
    'django-appconf',
    'django-crispy-forms',
    'BeautifulSoup',
],

tests_require = [
    'nose',
    'coverage',
    'mock',
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
