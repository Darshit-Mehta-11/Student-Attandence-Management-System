from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.PositiveSmallIntegerField(choices=[(1, '1st'), (2, '2nd'), (3, '3rd'), (4, '4th')], default=1)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('paid', models.BooleanField(default=False)),
                ('paid_on', models.DateField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=models.deletion.CASCADE, to='accounts.customuser')),
            ],
        ),
    ]