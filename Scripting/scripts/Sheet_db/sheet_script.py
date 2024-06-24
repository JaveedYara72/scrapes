import psycopg2
import gspread
from datetime import datetime, date
from oauth2client.service_account import ServiceAccountCredentials

# connecting to the database
conn = psycopg2.connect(
    database="postgres",
    user='postgres',
    password='ReR2rcJqRjfzBfsGzokU',
    host='una-brands-airbyte-stage.c0jcbrt0yua1.ap-southeast-1.rds.amazonaws.com',
    port='5432'
)

# only pass variables into the query
mart = "mart.pipeline_integration_status_daily"

# setting a cursor to the database
cur = conn.cursor()
cur.execute(f"SELECT * FROM {mart}")

# read the database
rows = cur.fetchall()

# Close the cursor and connection
cur.close()
conn.close()

# Convert datetime objects to strings
converted_rows = []
for row in rows:
    converted_row = []
    for value in row:
        if isinstance(value, datetime):
            converted_row.append(str(value))
        elif isinstance(value, date):
            converted_row.append(value.strftime('%Y-%m-%d'))  # Convert date to string
        elif value is None:
            converted_row.append("")  # Set None values as empty string
        else:
            try:
                datetime_value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                converted_row.append(datetime_value.strftime('%Y-%m-%d %H:%M:%S'))
            except ValueError:
                converted_row.append(value)
    converted_rows.append(converted_row)

# read credentials
scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(credentials)

# Open the Google Sheet
spreadsheet = client.open("Data pipeline integration status daily")

# Access a specific worksheet by name
worksheet = spreadsheet.worksheet("Sheet1")

# Clear existing data on the sheet
worksheet.clear()

# Write the data to the worksheet
header_row = [desc[0] for desc in cur.description]
worksheet.append_row(header_row)
worksheet.append_rows(converted_rows)

print(f"Data uploaded successfully to Google Sheet -> {datetime.now()}")
