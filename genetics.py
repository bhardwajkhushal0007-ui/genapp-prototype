MARKERS = ["D3S1358","vWA","FGA","D8S1179","D21S11","TH01","TPOX","CSF1PO"]

def validate_profile(profile):
    for marker in MARKERS:
        if marker not in profile: return False, f"Missing marker: {marker}"
        a,b = profile[marker]
        if not a or not b: return False, f"Enter both alleles for {marker}."
        try: float(a); float(b)
        except ValueError: return False, f"Alleles for {marker} must be numeric."
    return True, "OK"

def compare_profiles(unknown, reference):
    compared = matched = 0
    for marker in MARKERS:
        compared += 1
        if set(unknown[marker]) & set(reference[marker]): matched += 1
    score = round(100 * matched / compared, 2) if compared else 0
    return score, matched, compared
