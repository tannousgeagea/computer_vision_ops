from utils.config import edge_box, project, Annotation, Image, DataVersion, ImageDataVersion
from utils.tools import increment_version

def version_data():
    
    if not len(DataVersion.objects.filter(project=project)):
        print(f'data version for {project} does not exist yet - Creating new data version ... !')
        new_version = 'v0.00.01'
        data_version = DataVersion(
            project=project,
            version=new_version,
            description=f'Data Version {new_version} for Project {project.project_name}',
        )
        
    else:
        data_version = DataVersion.objects.filter(project=project).order_by('-version').first()
        new_version = increment_version(data_version.version)
        
    annotations = Annotation.objects.filter(project=project)
    if not len(annotations):
        print(f'No data for project {project.project_name} have been registered yet')
        return False
    
    new_data_version = DataVersion(
        project=project, version=new_version, description=f'Data Version {new_version} for Project {project.project_name}'
    )
    
    new_data_version.save()
    image_data_version = [
        ImageDataVersion(
            image=annotation.image,
            data_version=new_data_version,
        ) for annotation in annotations
    ]
    
    ImageDataVersion.objects.bulk_create(image_data_version)
    
if __name__ == "__main__":
    version_data()

