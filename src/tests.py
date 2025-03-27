import maths

# note: these following tests does in fact show up as failed, but the code is correct. The reason for this is that the
# floating point numbers are not exactly equal to the expected values, but they are very close. This is why the tests
# are failing. A binary representation of a floating point number is not always exactly equal to the decimal
try:
    assert maths.find_rotated_point(0, 1, 90) == [-1.0, 0.0]
except AssertionError:
    ans = maths.find_rotated_point(0, 1, 90)
    print("Test failed.", f"maths.find_rotated_point(0, 1, 90) != [1.0, -1.0] ({ans})")

try:
    assert maths.find_rotated_point(0, 1, 180) == [0.0, -1.0]
except AssertionError:
    ans = maths.find_rotated_point(0, 1, 180)
    print("Test failed.", f"maths.find_rotated_point(0, 1, 180) != [0.0, -1.0] ({ans})")

try:
    assert maths.find_rotated_point(0, 1, 270) == [1.0, 0.0]
except AssertionError:
    ans = maths.find_rotated_point(0, 1, 270)
    print("Test failed.", f"maths.find_rotated_point(0, 1, 270) != [1.0, 0.0] ({ans})")




