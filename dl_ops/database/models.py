import json
from django.db import models
from utils.common import get_model_path, get_image_path, get_label_path


class PlantInfo(models.Model):
    """
    Model representing a plant.

    Attributes:
    - plant_id: A unique identifier for the plant.
    - plant_name: The name of the plant.
    - plant_location: The location of the plant.
    - meta_info: Additional metadata related to the plant.
    - created_at: Timestamp of when the plant record was created.
    """
    plant_id = models.CharField(max_length=255)
    plant_name = models.CharField(max_length=255)
    plant_location = models.CharField(max_length=255)
    meta_info = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Plant Info"
        verbose_name_plural = "Plants Info"
        db_table = 'plant_info'

    def __str__(self):
        return f"{self.plant_name} ({self.plant_location})"

class EdgeBoxInfo(models.Model):
    """
    Model representing an Edge Box.

    Attributes:
    - plant: Foreign key linking to the plant where the edge box is located.
    - edge_box_id: A unique identifier for the edge box.
    - edge_box_location: The location of the edge box.
    - created_at: Timestamp of when the edge box record was created.
    - meta_info: Additional metadata related to the edge box.
    """
    plant = models.ForeignKey(PlantInfo, on_delete=models.CASCADE)
    edge_box_id = models.CharField(max_length=255)
    edge_box_location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    meta_info = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Edge Box Info"
        verbose_name_plural = "Edge Boxes Info"
        db_table = 'edge_box_info'

    def __str__(self):
        return f"Edge Box {self.edge_box_id} at {self.edge_box_location}"
    
class Project(models.Model):
    """
    Model representing a project.

    Attributes:
    - edge_box: Foreign key linking to the edge box associated with the project.
    - project_id: A unique identifier for the project.
    - project_name: The name of the project.
    - annotation_group: Group of annotations related to the project.
    - project_type: The type of the project.
    - created_at: Timestamp of when the project record was created.
    - config: Configuration settings for the project.
    """
    edge_box = models.ForeignKey(EdgeBoxInfo, on_delete=models.CASCADE)
    project_id = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    annotation_group = models.JSONField()
    project_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    config = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        db_table = 'project'

    def __str__(self):
        return f"Project {self.project_name} ({self.project_type})"

class DataVersion(models.Model):
    """
    Model representing a version of data.

    Attributes:
    - project: Foreign key linking to the project associated with this data version.
    - version: The version identifier for the data.
    - description: A description of the data version.
    - created_at: Timestamp of when the data version record was created.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    version = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Data Version"
        verbose_name_plural = "Data Versions"
        db_table = 'data_version'

    def __str__(self):
        return f"Data Version {self.version} for {self.project.project_name}"

class Image(models.Model):
    """
    Model representing an image.

    Attributes:
    - edge_box: Foreign key linking to the edge box that captured the image.
    - image_id: A unique identifier for the image.
    - image_file: Path to the image file.
    - created_at: Timestamp of when the image was created.
    - annotated: Boolean indicating whether the image has been annotated.
    - processed: Boolean indicating whether the image has been processed.
    - mode: Mode or type of the image.
    """
    edge_box = models.ForeignKey(EdgeBoxInfo, on_delete=models.CASCADE)
    image_id = models.CharField(max_length=255)
    image_file = models.ImageField(upload_to=get_image_path)
    created_at = models.DateTimeField(auto_now_add=True)
    annotated = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    mode = models.CharField(max_length=255, default='N/A')

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
        db_table = 'image'

    def __str__(self):
        return f"Image {self.image_id} from {self.edge_box.edge_box_id}"

class ImageDataVersion(models.Model):
    """
    Intermediary model linking images to data versions.

    Attributes:
    - image: Foreign key linking to the image.
    - data_version: Foreign key linking to the data version.
    - created_at: Timestamp of when the link was created.
    """
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    data_version = models.ForeignKey(DataVersion, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Image Data Version"
        verbose_name_plural = "Image Data Versions"
        db_table = 'image_data_version'

    def __str__(self):
        return f"Image {self.image.image_id} in Data Version {self.data_version.version}"

class Annotation(models.Model):
    """
    Model representing an annotation for an image.

    Attributes:
    - image: Foreign key linking to the image.
    - annotation_file: Path to the annotation file.
    - created_at: Timestamp of when the annotation was created.
    - meta_info: Additional metadata related to the annotation.
    """
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default='N/A')
    annotation_file = models.FileField(upload_to=get_label_path, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    meta_info = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Annotation"
        verbose_name_plural = "Annotations"
        db_table = 'annotation'

    def __str__(self):
        return f"Annotation for Image {self.image.image_id}"

class Model(models.Model):
    """
    Model representing a machine learning model.

    Attributes:
    - project: Foreign key linking to the project associated with this model.
    - model_id: A unique identifier for the model.
    - model_name: The name of the model.
    - description: A description of the model.
    - created_at: Timestamp of when the model record was created.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    model_id = models.CharField(max_length=255)
    model_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Model"
        verbose_name_plural = "Models"
        db_table = 'model'

    def __str__(self):
        return f"Model {self.model_name} ({self.model_id})"

