# Vehicle Registration & Licensing System (VRLS)

## About the Project

This is a DBMS mini project where we designed a system to manage vehicle registration and licensing details. The idea was to create a centralized database that can store and organize information about vehicle owners, registrations, inspections, insurance, and also keep a history of all activities related to a vehicle.

---

## What the system does

* Stores owner and vehicle details
* Keeps track of registration dates and expiry
* Records inspection results
* Maintains insurance information
* Logs all important events in a history table
* Allows basic searching and viewing of records

---

## Database Design

We created multiple tables like:

* Owner
* Vehicle
* Registration
* Inspection
* Insurance
* History

All tables are connected using keys (like owner_id, vehicle_id, etc.) to maintain relationships.

We also applied normalization:

* 1NF: No repeating values
* 2NF: No partial dependency
* 3NF: Removed redundancy as much as possible

---

## Features implemented

* SQL queries to fetch combined data (joins)
* Function to calculate vehicle age
* View to check expired registrations
* Filtering (like failed inspections)
* History tracking for each vehicle

---

## Frontend

We also created a simple HTML page to show how the system would look.
It displays:

* Sample data in tables
* SQL queries used
* Different sections like owner data, registration, inspection, etc.

(This is just a demo UI, not connected to a real database)

---

## Tech Used

* SQL (for database)
* HTML + CSS (for frontend demo)

---

## Conclusion

This project helped us understand how real-world systems manage structured data using DBMS concepts like normalization, relationships, and queries. It also gave us a basic idea of how frontend and backend can be connected.

---

## Team Members

* Ambarish Mohan
* Ashish Govind
* Afrose Banu
* Siddharth Tripathi
* Tanush Chandrahas
