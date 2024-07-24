# main.py

import streamlit as st
from ui import main_ui
import database as dbs

def main():
    # Create database tables if they don't exist
    dbs.create_tables()

    # Run the main UI
    main_ui()
    dbs.close_connection()

if __name__ == "__main__":
    main()
