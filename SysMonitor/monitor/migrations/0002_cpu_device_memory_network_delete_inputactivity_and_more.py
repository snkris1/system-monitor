# Generated by Django 5.1.3 on 2024-11-10 04:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CPU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, help_text='Time of the record', verbose_name='Timestamp')),
                ('total_usage_percent', models.FloatField(verbose_name='Total CPU Utilization')),
                ('per_cpu_percent', models.JSONField(verbose_name='CPU Utilization per Core')),
                ('cpu_freq', models.JSONField(verbose_name='CPU Frequency')),
                ('cpu_temperature', models.JSONField(help_text='CPU temperature in Celsius', verbose_name='CPU Temperature')),
            ],
            options={
                'verbose_name': 'CPU',
                'verbose_name_plural': 'CPUs',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the device', max_length=255, verbose_name='Device Name')),
            ],
            options={
                'verbose_name': 'Device',
                'verbose_name_plural': 'Devices',
            },
        ),
        migrations.CreateModel(
            name='Memory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, help_text='Time of the record', verbose_name='Timestamp')),
                ('total_memory', models.IntegerField(verbose_name='Total Memory')),
                ('available_memory', models.IntegerField(verbose_name='Available Memory')),
                ('used_memory', models.IntegerField(verbose_name='Used Memory')),
                ('memory_percent', models.FloatField(verbose_name='Memory Usage')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memory', to='monitor.device', verbose_name='CPU Device')),
            ],
            options={
                'verbose_name': 'Memory',
                'verbose_name_plural': 'Memory',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, help_text='Time of the record', verbose_name='Timestamp')),
                ('is_up', models.BooleanField(help_text='Network status', verbose_name='Is Up')),
                ('speed', models.IntegerField(verbose_name='Speed')),
                ('mtu', models.IntegerField(verbose_name='MTU')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='network', to='monitor.device', verbose_name='CPU Device')),
            ],
            options={
                'verbose_name': 'Network',
                'verbose_name_plural': 'Networks',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.DeleteModel(
            name='InputActivity',
        ),
        migrations.DeleteModel(
            name='NetworkActivity',
        ),
        migrations.RemoveField(
            model_name='notificationalert',
            name='user',
        ),
        migrations.DeleteModel(
            name='SystemPerformance',
        ),
        migrations.RemoveField(
            model_name='visualizationpreference',
            name='user',
        ),
        migrations.AddField(
            model_name='cpu',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cpu', to='monitor.device', verbose_name='CPU Device'),
        ),
        migrations.DeleteModel(
            name='NotificationAlert',
        ),
        migrations.DeleteModel(
            name='VisualizationPreference',
        ),
    ]