import sqlite3

conn = sqlite3.connect('dress_search.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Check all images
cursor.execute('SELECT id, filename, silhouette, length, sleeve_type, color FROM images')
print('Images in DB:')
for row in cursor.fetchall():
    print(f'  ID {row[0]}: silhouette={row[2]}, length={row[3]}, sleeve={row[4]}, color={row[5]}')

# Check embeddings
cursor.execute('SELECT COUNT(*) FROM embeddings')
emb_count = cursor.fetchone()[0]
print(f'\nEmbeddings stored: {emb_count}')

# Test a filter query
print('\n--- Testing filter query for "long sleeve" ---')
cursor.execute('SELECT COUNT(*) FROM images WHERE sleeve_type = "long sleeve"')
print(f'Images with "long sleeve": {cursor.fetchone()[0]}')

cursor.execute('SELECT COUNT(*) FROM images WHERE sleeve_type = "off-shoulder"')
print(f'Images with "off-shoulder": {cursor.fetchone()[0]}')

# Show all unique sleeve values
cursor.execute('SELECT DISTINCT sleeve_type FROM images')
print(f'\nUnique sleeve_type values: {[row[0] for row in cursor.fetchall()]}')
