#!/usr/bin/env python3
"""
Database Viewer for Kisan+ Application
This script displays the database contents in a readable format
"""

import sqlite3
import pandas as pd
from datetime import datetime
import os

def view_database():
    db_path = "instance/kisan.db"
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🌱 KISAN+ DATABASE VIEWER")
        print("=" * 50)
        print(f"📅 Viewed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"\n📊 Found {len(tables)} tables in database:")
        for table in tables:
            print(f"   • {table[0]}")
        
        # Display each table
        for table_name in [t[0] for t in tables]:
            print(f"\n" + "="*60)
            print(f"📋 TABLE: {table_name.upper()}")
            print("="*60)
            
            # Get table info
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print("🔧 SCHEMA:")
            for col in columns:
                print(f"   • {col[1]} ({col[2]}) {'- PRIMARY KEY' if col[5] else ''}")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"\n📈 RECORDS: {count} rows")
            
            if count > 0:
                # Get all data
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                
                # Create DataFrame for better display
                df = pd.DataFrame(rows, columns=[col[1] for col in columns])
                
                print(f"\n📄 DATA:")
                if len(df) <= 10:
                    # Show all rows if 10 or fewer
                    print(df.to_string(index=False))
                else:
                    # Show first 5 and last 5 rows
                    print("📊 First 5 rows:")
                    print(df.head().to_string(index=False))
                    print(f"\n... ({len(df)-10} more rows) ...")
                    print("\n📊 Last 5 rows:")
                    print(df.tail().to_string(index=False))
            else:
                print("   (No data)")
        
        conn.close()
        
        print("\n" + "="*60)
        print("✅ Database view complete!")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error reading database: {e}")

def export_to_csv():
    """Export all tables to CSV files"""
    db_path = "instance/kisan.db"
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        
        # Get all table names
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        export_dir = "database_exports"
        os.makedirs(export_dir, exist_ok=True)
        
        print(f"\n📁 Exporting tables to {export_dir}/ directory...")
        
        for table_name in [t[0] for t in tables]:
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            csv_file = f"{export_dir}/{table_name}.csv"
            df.to_csv(csv_file, index=False)
            print(f"   ✅ {table_name}.csv ({len(df)} rows)")
        
        conn.close()
        print(f"🎉 All tables exported successfully!")
        
    except Exception as e:
        print(f"❌ Error exporting: {e}")

if __name__ == "__main__":
    print("🌱 KISAN+ DATABASE TOOLS")
    print("1. View database contents")
    print("2. Export to CSV files")
    print("3. Both")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice in ["1", "3"]:
        view_database()
    
    if choice in ["2", "3"]:
        export_to_csv()
    
    if choice not in ["1", "2", "3"]:
        print("❌ Invalid choice. Running view database...")
        view_database()
