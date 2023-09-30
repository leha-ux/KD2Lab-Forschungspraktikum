#import psycopg2 library
import psycopg2

#compose a connection string
connection = "postgres://postgres:password@localhost:5432/riro2023"

#connect to Timescale database using the psycopg2 connect function
conn = psycopg2.connect(connection)
cursor = conn.cursor()

#create a table for eye tracker data if not exists
cursor.execute("""
  CREATE TABLE IF NOT EXISTS eyeData (
    id serial PRIMARY KEY,
    user_id int NOT NULL,
    computer_id int NOT NULL,
    gaze_x real NOT NULL,
    gaze_y real NOT NULL,
    pupil_diameter real NOT NULL,
    timestamp timestamp NOT NULL
  );
""")

#define a function that generates eye tracker data
def generate_gaze_data():
  #some logic to generate random or realistic data
  #return a list of tuples with the format (tracker_id, computer_id, gaze_x, gaze_y, pupil_diameter, timestamp)
  return [
    (1, 1, 0.5, 0.6, 3.2, "2021-12-18 10:00:00"),
    (1, 1, 0.4, 0.7, 3.1, "2021-12-18 10:00:01"),
    (2, 2, 0.6, 0.5, 3.3, "2021-12-18 10:00:00"),
    (2, 2, 0.7, 0.4, 3.4, "2021-12-18 10:00:01")
  ]

#get the eye tracker data from the function
gaze_data = generate_gaze_data()

#insert the data into the table using executemany method of psycopg2
cursor.executemany("""
  INSERT INTO eyeDATA (user_id, computer_id, gaze_x, gaze_y, pupil_diameter, timestamp) VALUES (%s,%s,%s,%s,%s,%s);
""", gaze_data)

#commit changes to the database
conn.commit()

#close the connection
conn.close()
