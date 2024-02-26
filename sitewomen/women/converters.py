class FourDigitYearConverter:
    regex = "[0-9]{4}"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return "%04d" % value

x = FourDigitYearConverter()
print(type(x.to_python(2020)))
print(type(x.to_url(2020)))
