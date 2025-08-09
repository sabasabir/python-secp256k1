class Point:
    def __init__(self, x, y, curve):
        self.curve = curve
        self.x = x
        self.y = y

    def __eq__(self, other):  # Equality check with point-at-infinity handling
        if self.is_at_infinity() and other.is_at_infinity():
            return True
        return self.x == other.x and self.y == other.y and self.curve == other.curve

    def double(self):  # Point doubling
        s = self.curve.tangent_slope(self)
        x = (s**2 - 2 * self.x) % self.curve.p
        y = (s * (self.x - x) - self.y) % self.curve.p
        return Point(x, y, self.curve)

    def __add__(self, other):  # EC point addition rules
        if self.is_at_infinity():
            return other
        if other.is_at_infinity():
            return self
        if self == other:
            return self.double()
        if self.x == other.x and (self.y + other.y) % self.curve.p == 0:
            return Point(None, None, self.curve)  # infinity
        s = (
            (other.y - self.y) * pow(other.x - self.x, -1, self.curve.p)
        ) % self.curve.p
        x_r = (s**2 - self.x - other.x) % self.curve.p
        y_r = (s * (self.x - x_r) - self.y) % self.curve.p
        return Point(x_r, y_r, self.curve)

    def __rmul__(self, n):  # Scalar multiplication (double-and-add)
        result = Point(None, None, self.curve)  # infinity
        addend = self
        if n < 0:
            raise ValueError("Scalar must be non-negative")
        while n > 0:
            if n & 1:
                result = result + addend
            addend = addend.double()
            n >>= 1
        return result

    def __repr__(self):
        return (
            "Point(infinity)" if self.is_at_infinity() else f"Point({self.x}, {self.y})"
        )

    def is_at_infinity(self):  # Special null point
        return self.x is None and self.y is None


class Curve:
    def __init__(self, a, b, p, n, h, Gx, Gy, name):
        self.a, self.b, self.p, self.n, self.h, self.name = a, b, p, n, h, name
        self.G = Point(Gx, Gy, self)
        if not self.is_on_curve(self.G):
            raise ValueError("Generator point not on curve")
        self.discriminant = 4 * self.a**3 + 27 * self.b**2
        if self.discriminant == 0:
            raise ValueError("Invalid curve, discriminant is zero")

    def is_on_curve(self, point):  # y² = x³ + ax + b
        if point.is_at_infinity():
            return True
        return (point.y**2) % self.p == (
            point.x**3 + self.a * point.x + self.b
        ) % self.p

    def tangent_slope(self, point):  # slope for point doubling
        numerator = (3 * point.x**2 + self.a) % self.p
        denominator = (2 * point.y) % self.p
        return (numerator * pow(denominator, -1, self.p)) % self.p
