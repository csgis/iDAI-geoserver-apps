from django.db import migrations

def no_op(apps, schema_editor):
    pass  # This is a no-op function

class Migration(migrations.Migration):

    dependencies = [
        ('daard_database', '0025_auto_20220202_1412'),
    ]

    operations = [
        migrations.RunPython(no_op, reverse_code=no_op),
    ]
