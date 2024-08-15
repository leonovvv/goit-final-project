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
      zip_safe=False)