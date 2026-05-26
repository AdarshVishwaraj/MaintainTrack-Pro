"""
insert_data.py — MaintainTrack Pro
------------------------------------
Adds data into all 6 tables:
  SUPPLIER, EQUIPMENT, PART,
  MAINTENANCE_LOG, BREAKDOWN_LOG, ISSUE_RECORD

Run from the project root:
    python scripts/insert_data.py

Safe to run multiple times — always appends fresh rows.
"""

import sqlite3
import os
from datetime import date, timedelta

# ── Config ────────────────────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'maintaintrack.db')
today   = date.today()


def get_connection():
    if not os.path.exists(DB_PATH):
        print("[ERROR] Database not found at:", os.path.abspath(DB_PATH))
        print("        Run the Java app once first so it creates the schema,")
        print("        then re-run this script.")
        exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# ── 1. SUPPLIERS ──────────────────────────────────────────────────────────
def insert_suppliers(conn):
    suppliers = [
        ("FastParts Ltd",      "Rahul Sharma",   "+91-9876543210", "rahul@fastparts.in"),
        ("BoltWorld India",    "Priya Mehta",    "+91-9123456789", "priya@boltworld.in"),
        ("TechSupply Co",      "Arjun Kapoor",   "+91-9988776655", "arjun@techsupply.in"),
        ("MechZone Traders",   "Sunita Rao",     "+91-9871234560", "sunita@mechzone.in"),
        ("ElectroParts India", "Vikram Singh",   "+91-9765432100", "vikram@electroparts.in"),
    ]
    conn.executemany(
        "INSERT INTO SUPPLIER (name, contact_name, phone, email) VALUES (?,?,?,?);",
        suppliers
    )
    print(f"[OK] Inserted {len(suppliers)} suppliers")


# ── 2. EQUIPMENT ──────────────────────────────────────────────────────────
def insert_equipment(conn):
    equipment = [
        # (name, location, status, next_maintenance_date, interval_days)
        ("CNC Machine A1",       "Shop Floor 1",  "Operational",       str(today + timedelta(days=5)),   30),
        ("Hydraulic Press B2",   "Shop Floor 2",  "Operational",       str(today - timedelta(days=2)),   15),
        ("Conveyor Belt C3",     "Warehouse",     "Under Maintenance", str(today + timedelta(days=12)),  60),
        ("Air Compressor D4",    "Utility Room",  "Operational",       str(today + timedelta(days=20)),  45),
        ("Lathe Machine E5",     "Shop Floor 1",  "Operational",       str(today - timedelta(days=1)),   30),
        ("Drill Press F6",       "Shop Floor 3",  "Operational",       str(today + timedelta(days=10)),  30),
        ("Welding Robot G7",     "Assembly Line", "Operational",       str(today + timedelta(days=7)),   21),
        ("Forklift H8",          "Warehouse",     "Out of Service",    str(today - timedelta(days=5)),   90),
        ("Grinding Machine I9",  "Shop Floor 2",  "Operational",       str(today + timedelta(days=14)), 30),
        ("Cooling Tower J10",    "Rooftop",       "Operational",       str(today + timedelta(days=30)), 60),
    ]
    conn.executemany(
        """INSERT INTO EQUIPMENT
           (name, location, status, next_maintenance_date, interval_days)
           VALUES (?,?,?,?,?);""",
        equipment
    )
    print(f"[OK] Inserted {len(equipment)} equipment records")


