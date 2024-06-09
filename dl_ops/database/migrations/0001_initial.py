# Generated by Django 4.2 on 2024-06-03 09:35

from django.db import migrations, models
import django.db.models.deletion
import utils.common


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Data Version',
                'verbose_name_plural': 'Data Versions',
                'db_table': 'data_version',
            },
        ),
        migrations.CreateModel(
            name='EdgeBoxInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edge_box_id', models.CharField(max_length=255)),
                ('edge_box_location', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('meta_info', models.JSONField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Edge Box Info',
                'verbose_name_plural': 'Edge Boxes Info',
                'db_table': 'edge_box_info',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_id', models.CharField(max_length=255)),
                ('image_file', models.ImageField(upload_to=utils.common.get_image_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('annotated', models.BooleanField()),
                ('processed', models.BooleanField()),
                ('mode', models.CharField(max_length=255)),
                ('edge_box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.edgeboxinfo')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
                'db_table': 'image',
            },
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_id', models.CharField(max_length=255)),
                ('model_name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Model',
                'verbose_name_plural': 'Models',
                'db_table': 'model',
            },
        ),
        migrations.CreateModel(
            name='ModelMetric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metric_id', models.CharField(max_length=255)),
                ('metric', models.CharField(max_length=255)),
                ('entry_timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Model Metrics',
                'db_table': 'model_metric',
            },
        ),
        migrations.CreateModel(
            name='PlantInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plant_id', models.CharField(max_length=255)),
                ('plant_name', models.CharField(max_length=255)),
                ('plant_location', models.CharField(max_length=255)),
                ('meta_info', models.JSONField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Plant Info',
                'verbose_name_plural': 'Plants Info',
                'db_table': 'plant_info',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.CharField(max_length=255)),
                ('project_name', models.CharField(max_length=255)),
                ('annotation_group', models.JSONField()),
                ('project_type', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('config', models.JSONField(blank=True, null=True)),
                ('edge_box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.edgeboxinfo')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
                'db_table': 'project',
            },
        ),
        migrations.CreateModel(
            name='ModelVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_version', models.CharField(max_length=255)),
                ('model_file', models.FileField(max_length=255, upload_to=utils.common.get_model_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.model')),
                ('trained_with', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.dataversion')),
            ],
            options={
                'verbose_name': 'Model Version',
                'verbose_name_plural': 'Model Versions',
                'db_table': 'model_version',
            },
        ),
        migrations.CreateModel(
            name='ModelEval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metric_value', models.FloatField()),
                ('num_epochs', models.IntegerField()),
                ('optimizer', models.CharField(max_length=255)),
                ('lr', models.FloatField()),
                ('batch_size', models.IntegerField()),
                ('imgsz', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.modelmetric')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.modelversion')),
            ],
            options={
                'verbose_name_plural': 'Model Evaluation',
                'db_table': 'model_eval',
            },
        ),
        migrations.AddField(
            model_name='model',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.project'),
        ),
        migrations.CreateModel(
            name='ImageDataVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('data_version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.dataversion')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.image')),
            ],
            options={
                'verbose_name': 'Image Data Version',
                'verbose_name_plural': 'Image Data Versions',
                'db_table': 'image_data_version',
            },
        ),
        migrations.AddField(
            model_name='edgeboxinfo',
            name='plant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.plantinfo'),
        ),
        migrations.AddField(
            model_name='dataversion',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.project'),
        ),
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annotation_file', models.FileField(max_length=255, upload_to=utils.common.get_label_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('meta_info', models.JSONField(blank=True, null=True)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.image')),
                ('project', models.ForeignKey(default='N/A', on_delete=django.db.models.deletion.CASCADE, to='database.project')),
            ],
            options={
                'verbose_name': 'Annotation',
                'verbose_name_plural': 'Annotations',
                'db_table': 'annotation',
            },
        ),
    ]
