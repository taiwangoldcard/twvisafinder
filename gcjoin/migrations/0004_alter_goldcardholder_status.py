# Generated by Django 3.2 on 2021-08-14 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gcjoin', '0003_alter_goldcardholder_roles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goldcardholder',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending Approval'), ('Approved', 'Verified as a Gold Card Holder'), ('Joined', 'Community Onboarding Complete'), ('Banned', 'Removed for being disruptive'), ('Unknown', 'Added before this system existed'), ('Rejected', 'Rejected')], default='Pending', max_length=64),
        ),
    ]
