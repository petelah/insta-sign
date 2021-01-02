from flask import jsonify
from src import db


def dump_db():
	"""
	Dumps whole databse to JSON.
	:return: JSON object
	"""
	table_list = []
	for table in db.metadata.tables.items():
		table_list.append(table[0])
	db_dict = dict.fromkeys(table_list)
	for table in table_list:
		db_dict[table] = []
		query = db.engine.execute(
			f'SELECT * FROM {table}'
		)
		for row in query:
			db_dict[f"{table}"].append(list(row))
	return jsonify(db_dict)
