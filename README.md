# Sample Arcgis PRO SDK addin for toolbox packaging

## Usage
Arcgis PRO provides customization capabilities using Python toolbox (PYT). However, these Python toolbox are stored as files in the current Arcgis Project and have to be imported back manually when shared as PYT files to other users or when creating a new Arcgis project.

Arcgis PRO SDK addins provides a simple way to **package and deploy PYT toolbox at large scale** as :
  - They can be deployed from a central location (shared folder) to all Arcgis PRO users
  - Arcgis PRO SDK register PYT toolbox as geoprocessing tools which make them globally available in all Arcgis Projects.

## Packaging a toolbox
Python toolboxes have to be stored in the `Toolboxes\toolboxes` repository of the SDK addin and declared as `AddInContent` in the **.csproj** Visual Studio project description file to be included in the addin at build time.

** Directory structure **
```
\---Toolboxes
    \---toolboxes
            sampletoolbox.pyt
 ```

**Toolbox path declared as `AddInContent` inProAppModule3.csproj **
```
  <ItemGroup>
    <AddInContent Include="Toolboxes\toolboxes\sampletoolbox.pyt" />
  </ItemGroup>
```

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


## Reference
https://github.com/Esri/arcgis-pro-sdk/wiki/ProGuide-content-and-image-resources#embedding-toolboxes
https://github.com/Esri/arcgis-pro-sdk/wiki/ProGuide-ArcGIS-Pro-Extensions-NuGet