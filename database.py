import sqlite3

DB_PATH = "invoices.db"


def _get_connection():
    """Returns a connection with row_factory so rows behave like dicts."""
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row  #to access columns by its name
    return con


def _init_db():
    """Creates the table if it doesn't exist yet (safe to call on every startup)."""
    with _get_connection() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                    id             INTEGER PRIMARY KEY AUTOINCREMENT,
                    invoice_number TEXT UNIQUE NOT NULL,
                    date           DATE,
                    due_date       DATE,
                    order_number   TEXT,
                    vat_percent    REAL
            )
        """)

_init_db()  # runs once when the module is imported


def _row_to_dict(row) -> dict:
    return {
        "invoice_number": row["invoice_number"],
        "date":           row["date"],
        "due_date":       row["due_date"],
        "order_number":   row["order_number"],
        "vat_percent":    row["vat_percent"],
        "id":             row["id"],
    }


# ── functions to API endpoints ──────────────────────────────────

def get_all_invoices(limit: int = None):
    query = "SELECT * FROM invoices ORDER BY id"
    if limit:
        query += f" LIMIT {limit}"
    with _get_connection() as con:
        rows = con.execute(query).fetchall()

    result = [] # the result will be the list of dictionaries
    for r in rows:
        d = _row_to_dict(r)
        result.append(d)
    
    return result


def get_invoice_details(invoice_id: int):
    with _get_connection() as con:
        row = con.execute(
            "SELECT * FROM invoices WHERE id = ?", (invoice_id,)
        ).fetchone()
    if row is None:
        return "not found"
    return [_row_to_dict(row)]


def add_invoice(invoiceData):
    with _get_connection() as con:
        try:
            con.execute("""
                INSERT INTO invoices (invoice_number, date, due_date, order_number, vat_percent)
                VALUES (?, ?, ?, ?, ?)
            """, (invoiceData.invoice_number, invoiceData.date, invoiceData.due_date,
                  invoiceData.order_number, invoiceData.vat_percent))
        except sqlite3.IntegrityError:
            raise ValueError("invoice_number already exists in database")


def update_invoice(invoice_id: int, invoiceData):
    fields = invoiceData.model_dump(exclude_unset=True)
    if not fields:
        return  # nothing to update

    set_clause=[]
    for col in fields:
        part = f"{col} = ?"
        set_clause.append(part)
    set_clause = ", ".join(set_clause)
    
    values = list(fields.values()) + [invoice_id]

    with _get_connection() as con:
        cur = con.execute(
            f"UPDATE invoices SET {set_clause} WHERE id = ?", values
        )
        if cur.rowcount == 0:
            raise ValueError("invoice not found")


def delete_invoice(invoice_id: int):
    with _get_connection() as con:
        cur = con.execute("DELETE FROM invoices WHERE id = ?", (invoice_id,))
        if cur.rowcount == 0:
            raise ValueError("invoice not found")