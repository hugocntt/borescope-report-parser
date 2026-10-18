# Borescope Report Parser: Approach and Decisions

Reads a borescope report and finds the property address, whether the cavity is fully filled, partially filled, empty or uncertain, and the insulation type. Results are saved to Excel, one row per report.

## How to run

- pip install -r requirements.txt
- python parse_borescope.py


## Output

Each report gives: address, fill status, insulation type and warnings.

- One row per report, so many reports become one table that is easy to filter.
- Address is taken from the "Property:" line.
- Fill status is always one of four values: 'fully_filled', 'partially_filled', 'empty', 'uncertain'.
- Insulation type is one standard name: 'mineral_fibre', 'polystyrene_beads' or 'polyurethane_foam', or empty if none is mentioned.
- Warnings tell a person what to double-check.

## Decisions

- **Different wording:** each fill status and insulation type has a list of words surveyors use. New wording means adding a word to a list.
- **Order matters:** partial is checked first, so "not fully filled" or "full but with voids" count as partial.
- **Unclear reports:** if nothing matches, the status is 'uncertain' with a warning, rather than a guess.
- **Checks:** I read each snippet, decided what the right answer should be, and checked the output matched.

## Trade-offs

- Keyword matching is simple and easy to explain, but it misses things like "no voids found" or a report that contradicts itself.

## With more time

- Add automatic checks (for example a 'run_checks()' function) so every change is tested against the expected answers.
- Test on more real reports and add more wording.
- Add fields like inspection date and cavity width.
- Replace the keyword lists with an LLM, which scales better to large numbers of reports with varied wording, and use it to review any 'uncertain' results.

## Tools used

AI and Google were used as assistive tools while building this. All the decisions and code are mine, and I understand and can explain the code.