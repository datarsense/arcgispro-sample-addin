# Sample Arcgis PRO SDK addin for toolbox packaging

## Usage
Arcgis PRO provides customization capabilities using Python toolbox (PYT). However, these Python toolbox are stored as files in the current Arcgis Project and have to be imported back manually when shared as PYT files to other users or when creating a new Arcgis project.

Arcgis PRO SDK addins provides a simple way to **package and deploy PYT toolbox at large scale** as :
  - They can be deployed from a central location (shared folder) to all Arcgis PRO users
  - Arcgis PRO SDK register PYT toolbox as geoprocessing tools which make them globally available in all Arcgis Projects.

## Reference
https://github.com/Esri/arcgis-pro-sdk/wiki/ProGuide-content-and-image-resources#embedding-toolboxes
https://github.com/Esri/arcgis-pro-sdk/wiki/ProGuide-ArcGIS-Pro-Extensions-NuGet