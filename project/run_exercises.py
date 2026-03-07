#!/usr/bin/env python3
"""Parse exercises.md, run all SQL solutions against retaildb.duckdb, save results."""

import re
import duckdb

EXERCISES_FILE = "exercises.md"
DB_FILE = "retaildb.duckdb"
OUTPUT_FILE = "project/exercise_results.md"


def parse_exercises(text: str) -> list[dict]:
    """Extract exercises with their solution SQL blocks and labels."""
    exercises = []
    # Split into exercise sections
    parts = re.split(r"(?=^### Exercise \d+:)", text, flags=re.MULTILINE)

    for part in parts:
        header = re.match(r'### Exercise (\d+): "(.*?)"', part)
        if not header:
            continue
        num, title = header.group(1), header.group(2)

        # Extract solution block
        sol_match = re.search(
            r"<details>\s*<summary>Solution</summary>(.*?)</details>",
            part,
            re.DOTALL,
        )
        if not sol_match:
            continue
        sol_text = sol_match.group(1)

        # Find all SQL blocks with their preceding labels
        queries = []
        # Split solution text into chunks around ```sql blocks
        chunks = re.split(r"(```sql\n.*?```)", sol_text, flags=re.DOTALL)

        for i, chunk in enumerate(chunks):
            if not chunk.startswith("```sql"):
                continue
            sql = chunk.removeprefix("```sql\n").removesuffix("```").strip()

            # Look backwards for a label (bold text line)
            label = None
            if i > 0:
                preceding = chunks[i - 1]
                # Find last **...** or **...:*** line
                labels = re.findall(r"\*\*(.+?)\*\*", preceding)
                if labels:
                    label = labels[-1].rstrip(":")

            queries.append({"label": label, "sql": sql})

        exercises.append({"num": num, "title": title, "queries": queries})

    return exercises


def split_statements(sql: str) -> list[str]:
    """Split a SQL block into individual statements on semicolons."""
    stmts = []
    for s in sql.split(";"):
        s = s.strip()
        # Skip empty or comment-only fragments
        if s and not all(
            line.strip().startswith("--") or not line.strip()
            for line in s.splitlines()
        ):
            stmts.append(s)
    return stmts


def format_table(columns: list[str], rows: list[tuple]) -> str:
    """Format query results as a markdown table."""
    if not columns:
        return "_No results._\n"

    # Convert all values to strings
    str_rows = []
    for row in rows:
        str_rows.append([format_value(v) for v in row])

    # Column widths
    widths = [len(c) for c in columns]
    for row in str_rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(val))

    def pad(vals, widths):
        return "| " + " | ".join(v.ljust(w) for v, w in zip(vals, widths)) + " |"

    lines = [
        pad(columns, widths),
        "|" + "|".join("-" * (w + 2) for w in widths) + "|",
    ]
    for row in str_rows:
        lines.append(pad(row, widths))
    return "\n".join(lines) + "\n"


def format_value(v) -> str:
    if v is None:
        return "NULL"
    if isinstance(v, float):
        # Avoid scientific notation, trim trailing zeros
        if v == int(v) and abs(v) < 1e15:
            return str(int(v))
        return f"{v:.4f}".rstrip("0").rstrip(".")
    return str(v)


def run_query(con, sql: str) -> tuple[list[str], list[tuple]] | None:
    """Run a single statement. Returns (columns, rows) or None."""
    try:
        result = con.execute(sql)
        if result.description:
            columns = [desc[0] for desc in result.description]
            rows = result.fetchall()
            return columns, rows
        return None
    except Exception as e:
        return ["Error"], [(str(e),)]


def main():
    with open(EXERCISES_FILE) as f:
        text = f.read()

    exercises = parse_exercises(text)
    con = duckdb.connect(DB_FILE, read_only=True)
    output_parts = ["# Exercise Results\n"]

    for ex in exercises:
        output_parts.append(f'## Exercise {ex["num"]}: "{ex["title"]}"\n')

        for q in ex["queries"]:
            if q["label"]:
                output_parts.append(f'### {q["label"]}\n')

            output_parts.append(f'```sql\n{q["sql"]}\n```\n')

            # Split and run statements
            stmts = split_statements(q["sql"])
            results = []
            for stmt in stmts:
                r = run_query(con, stmt)
                if r is not None:
                    results.append(r)

            if results:
                for columns, rows in results:
                    output_parts.append(format_table(columns, rows))
            else:
                output_parts.append("_No result set._\n")

            output_parts.append("")  # blank line separator

        output_parts.append("---\n")

    con.close()

    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(output_parts))

    print(f"Wrote {OUTPUT_FILE} with {len(exercises)} exercises.")


if __name__ == "__main__":
    main()
