from django.db import migrations, models


def add_github_contact(apps, schema_editor):
    ContactInfo = apps.get_model('main', 'ContactInfo')
    ContactInfo.objects.get_or_create(
        contact_type='github',
        defaults={'label': '@skislyakow', 'value': 'skislyakow', 'sort_order': 2},
    )


def remove_github_contact(apps, schema_editor):
    ContactInfo = apps.get_model('main', 'ContactInfo')
    ContactInfo.objects.filter(contact_type='github').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_skill_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinfo',
            name='contact_type',
            field=models.CharField(
                choices=[('email', 'Email'), ('telegram', 'Telegram'), ('github', 'GitHub')],
                max_length=10,
                verbose_name='Тип',
            ),
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='value',
            field=models.CharField(
                help_text='email, @username или username GitHub',
                max_length=200,
                verbose_name='Значение',
            ),
        ),
        migrations.RunPython(add_github_contact, remove_github_contact),
    ]
