from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daard_database', '0036_auto_20221011_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diseasecase',
            name='age',
            field=models.CharField(choices=[('does_not_apply', 'Does not apply')], max_length=200),
        ),
    ]
