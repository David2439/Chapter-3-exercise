from numbers import Number


class Polynomial:

    def __init__(self, coefs):
        self.coefficients = coefs

    def degree(self):
        return len(self.coefficients) - 1

    def __str__(self):
        coefs = self.coefficients
        terms = []

        if coefs[0]:
            terms.append(str(coefs[0]))
        if self.degree() and coefs[1]:
            terms.append(f"{'' if coefs[1] == 1 else coefs[1]}x")

        terms += [f"{'' if c == 1 else c}x^{d}"
                  for d, c in enumerate(coefs[2:], start=2) if c]

        return " + ".join(reversed(terms)) or "0"

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.coefficients) + ")"

    def __eq__(self, other):

        return isinstance(other, Polynomial) and\
             self.coefficients == other.coefficients

    def __add__(self, other):

        if isinstance(other, Polynomial):
            common = min(self.degree(), other.degree()) + 1
            coefs = tuple(a + b for a, b in zip(self.coefficients,
                                                other.coefficients))
            coefs += self.coefficients[common:] + other.coefficients[common:]

            return Polynomial(coefs)

        elif isinstance(other, Number):
            return Polynomial((self.coefficients[0] + other,)
                              + self.coefficients[1:])

        else:
            return NotImplemented

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):

        if isinstance(other, Polynomial):
            common = min(self.degree(), other.degree()) + 1
            coefs = tuple(a - b for a, b in zip(self.coefficients, 
                                                other.coefficients))
            coefs += self.coefficients[common:]
            + tuple(-b for b in other.coefficients[common:])
            return Polynomial(coefs)

        elif isinstance(other, Number):
            return Polynomial((self.coefficients[0] - other,) 
                              + self.coefficients[1:])

        else:
            return NotImplemented

    def __rsub__(self, other):
        return other - self

    def __mul__(self, other):

        if isinstance(other, Polynomial):
            new_degree = self.degree() + other.degree()
            new_coeffs = [0] * (new_degree + 1)

            for i, a in enumerate(self.coefficients):
                for j, b in enumerate(other.coefficients):
                    new_coeffs[i + j] += a * b

            return Polynomial(new_coeffs)

        elif isinstance(other, (int, float)):
            new_coeffs = [coeff * other for coeff in self.coefficients]
            return Polynomial(new_coeffs)

        else:
            return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __power__(self, other):

        if isinstance(other, int):
            if int == 0:
                return Polynomial([1])
            else:
                result = Polynomial([1])
                for x in range(other):
                    result = result * self
                return result
        else:
            return NotImplemented

    def __call__(self, other):
        result = 0
        if isinstance(other, Number):
            for degree, coeffs in enumerate(self.coefficients):
                result += coeffs * (other ** degree)
            return result
        else:
            return NotImplemented
