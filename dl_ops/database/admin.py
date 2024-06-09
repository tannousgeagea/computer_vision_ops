from django.contrib import admin
from .models import (
    PlantInfo, EdgeBoxInfo, Project, DataVersion,
    Image, ImageDataVersion, Annotation, Model, ModelVersion,
    ModelEval, ModelMetric
)

@admin.register(PlantInfo)
class PlantInfoAdmin(admin.ModelAdmin):
    list_display = ('plant_id', 'plant_name', 'plant_location', 'created_at')
    search_fields = ('plant_id', 'plant_name', 'plant_location')
    list_filter = ('created_at',)

@admin.register(EdgeBoxInfo)
class EdgeBoxInfoAdmin(admin.ModelAdmin):
    list_display = ('edge_box_id', 'edge_box_location', 'plant', 'created_at')
    search_fields = ('edge_box_id', 'edge_box_location', 'plant__plant_name')
    list_filter = ('created_at', 'plant__plant_name')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'project_name', 'edge_box', 'project_type', 'created_at')
    search_fields = ('project_id', 'project_name', 'project_type', 'edge_box__edge_box_id')
    list_filter = ('created_at', 'project_type')

@admin.register(DataVersion)
class DataVersionAdmin(admin.ModelAdmin):
    list_display = ('version', 'description', 'project', 'created_at')
    search_fields = ('version', 'description', 'project__project_name')
    list_filter = ('created_at', 'project__project_name')

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_id', 'image_file', 'edge_box', 'annotated', 'processed', 'mode', 'created_at')
    search_fields = ('image_id', 'image_file', 'edge_box__edge_box_id')
    list_filter = ('created_at', 'annotated', 'processed')

@admin.register(ImageDataVersion)
class ImageDataVersionAdmin(admin.ModelAdmin):
    list_display = ('image', 'data_version', 'created_at')
    search_fields = ('image__image_id', 'data_version__version')
    list_filter = ('created_at', 'data_version')

@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ('image', 'annotation_file', 'created_at')
    search_fields = ('image__image_id', 'annotation_file')
    list_filter = ('created_at',)

@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('model_id', 'model_name', 'project', 'created_at')
    search_fields = ('model_id', 'model_name', 'project__project_name')
    list_filter = ('created_at', 'project__project_name')

@admin.register(ModelVersion)
class ModelVersionAdmin(admin.ModelAdmin):
    list_display = ('model', 'model_version', 'trained_with', 'created_at')
    search_fields = ('model__model_name', 'model_version', 'trained_with__version')
    list_filter = ('created_at', 'model__model_name')


@admin.register(ModelEval)
class ModelEvalAdmin(admin.ModelAdmin):
    list_display = ('model', 'metric', 'metric_value', 'num_epochs', 'optimizer', 'lr', 'batch_size', 'imgsz', 'created_at')
    list_filter = ('model', 'metric', 'optimizer', 'created_at')
    search_fields = ('model__name', 'metric__name', 'optimizer')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

@admin.register(ModelMetric)
class ModelMetricAdmin(admin.ModelAdmin):
    list_display = ('metric_id', 'metric', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('metric_id', 'metric')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

# Register the models without custom admin views
# admin.site.register(PlantInfo, PlantInfoAdmin)
# admin.site.register(EdgeBoxInfo, EdgeBoxInfoAdmin)
# admin.site.register(Project, ProjectAdmin)
# admin.site.register(DataVersion, DataVersionAdmin)
# admin.site.register(Image, ImageAdmin)
# admin.site.register(ImageDataVersion, ImageDataVersionAdmin)
# admin.site.register(Annotation, AnnotationAdmin)
# admin.site.register(Model, ModelAdmin)
# admin.site.register(ModelVersion, ModelVersionAdmin)
