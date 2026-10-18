from openpyxl import Workbook

snippet_a = """Property: 14 Elm Road, Leeds, LS6 2AB
Inspection date: 03/06/2025
Wall type: Masonry cavity
Cavity width: 50mm
Insulation present: Yes
Insulation type: Blown mineral fibre
Fill: Full"""

snippet_b = """Property: Flat 2, 8 Victoria Street, York, YO1 6GF
Borescope inspection carried out at the front and rear elevations.
The cavity measured approximately 60-65mm. Polystyrene bead
insulation was observed but the fill was inconsistent, with an
estimated 40% coverage at the rear and voids visible near the
first floor joist line. Recommend top-up."""

snippet_c = """Property: 31 Mill Lane, Bradford, BD5 0HN
Drill point 1 (front, ground floor): cavity 75mm, no insulation
Drill point 2 (side, first floor): cavity 75mm, no insulation
Drill point 3 (rear, ground floor): cavity 70mm, debris present,
unable to confirm insulation
Overall: Cavity appears unfilled. CWI not present."""

# keywords for each fill status and insulation type
fill_status_words = {
    "partially_filled": ["not fully filled", "partial", "inconsistent", "void", "gaps", "top-up"],
    "fully_filled": ["fill: full", "fully filled"],
    "empty": ["no insulation", "unfilled", "cwi not present"],}

insulation_words = {
    "mineral_fibre": ["mineral fibre", "mineral wool", "rockwool"],
    "polystyrene_beads": ["polystyrene", "bead"],
    "polyurethane_foam": ["polyurethane", "foam"],}

# function tocheck words in text
def mentions(text, words):
    return any(word in text.lower() for word in words)

# function to find first option that matches
def first_match(text, options):
    for name, words in options.items():
        if mentions(text, words):
            return name
    return None

# function to get the property address
def find_address(text):
    for line in text.splitlines():
        if line.lower().startswith("property:"):
            return line.split(":", 1)[1].strip()
    return None

# function to find warnings
def find_warnings(status, text):
    warnings = []
    if status == "partially_filled":
        warnings.append("Partial fill is an estimate, needs checking")
    if status == "uncertain":
        warnings.append("No clear fill information, needs checking")
    if mentions(text, ["unable to confirm"]):
        warnings.append("Insulation could not be confirmed at some inspection points")
    return warnings

# function to parse one report
def parse_borescope(text):
    status = first_match(text, fill_status_words) or "uncertain"
    return {
        "property_address": find_address(text),
        "cavity_fill_status": status,
        "insulation_type": first_match(text, insulation_words),
        "warnings": find_warnings(status, text),}

# function to save results to excel
def save_to_excel(reports, path):
    book = Workbook()
    sheet = book.active
    sheet.append(["Report", "Property address", "Cavity fill status", "Insulation type", "Warnings"])
    for name, text in reports.items():
        r = parse_borescope(text)
        sheet.append([name, r["property_address"], r["cavity_fill_status"],
                      r["insulation_type"], ", ".join(r["warnings"])])
    book.save(path)

if __name__ == "__main__":
    path = "borescope_results.xlsx"
    save_to_excel({"A": snippet_a, "B": snippet_b, "C": snippet_c}, path)
    print(f"Saved {path}")