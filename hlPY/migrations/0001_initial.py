# Generated by Django 2.2.1 on 2019-05-13 16:07

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_info',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('sex', models.CharField(max_length=2)),
                ('age', models.IntegerField(default=20)),
                ('phone', models.CharField(max_length=11, unique=True)),
                ('coin', models.IntegerField(default=5000)),
                ('image', models.CharField(max_length=255)),
                ('env_dir', models.CharField(max_length=255)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='course_python_practice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('practice_id', models.IntegerField()),
                ('practice_name', models.CharField(max_length=255)),
                ('practice_chapter_id', models.IntegerField()),
                ('practice_chapter_name', models.CharField(max_length=255)),
                ('practice_info_id', models.CharField(max_length=255, unique=True)),
                ('practice_info_contant', models.CharField(max_length=255)),
            ],
            options={
                'unique_together': {('practice_id', 'practice_chapter_id', 'practice_info_id')},
            },
        ),
        migrations.CreateModel(
            name='user_tool',
            fields=[
                ('tool_id', models.IntegerField(primary_key=True, serialize=False)),
                ('tool_name', models.CharField(max_length=255)),
                ('tool_describe', models.CharField(max_length=255)),
                ('tool_price', models.IntegerField()),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('conform_status', models.IntegerField(default=0)),
                ('save_dir', models.CharField(max_length=255)),
                ('download_num', models.IntegerField()),
                ('conform_date', models.DateTimeField()),
                ('tool_owner_id', models.ForeignKey(on_delete='CASCADE', related_name='user_id_user_tool', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='program_env',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program_env', models.IntegerField(default=1)),
                ('user_id', models.ForeignKey(on_delete='CASCADE', related_name='user_id_program_env', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='practice_learn_progress',
            fields=[
                ('progress_id', models.IntegerField(primary_key=True, serialize=False)),
                ('practice_id', models.IntegerField()),
                ('practice_chapter_id', models.IntegerField()),
                ('learn_status', models.CharField(max_length=2, null=True)),
                ('learn_time', models.BigIntegerField(null=True)),
                ('practice_info_id', models.ForeignKey(on_delete='CASCADE', to='hlPY.course_python_practice', to_field='practice_info_id')),
                ('user_id', models.ForeignKey(on_delete='CASCADE', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='course_python_basic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basic_id', models.IntegerField()),
                ('basic_name', models.CharField(max_length=255)),
                ('basic_chapter_id', models.IntegerField()),
                ('basic_chapter_name', models.CharField(max_length=255)),
                ('basic_contant_id', models.CharField(max_length=255, unique=True)),
                ('basic_contant_info', models.CharField(max_length=255)),
            ],
            options={
                'unique_together': {('basic_id', 'basic_chapter_id', 'basic_contant_id')},
            },
        ),
        migrations.CreateModel(
            name='basic_learn_progress',
            fields=[
                ('progress_id', models.AutoField(primary_key=True, serialize=False)),
                ('basic_id', models.IntegerField()),
                ('basic_chapter_id', models.IntegerField()),
                ('learn_status', models.CharField(max_length=2)),
                ('learn_time', models.BigIntegerField(default=0)),
                ('basic_contant_id', models.ForeignKey(on_delete='CASCADE', to='hlPY.course_python_basic', to_field='basic_contant_id')),
                ('user_id', models.ForeignKey(on_delete='CASCADE', related_name='user_id_basic_learn_progress', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
