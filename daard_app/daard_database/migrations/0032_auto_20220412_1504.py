from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daard_database', '0031_auto_20220202_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diseasecase',
            name='archaeological_burial_type',
            field=models.CharField(blank=True, choices=[('single', 'Single'), ('double', 'Double'), ('multiple', 'Multiple'), ('unknown', 'Unknown')], max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='diseasecase',
            name='archaeological_funery_context',
            field=models.CharField(blank=True, choices=[('primary', 'Primary'), ('secondary', 'Secondary'), ('unknown', 'Unknown')], max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='diseasecase',
            name='dna_analyses',
            field=models.CharField(choices=[('successful', 'Successful'), ('unsuccessful', 'Unsuccessful'), ('absent', 'Absent'), ('unknown', 'Unknown')], max_length=400),
        ),
        migrations.AlterField(
            model_name='diseasecase',
            name='sex',
            field=models.CharField(choices=[('f', 'F'), ('f?', 'F?'), ('unknown', 'Unknown'), ('m', 'M'), ('m?', 'M?')], max_length=200),
        ),
    ]
