from django.db import migrations, models
from django.db import connection

def insert_initial_data(apps, schema_editor):
    # some data to the database to visualize how the app works.
    with connection.cursor() as cursor:
        query = f"INSERT INTO pages_textmodel VALUES(1, 'This appears to be very nice and safe chat application.', '27.12.2023', 'ismo')"
        cursor.execute(query)
        query = f"INSERT INTO pages_textmodel VALUES(2, 'Yeah and you can also send private messages!', '27.12.2023', 'seppo')"
        cursor.execute(query)
        query = f"INSERT INTO pages_textmodel VALUES(3, 'I bet no1 else than the intended receiver can see them.', '27.12.2023', 'seppo')"
        cursor.execute(query)
        query = f"INSERT INTO pages_textmodel VALUES(4, 'Hello everybody!', '27.12.2023', 'patrick')"
        cursor.execute(query)
        query = f"INSERT INTO pages_textmodel VALUES(5, 'Hi!', '27.12.2023', 'alice')"
        cursor.execute(query)
        query = f"INSERT INTO pages_textmodel VALUES(6, 'Heyyyyyyyyyy!', '27.12.2023', 'bob')"
        cursor.execute(query)
        query = f"INSERT INTO pages_textmodel VALUES(7, 'Yes, the personal messages are safe and private 100%', '27.12.2023', 'admin')"
        cursor.execute(query)
        query = f"INSERT INTO pages_textmodel VALUES(8, 'That is good to hear, mister admin.', '27.12.2023', 'seppo')"
        cursor.execute(query)
        query = f"INSERT INTO pages_textmodel VALUES(9, 'I am going to throw a party at bikini bottom! Be there or be square!','27.12.2023','bob')"
        cursor.execute(query)

        query = f"INSERT INTO pages_messagemodel VALUES(1, 'It is very nice to be able to talk in private.', 'seppo', 'ismo')"
        cursor.execute(query)
        query = f"INSERT INTO pages_messagemodel VALUES(2, 'Indeed, my dear friend.', 'ismo', 'seppo')"
        cursor.execute(query)
        query = f"INSERT INTO pages_messagemodel VALUES(3, 'This application is extremely well made.', 'ismo', 'seppo')"
        cursor.execute(query)
        query = f"INSERT INTO pages_messagemodel VALUES(4, 'I agree, there could not be a greater chat application.', 'seppo', 'ismo')"
        cursor.execute(query)
        query = f"INSERT INTO pages_messagemodel VALUES(5, 'I hope you chose a safe password as I did. Luckily my safe choice is also easy to remember!', 'patrick', 'bob')"
        cursor.execute(query)
        query = f"INSERT INTO pages_messagemodel VALUES(6, 'My password is almost impregnable. There is no way any1 could quess it!', 'bob', 'patrick')"

class Migration(migrations.Migration):

    dependencies = [
        ('pages','0011_alter_messagelimit_message_count_and_more'),
    ]

    operations = [
        migrations.RunPython(insert_initial_data),
    ]