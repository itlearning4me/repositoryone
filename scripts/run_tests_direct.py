"""Direct test runner for the calculator (bypasses pytest)."""
import sys
import os
import math

# Ensure project root is on sys.path so `projectone` package can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from projectone.calculator import evaluate_expression, format_result


def approx_equal(a, b, rel=1e-9, abs_tol=0.0):
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_tol)


def run():
    tests = [
        ("1e3", 1000.0),
        ("1.23e3", 1230.0),
        ("2^10", 1024.0),
        ("2**8", 256.0),
        ("sin(pi/2)", 1.0),
        ("log(e)", 1.0),
        ("1e-3 * 5", 0.005),
    ]

    failed = 0
    for expr, expected in tests:
        try:
            got = evaluate_expression(expr)
        except Exception as e:
            print(f"FAIL: {expr} -> raised {e}")
            failed += 1
            continue

        if not approx_equal(got, expected):
            print(f"FAIL: {expr} expected={expected!r} got={got!r}")
            failed += 1
        else:
            print(f"OK:   {expr} -> {got}")

    # test format_result produces strings and scientific contains 'e'
    fr = format_result(12345.0)
    if "e" not in fr.get("scientific", ""):
        print("FAIL: format_result scientific missing 'e'")
        failed += 1

    # test invalid expression
    try:
        evaluate_expression("import os; os.system('rm -rf /')")
    except ValueError:
        print("OK:   invalid expression raised ValueError")
    except Exception as e:
        print(f"FAIL: invalid expression raised unexpected {e}")
        failed += 1
    else:
        print("FAIL: invalid expression did not raise")
        failed += 1

    if failed:
        print(f"\n{failed} tests failed")
        return 2
    print("\nAll tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(run())
