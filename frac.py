class Frac:
    def __init__(self, numerator, denominator=1):
        self._numerator, self._denominator = _to_ratio(numerator)
        denominator = _to_ratio(denominator)
        self._denominator *= denominator[0] # (a / b) / (c / d) = ad / bc
        self._numerator *= denominator[1]
        self._simplify()

    def set_numerator(self, numerator):
        numerator = _to_ratio(numerator)
        self.numerator = numerator[0]
        self._denominator *= numerator[1]
        self._simplify()

    def set_denominator(self, denominator):
        denominator = _to_ratio(denominator)
        self._denominator = denominator[0]
        self._numerator *= denominator[1]
        self._simplify()
    
    def _simplify(self):
        if self._denominator == 0:
            if self._numerator < 0:
                self._numerator = -1
            elif self._numerator > 0:
                self._numerator = 1
            else:
                self._numerator = 0
            return
        
        if self._denominator < 0: # make numerator negative if any
            self._numerator *= -1
            self._denominator *= -1

        a = self._numerator
        b = self._denominator
        while b > 0: # euclidean algorithm to find gcd
            r = a % b
            a = b
            b = r
        self._numerator //= a # divide gcd from both
        self._denominator //= a
    
    def __hash__(self):
        return hash(float(self))
    
    def __round__(self, digits=0):
        if not isinstance(digits, int):
            raise TypeError(f'expected int but recieved {type(digits)}')
        
        if self._denominator == 0:
            if self._numerator == 0:
                return float('nan') # 0 / 0 = nan
            return float('inf') * self._numerator # 1 / 0 = inf
        
        if digits == 0:
            sign = -1 if self._numerator < 0 else 1
            numer_copy = abs(self._numerator)

            result, twice_remainder = divmod(numer_copy, self._denominator)
            twice_remainder *= 2

            if twice_remainder > self._denominator or twice_remainder == self._denominator and result % 2 == 1:
                result += 1 # round up if decimal part is > .5 or .5 and rounds up to even

            return result * sign
        if digits < 0:
            return round(self._numerator // self._denominator, digits)
        return round(self._numerator / self._denominator, digits)

    def __abs__(self):
        return Frac(abs(self._numerator), self._denominator)
    
    def __neg__(self):    
        return Frac(self._numerator * -1, self._denominator)

    def __add__(self, other):
        other = _to_ratio(other)
        if self._denominator == 0 and other[1] == 0:
            if self._numerator == 1 and other[0] == 1:
                return Frac(1, 0) # inf + inf = inf
            if self._numerator == -1 and other[0] == -1:
                return Frac(-1, 0) # -inf + -inf = -inf
        return Frac(self._numerator * other[1] + self._denominator * other[0], self._denominator * other[1]) # a / b + c / d = (ad + bc) / bd
        
    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        other = _to_ratio(other)
        if self._denominator == 0 and other[1] == 0:
            if self._numerator == 1 and other[0] == -1: # inf - -inf = inf
                return Frac(1, 0)
            if self._numerator == -1 and other[0] == 1: # -inf - inf = -inf
                return Frac(-1, 0)
        return Frac(self._numerator * other[1] - self._denominator * other[0], self._denominator * other[1]) # a / b - c / d = (ad - bc) / bd

    def __rsub__(self, other):
        return Frac(other) - self

    def __mul__(self, other):
        other = _to_ratio(other)
        return Frac(self._numerator * other[0], self._denominator * other[1]) # (a / b) * (c / d) = ac / bd
        
    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        other = _to_ratio(other)
        if self._denominator == 0 and other[0] < 0 and other[1] > 0:
            return Frac(-self._numerator, 0) # -inf/inf/nan / -a = inf/-inf/nan respectively
        return Frac(self._numerator * other[1], self._denominator * other[0]) # (a / b) / (c / d) = ad / bc
        
    def __rtruediv__(self, other):
        return Frac(other) / self
    
    def __floordiv__(self, other):
        other = _to_ratio(other)
        if self._denominator == 0:
            if self._numerator == 0 or other[1] == 0:
                return float('nan')
            if other[0] == 0:
                return float('inf') * self._numerator
            return float('inf') * self._numerator * other[0]
        if other[0] == 0:
            if self._numerator == 0 or other[1] == 0:
                return float('nan')
            return float('inf') * self._numerator
        return self._numerator * other[1] // (self._denominator * other[0])
        
    def __rfloordiv__(self, other):
        return Frac(other) // self

    def __mod__(self, other):
        other = _to_ratio(other)
        if self._denominator == 0:
            if other[0] == 0 and other[1] == 1:
                return Frac(self._numerator, 0)
            return Frac(0, 0)
        if other[1] == 0:
            if other[0] == 0:
                return Frac(0, 0)
            if other[0] < 0:
                if self._numerator < 0:
                    return Frac(self)
                if self._numerator > 0:
                    return Frac(-1, 0)
                return Frac(0)
            if self._numerator < 0:
                return Frac(1, 0)
            if self._numerator > 0:
                return Frac(self)
            return Frac(0)
        if other[0] == 0:
            return Frac(self)
        ad = self._numerator * other[1]
        bc = self._denominator * other[0]
        return Frac(ad - ad // bc * bc, self._denominator * other[1])
    
    def __rmod__(self, other):
        return Frac(other) % self

    def __pow__(self, other): # returns Frac if other is int, otherwise returns float
        if isinstance(other, int):
            if self._numerator == 0 and self._denominator == 0:
                return Frac(0, 0) # nan ** a = nan
            if other < 0:
                other *= -1
                return Frac(self._denominator ** other, self._numerator ** other) # (a / b) ** -x = (b / a) ** x
            return Frac(self._numerator ** other, self._denominator ** other)
        
        other = _to_ratio(other)
        if self._numerator == 0 and self._denominator == 1 and other[0] < 0:
            return float('inf') # 0 ** -a = (1 / 0) ** a = inf
        
        if other[1] == 0:
            if other[0] < 0:
                second = float('-inf')
            elif other[0] > 0:
                second = float('inf')
            return float('nan')
        else:
            second = other[0] / other[1]

        return float(self) ** second
    
    def __rpow__(self, other):
        return Frac(other) ** self

    def __lt__(self, other):
        other = _to_ratio(other)
        return self._denominator == 0 and self._numerator == -1 and other[1] == 0 and other[0] == 1 or self._numerator * other[1] < self._denominator * other[0] # -inf < inf or ad < bc
        
    def __gt__(self, other):
        other = _to_ratio(other)
        return self._denominator == 0 and self._numerator == 1 and other[1] == 0 and other[0] == -1 or self._numerator * other[1] > self._denominator * other[0] # inf > -inf or ad > bc

    def __le__(self, other):
        other = _to_ratio(other)
        return (self._numerator != 0 or self._denominator > 0) and (other[0] != 0 or other[1] > 0) and (self._denominator > 0 or other[1] > 0 or self._numerator != 1 or other[0] != -1) and self._numerator * other[1] <= self._denominator * other[0] # self is not nan, other is not nan, not inf <= -inf, and ad <= bc

    def __ge__(self, other):
        other = _to_ratio(other)
        return (self._numerator != 0 or self._denominator > 0) and (other[0] != 0 or other[1] > 0) and (self._denominator > 0 or other[1] > 0 or self._numerator != -1 or other[0] != 1) and self._numerator * other[1] >= self._denominator * other[0] # self is not nan, other is not nan, not -inf >= inf, and ad >= bc

    def __eq__(self, other):
        other = _to_ratio(other)
        return self._numerator == other[0] and self._denominator == other[1] and (self._numerator != 0 or self._denominator > 0) # numerators equal, denominators equal, and not nan

    def floor(self):
        if self._denominator == 0:
            if self._numerator == 0:
                return float('nan')
            return float('inf') * self._numerator
        return self._numerator // self._denominator
    
    def ceil(self):
        return self.floor() + (self._denominator > 1) # add 1 to floor if not int
    
    def is_int(self):
        return self._denominator == 1 # int will be x / 1
    
    def is_undefined(self):
        return self._denominator == 0 # -inf, inf, or nan are x / 0
    
    def is_infinite(self):
        return self._denominator == 0 and self._numerator != 0 # -inf, inf, and not nan
    
    def sign(self):
        if self._numerator < 0:
            return -1
        if self._numerator > 0:
            return 1
        return 0
    
    def to_decimal_string(self, after_decimal=17): # returns string containing exact decimal of fraction up to after_decimal digits after decimal
        if not isinstance(after_decimal, int):
            raise TypeError(f'expected int but recieved {type(after_decimal)}')

        if self._numerator < 0:
            sign = '-'
            numer = -self._numerator
        else:
            sign = ''
            numer = self._numerator

        int_part, remainder = divmod(numer, self._denominator)

        if remainder == 0 or after_decimal <= 0:
            return sign + str(int_part)

        digits = ''
        for _ in range(after_decimal):
            remainder *= 10
            digit = remainder // self._denominator
            digits += str(digit)
            remainder %= self._denominator
            if remainder == 0:
                break

        return sign + str(int_part) + "." + digits

    def __int__(self):
        return self._numerator // self._denominator

    def __float__(self):
        if self._denominator == 0:
            if self._numerator == 0:
                return float('nan')
            return float('inf') * self._numerator
        return self._numerator / self._denominator
    
    def __bool__(self):
        return self._numerator != 0 or self._denominator == 0 # not 0
    
    def __iter__(self):
        return iter([self._numerator, self._denominator])

    def __str__(self):
        return f'{self._numerator} / {self._denominator}'

    def __repr__(self):
        return f'Frac({self._numerator}, {self._denominator})'
    
def _to_ratio(input): # turns input into unsimplified ratio
    inputType = type(input)
    if inputType is int:
        return input, 1
    if inputType is float:
        if input == float('inf'):
            return 1, 0
        if input == float('-inf'):
            return -1, 0
        if input == float('nan'):
            return 0, 0
        
        return input.as_integer_ratio()
    if inputType is str:
        input = input.lower()
        if input == 'inf' or input == 'infinity':
            return 1, 0
        if input == '-inf' or input == '-infinity':
            return -1, 0
        if input == 'nan' or input == '-nan':
            return 0, 0
        
        sign = 1
        if input[0] == '-':
            sign = -1
            input = input[1:]
        elif input[0] == '+':
            input = input[1:]

        if 'e' in input:
            base, exp = input.split('e')
            exp = int(exp)
        else:
            base = input
            exp = 0

        if base == '':
            base = '1'

        if '.' in base:
            int_part, frac_part = base.split('.')
        else:
            int_part = base
            frac_part = ''

        if int_part == '':
            int_part = '0'

        numerator = int(int_part + frac_part)
        denominator = 10 ** len(frac_part)

        if exp > 0:
            numerator *= 10 ** exp
        else:
            denominator *= 10 ** -exp

        return numerator * sign, denominator
    if inputType is Frac:
        return input._numerator, input._denominator
    raise TypeError(f'expected int, float, str, Frac, list, or tuple but received {inputType}')

s = set()
s.add(1.0)
s.add(1)
s.add(Frac(1, 1) + "0.12543154325435")
print(s)