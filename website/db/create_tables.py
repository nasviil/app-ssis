import os

script_path = os.path.join(os.path.dirname(
    __file__), 'create_tables_script.sql')


def create_tables(app, mysql):
    with open(script_path, 'r') as f:
        sql = f.read()
        with app.app_context():
            sql_commands = sql.split(';')
            cur = mysql.connection.cursor()
            for command in sql_commands:
                if command.strip():
                    cur.execute(command)
            mysql.connection.commit()