class ModelVersion(models.Model):
    """
    Model representing a version of a machine learning model.

    Attributes:
    - model: Foreign key linking to the model.
    - trained_with: Foreign key linking to the data version the model was trained with.
    - model_version: The version identifier for the model.
    - model_file: Path to the model file.
    - created_at: Timestamp of when the model version record was created.
    """
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    trained_with = models.ForeignKey(DataVersion, on_delete=models.CASCADE)
    model_version = models.CharField(max_length=255)
    model_file = models.FileField(upload_to=get_model_path, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Model Version"
        verbose_name_plural = "Model Versions"
        db_table = 'model_version'

    def __str__(self):
        return f"{self.model.model_name} - Version {self.model_version}"    


class ModelMetric(models.Model):
    metric_id = models.CharField(max_length=255)
    metric = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'model_metric'
        verbose_name_plural = 'Model Metrics'
    
    def __str__(self):
        return self.metric


# class ModelCFG(models.Model):
#     VALUE_TYPES = [
#         ('str', 'String'),
#         ('int', 'Integer'),
#         ('float', 'Float'),
#         ('bool', 'Boolean'),
#         ('json', 'JSON'),
#     ]
    
#     model = models.ForeignKey(ModelsType, on_delete=models.CASCADE)
#     key = models.CharField(max_length=255)
#     value_type = models.CharField(max_length=10, choices=VALUE_TYPES)
#     value = models.JSONField()
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         db_table = 'model_cfg'
#         verbose_name_plural = 'Model Configuration'
    
#     def __str__(self) -> str:
#         return f'{self.model}, {self.key}, {self.value_type}'

# # You might need to create a custom save method to ensure value type integrity
#     def save(self, *args, **kwargs):
#         if self.value_type == 'str' and not isinstance(self.value, str):
#             raise ValueError('Value must be a string')
#         elif self.value_type == 'int' and not isinstance(self.value, int):
#             raise ValueError('Value must be an integer')
#         elif self.value_type == 'float' and not isinstance(self.value, float):
#             raise ValueError('Value must be a float')
#         elif self.value_type == 'bool' and not isinstance(self.value, bool):
#             raise ValueError('Value must be a boolean')
#         # JSONField should naturally handle any dict, list, etc.
#         super().save(*args, **kwargs)
    
class ModelEval(models.Model):
    model = models.ForeignKey(ModelVersion, on_delete=models.CASCADE)
    metric = models.ForeignKey(ModelMetric, on_delete=models.CASCADE)
    metric_value = models.FloatField()
    num_epochs = models.IntegerField()
    optimizer = models.CharField(max_length=255)
    lr = models.FloatField()
    batch_size = models.IntegerField()
    imgsz = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'model_eval'
        verbose_name_plural = 'Model Evaluation'
        
    def __str__(self):
        return f"{self.model}, {self.metric}, {self.metric_value}"
