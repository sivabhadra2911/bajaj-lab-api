import re

def parse_lab_tests(text):
    results = []

    pattern = re.compile(r'([A-Z0-9 ()]+)\s+([\d.]+)\s*([a-zA-Z/%]+)?\s*\(?([\d.]+)-([\d.]+)\)?')

    for match in pattern.finditer(text):
        test_name, test_value, test_unit, ref_min, ref_max = match.groups()
        test_value = float(test_value)
        ref_min = float(ref_min)
        ref_max = float(ref_max)
        out_of_range = not (ref_min <= test_value <= ref_max)

        results.append({
            "test_name": test_name.strip(),
            "test_value": f"{test_value}",
            "bio_reference_range": f"{ref_min}-{ref_max}",
            "test_unit": test_unit or "",
            "lab_test_out_of_range": out_of_range
        })

    return results
