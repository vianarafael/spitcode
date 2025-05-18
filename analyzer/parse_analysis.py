import json
import re
from pathlib import Path

def extract_chunks(analysis_path: str) -> list[dict]:
    raw = Path(analysis_path).read_text(encoding='utf-8')

    sections = {
        "Best Practice Violations": "best_practices",
        "Security and Performance Issues": "security",
        "Modularity and Structure Improvements": "modularity"
    }

    chunks = []
    for section_name, category in sections.items():
        pattern = rf"### \*\*{re.escape(section_name)}\*\*([\s\S]+?)(\n---|\Z)"
        match = re.search(pattern, raw)
        if not match:
            continue

        section_body = match.group(1).strip()
        entries = re.split(r"\n\d+\.\s+\*\*(.+?)\*\*", section_body)[1:]

        for i in range(0, len(entries), 2):
            title = entries[i].strip()
            block = entries[i + 1].strip()

            fix_match = re.search(r"- \*\*Fix\*\*: (.+)", block)
            impact_match = re.search(r"- \*\*Impact\*\*: (.+)", block)
            fix = fix_match.group(1).strip() if fix_match else None
            impact = impact_match.group(1).strip() if impact_match else None

            chunks.append({
                "category": category,
                "issue": title,
                "impact": impact,
                "fix": fix
            })

    # Save chunks to JSON file
    output_path = Path("outputs/review_chunks.json")
    output_path.write_text(json.dumps(chunks, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"✅ Saved {len(chunks)} review chunks to {output_path}")

    return chunks

if __name__ == "__main__":
    extract_chunks("outputs/analysis.txt")
