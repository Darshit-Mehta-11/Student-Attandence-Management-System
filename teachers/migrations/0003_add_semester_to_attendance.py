from django.db import migrations, models


def load_default_semester(apps, schema_editor):
    Attendance = apps.get_model('teachers', 'Attendance')
    for att in Attendance.objects.all():
        att.semester = 1
        att.save()


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0002_alter_attendance_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='semester',
            field=models.PositiveSmallIntegerField(choices=[(1, '1st'), (2, '2nd'), (3, '3rd'), (4, '4th')], default=1, help_text='Semester during which attendance was recorded'),
        ),
        migrations.RunPython(load_default_semester, reverse_code=migrations.RunPython.noop),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together={('student', 'semester', 'date')},
        ),
        migrations.AlterModelOptions(
            name='attendance',
            options={'ordering': ['-semester', '-date']},
        ),
    ]