# Frac
### Python class for infinite precision fractions
Advantages of using this class include support for infinities and nan, ease of conversion between data types, and no usage of other libraries  

To use, add frac.py to the same folder as your project and add this line to the top of your file:  
from frac import Frac

### Description
An instance of this class holds 2 integers, representing a numerator and denominator. These numbers contain the value of the fraction including these special cases:  
1 / 0 = infinity  
-1 / 0 = -infinity  
0 / 0 = nan

The class defines all operators and conversions, as well as several extra functions to assist your projects. Frac instances work with types int, float, str, list and tuple of size 2, and another Frac.