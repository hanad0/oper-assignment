from django.db import migrations
from django.conf import settings


def create_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.get_or_create(name="quiz_creator")
    Group.objects.get_or_create(name="quiz_participant")


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.RunPython(create_groups),
    ]
