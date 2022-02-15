# Sample Arcgis PRO SDK addin for toolbox packaging

## Usage
Arcgis PRO provides customization capabilities using Python toolbox (PYT). However, these Python toolbox are stored as files in the current Arcgis Project and have to be imported back manually when shared as PYT files to other users or when creating a new Arcgis project.

Arcgis PRO SDK addins provides a simple way to **package and deploy PYT toolbox at large scale** as :
  - They can be deployed from a central location (shared folder) to all Arcgis PRO users
  - Arcgis PRO SDK register PYT toolbox as geoprocessing tools which make them globally available in all Arcgis Projects.

## Building the esriAddinX package
### Building with Visual Studio
This method is convenient for development but requires both Visual Studio and Arcgis PRO installed to make the project build.

Follow the https://github.com/Esri/arcgis-pro-sdk/wiki#installing-arcgis-pro-sdk-for-net tutorial to setup the build environment.

### Building in a CI Pipeline with github workflow
Use the following step to build the addin with **msbuild** in a github workflow. A build matrix is used to build the addin for 2.7, 2.8, 2.9 ArcGIS PRO versions for backward compatibilty.

```
name: MSBuild
on: [push]
env:
  # Path to the solution file relative to the root of the project.
  SOLUTION_FILE_PATH: ProAppModule3.sln
  # Configuration type to build.
  BUILD_CONFIGURATION: Release

jobs:
  build:
    runs-on: windows-latest
    strategy:
      matrix:
        arcgisproversion: ['2.7.0.26828', '2.8.0.29751', '2.9.0.32739']
    steps:
    - uses: actions/checkout@v2

    - name: Add MSBuild to PATH
      uses: microsoft/setup-msbuild@v1.0.2

    - name: Build
      working-directory: ${{env.GITHUB_WORKSPACE}}
      # Add additional options to the MSBuild command line here (like platform or verbosity level).
      # See https://docs.microsoft.com/visualstudio/msbuild/msbuild-command-line-reference
      run: | 
        ((Get-Content -path ProAppModule3\Config.daml -Raw) -replace '2.7.0.26828', '${{ matrix.arcgisproversion }}') | Set-Content -Path ProAppModule3\Config.daml
        ((Get-Content -path ProAppModule3\ProAppModule3.csproj -Raw) -replace '2.7.0.26828', '${{ matrix.arcgisproversion }}') | Set-Content -Path ProAppModule3\ProAppModule3.csproj
        msbuild /m /p:Configuration=${{env.BUILD_CONFIGURATION}} /t:clean ${{env.SOLUTION_FILE_PATH}}
        msbuild /m /p:Configuration=${{env.BUILD_CONFIGURATION}} /t:restore ${{env.SOLUTION_FILE_PATH}}
        msbuild /m /p:Configuration=${{env.BUILD_CONFIGURATION}} ${{env.SOLUTION_FILE_PATH}}

```

## Packaging a toolbox
### Option 1 : Build esriAddinX from source
The first option to package Arcgis PRO Python toolboxes is to clone this repository and build the `esriAddinX` package from source whth either Visual Studio or MSBuild. **A windows environment is required for such a build.**

Clone this repository and edit the `AddInInfo` part of the **Config.daml** addin configuration file :
```
  <AddInInfo id="{63e68afa-6999-4a28-9a19-4ac5e5f3aedf}" version="0.1a" desktopVersion="2.7.0.26828">
    <Name>ProAppModule3</Name>   
    <Description>ProAppModule3 description</Description>
    <Image>Images\AddinDesktop32.png</Image>
    <Author>datarsense</Author>
    <Company>Acme</Company>
    <Date>25/01/2022 22:30:50</Date>
    <Subject>Framework</Subject>
    <!-- Note subject can be one or more of these topics:
                    Content, Framework, Editing, Geodatabase, Geometry, Geoprocessing, Layouts, Map Authoring, Map Exploration -->
  </AddInInfo>
```

 Copy the Python toolboxes  in the `Toolboxes\toolboxes` repository of the SDK addin and declare them as `AddInContent` in the **.csproj** Visual Studio project description file to make them included in the `esriAddinX`package at build time.

**Directory structure**
```
\---Toolboxes
    \---toolboxes
            sampletoolbox.pyt
 ```

**Toolbox path declared as `AddInContent` inProAppModule3.csproj**
```
  <ItemGroup>
    <AddInContent Include="Toolboxes\toolboxes\sampletoolbox.pyt" />
  </ItemGroup>
```

### Option 2 : Embedding toolboxes in a precompiled esriAddinX template
Arcgis PRO `esriAddinX` sdk addins are basically a ZIP file packaging the addin executable files (.dll), the addin content (static files, toolboxes, ..) and a `Config.daml` file describing the addin content and the Arcgis PRO menus customizations (new icons, ...)

As Python toolboxes are just embedded in the `Toolboxes\toolboxes` repository of the `esriAddinX` ZIP archive, they can be added in the archive **after** package construction. This method requires an `esriAddinX`addin template built for the target Arcgis Pro version (provided by this project). A windows compilation environment is not required anymore.

Copy the **Config.daml** file of this project in your python toolbox repository and tweak the `AddInInfo` :
  * **Change** the `id` with a new unique GUID
  * **Keep** the `desktopVersion` which marks the Arcgis PRO target verion for which addin dll libraries have been built
  * **Personnalize** the `Name`, `Description`, `Author` ... fields

**Config.daml** addin configuration file :
```
  <AddInInfo id="{63e68afa-6999-4a28-9a19-4ac5e5f3aedf}" version="0.1a" desktopVersion="2.7.0.26828">
    <Name>ProAppModule3</Name>   
    <Description>ProAppModule3 description</Description>
    <Image>Images\AddinDesktop32.png</Image>
    <Author>datarsense</Author>
    <Company>Acme</Company>
    <Date>25/01/2022 22:30:50</Date>
    <Subject>Framework</Subject>
    <!-- Note subject can be one or more of these topics:
                    Content, Framework, Editing, Geodatabase, Geometry, Geoprocessing, Layouts, Map Authoring, Map Exploration -->
  </AddInInfo>
```

Use the following CI script to build the target `esriAddinX` package from template :
```
mkdir target && cd target
wget https://github.com/datarsense/arcgispro-sample-addin/releases/download/0.1c/ArcgisProToolboxPackage_2.7.0.26828.esriAddinX
unzip ArcgisProToolboxPackage_2.7.0.26828.esriAddinX && rm ArcgisProToolboxPackage_2.7.0.26828.esriAddinX
cp ../Config.daml ./Config.daml
cp ../src/*.pyt ./Toolboxes/toolboxes
rm Toolboxes/toolboxes/sampletoolbox.pyt
zip -r MyArcgisProToolbox_2.7.0.26828.esriAddinX ./
```

## Reference
https://github.com/Esri/arcgis-pro-sdk/wiki/ProGuide-content-and-image-resources#embedding-toolboxes
https://github.com/Esri/arcgis-pro-sdk/wiki/ProGuide-ArcGIS-Pro-Extensions-NuGet