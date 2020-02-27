
from setuptools import setup 
  
# reading long description from file 
with open('DESCRIPTION.txt') as file: 
    long_description = file.read() 
  
  
# specify requirements of your package here 
REQUIREMENTS = ['tk', 'Pillow', 'pdf2image', 'pytesseract'] 
  
# some more details 
CLASSIFIERS = [ 
    'Development Status :: 4 - Beta', 
    'Intended Audience :: Developers', 
    'Topic :: Multimedia :: Graphics :: Capture :: Scanners',
    'Programming Language :: Python :: 3.6'  
    ] 
  
# calling the setup function  
setup(name='CropNamer', 
      version='0.0.0', 
      description='Assists with renaming scanned items', 
      long_description=long_description, 
      url='https://github.com/giwl-21/Crop-Namer', 
      author='Muhsin Wahi-Anwar', 
      author_email='muhsin.wahianwar@gmail.com',  
      packages=['source'], 
      classifiers=CLASSIFIERS, 
      install_requires=REQUIREMENTS, 
      keywords='maps location address'
      ) 
