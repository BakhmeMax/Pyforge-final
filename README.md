# Pyforge-final

This is the final project of the PyForge3 course.

This project uses docker to create a PostgreSQL database and Python code to fill it with data.
The data is taken from the opensource API.

Sample URL: _https://www.ebi.ac.uk/pdbe/graph-api/compound/summary/ATP_

List of available compounds: **['ADP', 'ATP', 'STI', 'ZID', 'DPM', 'XP9', '18W', '29P']**

Data stored in PostgreSQL:
1. compound
2. name
3. formula
4. inchi
5. inchi_key
6. smiles
7. cross_links_count - amount of objects in cross_links property

Log file: _logs.log_


To start the project, you need to clone project and run the following command:

`cd /path/to/project`

`docker-compose up --build`

This will build your images and then start the containers.