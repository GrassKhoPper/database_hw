import sqlite3
import graphviz
import re

def visualize_sqlite_schema(db_path, output_path="schema", rows=3, cols=3):
    """Generates a visual representation of an SQLite3 database schema using Graphviz."""

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        dot = graphviz.Digraph(comment='Database Schema')

        dot.graph_attr['splines'] = 'polyline'
        dot.graph_attr['rankdir'] = 'LR'
        dot.attr(nodesep='0.3', ranksep='0.3')

        tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        tables = [t[0] for t in tables if t[0] not in ["sqlite_sequence"]]

        tables_per_row = (len(tables) + rows - 1) // rows

        for i in range(rows):
            with dot.subgraph(name=f'row_{i}') as row:
                row.attr(rank='same')  # Force tables in the same row to be on the same rank


                start_index = i * tables_per_row
                end_index = min((i + 1) * tables_per_row, len(tables)) #prevent index out of bounds



                for j, table_name in enumerate(tables[start_index:end_index]):
                    # Calculate width dynamically
                    column_count = len(cursor.execute(f"PRAGMA table_info({table_name});").fetchall())
                    width = str(max(1.0, 0.7 + column_count * 0.2))


                    row.node(table_name, shape='plaintext', label=create_table_label(cursor, table_name),
                             width=width, height='0.75')

                    # Create invisible edges for horizontal ordering within the row
                    if j < end_index - start_index - 1:

                        row.edge(tables[start_index + j], tables[start_index + j + 1], style="invis")



            # Create invisible edges between the first table of each row for vertical alignment
            if i < rows - 1:

                dot.edge(tables[i * tables_per_row], tables[min((i+1)*tables_per_row, len(tables))], style="invis") #min for last row




            # Add Foreign Key Edges (unchanged)
            for table_name in tables[start_index:end_index]: # create edges for all tables
                create_stmt = cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'").fetchone()[0]

                foreign_keys = extract_fks_from_create(create_stmt, table_name)

                for parent_table, child_col, parent_col in foreign_keys:
                    if parent_table in tables:
                        try:
                            dot.edge(table_name, parent_table, label=f"{child_col} -> {parent_col}", constraint='false')
                        except Exception as e:
                            print(f"Warning: Could not create FK edge: {table_name}.{child_col} -> {parent_table}.{parent_col}: {e}")

       
        dot.render(output_path, view=False, format='png')

        print(f"Schema visualization saved to {output_path}")

    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()


def extract_fks_from_create(create_statement, table_name):
    """Extract foreign keys from CREATE TABLE statement."""

    fks = []
    for match in re.finditer(r"FOREIGN KEY\s*\((.*?)\)\s*REFERENCES\s*(.*?)\s*\((.*?)\)", create_statement, re.IGNORECASE):
        child_cols = [c.strip() for c in match.group(1).split(',')]
        parent_table_ref = match.group(2)

        if '"' in parent_table_ref or "'" in parent_table_ref:
            parent_table = parent_table_ref.split('(')[0].strip().replace('"', '').replace("'", "")
        else:
            parent_table = parent_table_ref.split('(')[0].strip()
        if parent_table.endswith('"') or parent_table.endswith("'"):
            parent_table = parent_table[:-1]
        
        parent_cols = [p.strip() for p in match.group(3).split(',')]
        fks.extend([(parent_table, child_col, parent_col) for child_col, parent_col in zip(child_cols, parent_cols)])

    return fks

def create_table_label(cursor, table_name):
    """Creates the HTML-like label for the table node."""

    columns = cursor.execute(f"PRAGMA table_info({table_name});").fetchall()
    label = f"<\n<TABLE BORDER=\"0\" CELLBORDER=\"1\" CELLSPACING=\"0\">\n<TR><TD COLSPAN=\"2\">{table_name}</TD></TR>\n"
    for column in columns:
        label += f"<TR><TD>{column[1]} ({column[2]})</TD></TR>\n"
    label += "</TABLE>>"
    return label

db_file = "store.sql3.db"
visualize_sqlite_schema(db_file, rows=3, cols=3)