# ── 3. PARTS ──────────────────────────────────────────────────────────────
def insert_parts(conn):
    # supplier_ids are relative to this session's inserts.
    # We fetch them by name to be safe.
    sup = {row[0]: row[1] for row in conn.execute("SELECT name, id FROM SUPPLIER;")}

    parts = [
        # (supplier_id, name, qty_on_hand, min_qty, unit, unit_cost)
        (sup["FastParts Ltd"],      "Hydraulic Oil Filter",    20,  5,  "pcs",  450.00),
        (sup["FastParts Ltd"],      "V-Belt Drive",             8,  3,  "pcs",  320.00),
        (sup["FastParts Ltd"],      "Coolant Fluid 5L",        12,  5,  "can",  560.00),
        (sup["BoltWorld India"],    "M12 Hex Bolt Set",       150, 20,  "set",   85.00),
        (sup["BoltWorld India"],    "Bearing 6205-2RS",        30, 10,  "pcs",  210.00),
        (sup["BoltWorld India"],    "Lock Washer M10",        200, 30,  "pcs",   12.00),
        (sup["TechSupply Co"],      "Control Relay 24V",        6,  5,  "pcs", 1200.00),
        (sup["TechSupply Co"],      "Air Pressure Gauge",       4,  2,  "pcs",  675.00),
        (sup["MechZone Traders"],   "Pneumatic Cylinder 50mm",  3,  2,  "pcs", 2400.00),
        (sup["MechZone Traders"],   "Grease Cartridge 400g",   25, 10,  "pcs",  180.00),
        (sup["ElectroParts India"], "Motor Capacitor 25uF",     9,  4,  "pcs",  340.00),
        (sup["ElectroParts India"], "Contactor 32A",            5,  3,  "pcs",  890.00),
        (sup["ElectroParts India"], "Proximity Sensor NPN",    10,  4,  "pcs",  760.00),
    ]
    conn.executemany(
        """INSERT INTO PART
           (supplier_id, name, qty_on_hand, min_qty, unit, unit_cost)
           VALUES (?,?,?,?,?,?);""",
        parts
    )
    print(f"[OK] Inserted {len(parts)} parts")


# ── 4. MAINTENANCE LOGS ───────────────────────────────────────────────────
def insert_maintenance_logs(conn):
    # Fetch equipment ids by name
    eq = {row[0]: row[1] for row in conn.execute("SELECT name, id FROM EQUIPMENT;")}

    logs = [
        # (equipment_id, done_on, notes, done_by)
        (eq["CNC Machine A1"],      str(today - timedelta(days=30)), "Full lubrication and belt check",         "Harshit"),
        (eq["Hydraulic Press B2"],  str(today - timedelta(days=15)), "Hydraulic fluid replaced, seals checked", "Ravi"),
        (eq["Conveyor Belt C3"],    str(today - timedelta(days=60)), "Belt tension adjusted and rollers oiled",  "Harshit"),
        (eq["Air Compressor D4"],   str(today - timedelta(days=45)), "Filter cleaned, pressure relief tested",   "Ankit"),
        (eq["Lathe Machine E5"],    str(today - timedelta(days=30)), "Tool alignment and spindle lubrication",   "Harshit"),
        (eq["Drill Press F6"],      str(today - timedelta(days=10)), "Chuck replaced, depth stop calibrated",    "Ravi"),
        (eq["Welding Robot G7"],    str(today - timedelta(days=21)), "Wire feed cleaned, torch tip replaced",    "Ankit"),
        (eq["Grinding Machine I9"], str(today - timedelta(days=14)), "Wheel dressed, coolant nozzle cleaned",    "Harshit"),
        (eq["Cooling Tower J10"],   str(today - timedelta(days=60)), "Fill media cleaned, fan blades inspected", "Ravi"),
        (eq["CNC Machine A1"],      str(today - timedelta(days=60)), "Software calibration and axis alignment",  "Ankit"),
    ]
    conn.executemany(
        """INSERT INTO MAINTENANCE_LOG
           (equipment_id, done_on, notes, done_by)
           VALUES (?,?,?,?);""",
        logs
    )
    print(f"[OK] Inserted {len(logs)} maintenance logs")


# ── 5. BREAKDOWN LOGS ─────────────────────────────────────────────────────
def insert_breakdown_logs(conn):
    eq = {row[0]: row[1] for row in conn.execute("SELECT name, id FROM EQUIPMENT;")}

    logs = [
        # (equipment_id, occurred_on, description, resolved_by)
        (eq["Hydraulic Press B2"], str(today - timedelta(days=10)), "Hydraulic leak — worn seal on cylinder",       "Ravi"),
        (eq["Lathe Machine E5"],   str(today - timedelta(days=5)),  "Motor overheating — coolant level low",        "Harshit"),
        (eq["Forklift H8"],        str(today - timedelta(days=5)),  "Transmission failure — gear box oil leak",     None),
        (eq["Conveyor Belt C3"],   str(today - timedelta(days=20)), "Belt snapped at splice joint",                 "Ankit"),
        (eq["Welding Robot G7"],   str(today - timedelta(days=3)),  "Wire feed jam — contact tip clogged",          "Ankit"),
    ]
    conn.executemany(
        """INSERT INTO BREAKDOWN_LOG
           (equipment_id, occurred_on, description, resolved_by)
           VALUES (?,?,?,?);""",
        logs
    )
    print(f"[OK] Inserted {len(logs)} breakdown logs")


