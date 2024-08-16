from setuptools import setup

setup(name='blue_line_bot',
      version='0.1',
      description='Basic personal assistant',
      url='https://github.com/leonovvv/goit-final-project',
      author='tuaregs',
      license='MIT',
      packages=['blue_line_bot'],
      entry_points = {
        'console_scripts': ['run_bot=blue_line_bot.main:main'],
      },
      install_requires=[
        'colorama==0.4.6',
        'prettytable==3.11.0',
        'prompt_toolkit==3.0.47',
        'wcwidth==0.2.13',
      ],
      zip_safe=False)