# ── 6. ISSUE RECORDS ──────────────────────────────────────────────────────
def insert_issue_records(conn):
    eq   = {row[0]: row[1] for row in conn.execute("SELECT name, id FROM EQUIPMENT;")}
    part = {row[0]: row[1] for row in conn.execute("SELECT name, id FROM PART;")}

    records = [
        # (part_id, equipment_id, issued_on, qty, issued_by, type)
        (part["Hydraulic Oil Filter"],    eq["Hydraulic Press B2"],  str(today - timedelta(days=10)), 2, "Ravi",    "issue"),
        (part["Bearing 6205-2RS"],        eq["Lathe Machine E5"],    str(today - timedelta(days=5)),  1, "Harshit", "issue"),
        (part["Coolant Fluid 5L"],        eq["Lathe Machine E5"],    str(today - timedelta(days=5)),  1, "Harshit", "issue"),
        (part["M12 Hex Bolt Set"],        eq["CNC Machine A1"],      str(today - timedelta(days=30)), 5, "Harshit", "issue"),
        (part["M12 Hex Bolt Set"],        eq["CNC Machine A1"],      str(today - timedelta(days=1)),  2, "Ankit",   "return"),
        (part["V-Belt Drive"],            eq["Conveyor Belt C3"],    str(today - timedelta(days=20)), 1, "Ankit",   "issue"),
        (part["Control Relay 24V"],       eq["Welding Robot G7"],    str(today - timedelta(days=3)),  1, "Ankit",   "issue"),
        (part["Air Pressure Gauge"],      eq["Air Compressor D4"],   str(today - timedelta(days=45)), 1, "Ankit",   "issue"),
        (part["Grease Cartridge 400g"],   eq["Drill Press F6"],      str(today - timedelta(days=10)), 2, "Ravi",    "issue"),
        (part["Proximity Sensor NPN"],    eq["Grinding Machine I9"], str(today - timedelta(days=14)), 1, "Harshit", "issue"),
        (part["Motor Capacitor 25uF"],    eq["Cooling Tower J10"],   str(today - timedelta(days=60)), 1, "Ravi",    "issue"),
        (part["Pneumatic Cylinder 50mm"], eq["Hydraulic Press B2"],  str(today - timedelta(days=10)), 1, "Ravi",    "issue"),
    ]
    conn.executemany(
        """INSERT INTO ISSUE_RECORD
           (part_id, equipment_id, issued_on, qty, issued_by, type)
           VALUES (?,?,?,?,?,?);""",
        records
    )
    print(f"[OK] Inserted {len(records)} issue records")


# ── Summary ───────────────────────────────────────────────────────────────
def print_summary(conn):
    print("\n── Database Summary ─────────────────────────────────────")
    for t in ['SUPPLIER','EQUIPMENT','PART','MAINTENANCE_LOG','BREAKDOWN_LOG','ISSUE_RECORD']:
        c = conn.execute(f"SELECT COUNT(*) FROM {t};").fetchone()[0]
        print(f"   {t:<22} → {c} rows")

    print("\n── Equipment status ─────────────────────────────────────")
    for name, status, nmd in conn.execute(
        "SELECT name, status, next_maintenance_date FROM EQUIPMENT ORDER BY next_maintenance_date;"
    ):
        flag = " ⚠  OVERDUE" if nmd and nmd < str(today) else ""
        print(f"   {name:<28} [{status}]  due: {nmd}{flag}")

    print("\n── Low stock parts ──────────────────────────────────────")
    rows = conn.execute(
        "SELECT name, qty_on_hand, min_qty FROM PART WHERE qty_on_hand <= min_qty;"
    ).fetchall()
    if rows:
        for name, qty, min_qty in rows:
            print(f"   ⚠  {name:<32} qty={qty}  min={min_qty}")
    else:
        print("   All parts above minimum stock.")
    print("─────────────────────────────────────────────────────────\n")


# ── Main ──────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print(f"\n[insert_data] Connecting to: {os.path.abspath(DB_PATH)}\n")
    conn = get_connection()

    try:
        insert_suppliers(conn)
        insert_equipment(conn)
        insert_parts(conn)
        insert_maintenance_logs(conn)
        insert_breakdown_logs(conn)
        insert_issue_records(conn)
        conn.commit()
        print("\n[OK] All data committed successfully.")
    except Exception as e:
        conn.rollback()
        print(f"\n[ERROR] {e}")
        print("        All changes rolled back — nothing was saved.")
        raise

    print_summary(conn)
    conn.close()
    