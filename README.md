# Road Map Geometry
## Website 
[Road Map Geometry - Deployed Website](https://road-geometry-software-dev.onrender.com/)
## Overview
Road Map Geometry is a web-based application designed to calculate and display geometric properties of roads, such as the radius of curvature, road names, points of tangency, and points of curvature. This project utilizes Django and integrates data from OpenStreetMap to provide detailed and accurate road analysis.

![Screenshot (314)](https://github.com/chiranjivikeshav/Road_Geometry_Software_Dev/assets/117706982/cee4a416-59e0-4002-9984-a1f90c8dedd3)

## Features
- **Radius of Curvature**:   Radius of the curve on which the point lies.
- **Road Name**:   Dynamically retrieves and displays the name of the road from OpenStreetMap for the point.
- **Point of Tangency**:   The point of tangency is the end of the curve. 
- **Point of Curvature**:   The point of curvature is the point where the circular curve begins.

## Prerequisites for Installation

Before you begin, ensure you have met the following requirements:

- **Python 3.10**: Make sure Python 3.10 is installed on your machine. This version ensures compatibility with all the dependencies listed in the `requirements.txt` file. You can download Python 3.10 from the [official Python website](https://www.python.org/downloads/release/python-3100/).
- **Git**: Installed on your machine to clone the repository. Cloning is the process of creating an identical copy of a repository, So instead of making a copy of a project using the git command, you can directly download it from GitHub and therefore you don't need to install Git. Otherwise, you can download Git from the [official Git website](https://git-scm.com/downloads).
How to clone or download the project is in the next section.
  
- **Internet Access**: Necessary for pulling road data from OpenStreetMap and other functionalities that may require online access.
### Note: If you want to contribute to this project then see the contribution section before installation. The contribution section is described below.
## Installation
Follow these detailed steps to set up the Road Map Geometry project locally:
1. Create a folder or go to an existing folder.
2. Clone the repo if you have installed Git, Otherwise follow the next steps:
   - Open a terminal (Command Prompt or PowerShell or any code editing software like VS Code, which provides a terminal) 
    corresponding to the folder you have opened.
   - Run below command in the terminal<br>
     `git clone https://github.com/chiranjivikeshav/Road_Geometry_Software_Dev.git`.
3. Download the ZIP File if you have not installed Git: 
   - Go to the [GitHub page](https://github.com/chiranjivikeshav/Road_Geometry_Software_Dev) of the Road Map Geometry 
     repository in your web browser.
   - Find the "Code" Button and Click on this button to open a dropdown menu.
   - In the dropdown menu, there will be an option to "Download ZIP." Clicking this will download a .zip file of the current 
     state of the repository to your computer.
   - Once the download is complete, locate the ZIP file in the folder that you have selected in step 1.
   - Then Extract the zip file.
  
4. Navigate to the project directory: Run this command in the terminal `cd Road_Geometry_Software_Dev`.
5. Set Up a Python Virtual Environment (Optional)
   - It’s recommended to create a virtual environment for Python projects to manage dependencies effectively. If you want to 
     set it up then run the following commands in your terminal Otherwise skip this step.
   - Install virtualenv if it's not installed `pip install virtualenv`.
   - Create a virtual environment `virtualenv venv`.
   - Activate the virtual environment if you are using Windows `venv\Scripts\activate`.
   - Activate the virtual environment if you are using On MacOS/Linux `source venv/bin/activate`.

3. Install all the dependencies which will be required in this project: Run command `pip install -r requirements.txt`.

4. Run Local server: Use the command `python manage.py runserver`.

6. Visit http://127.0.0.1:8000/ in your web browser to start using the application.
## Usage
After setting up the project, you can use it by navigating to the web interface where you can enter the road you wish to analyze. The application will then display the geometric characteristics of the road along with a visual pop-up.
## Built With
- **Django** - The web framework used.
- **OpenStreetMap** - Source of road data.
  
## Contributing
Contributions are what makes the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated. Make sure Git is installed on your machine. 

1. Fork the Project: You can Folk the repository form [GitHub page](https://github.com/chiranjivikeshav/Road_Geometry_Software_Dev). There is a folk button on the top-right corner.
2. Follow the installation process which is described above. Make sure you clone the repository instead of downloading it and 
now for cloning the command is <br>
`git clone https://github.com/YOUR_GITHUB_USERNAME/Road_Geometry_Software_Dev.git`.
4. Create the Feature to which you want to contribute.
5. Add your change using (`git add . `).
6. Commit your Changes (`git commit -m "commit message"`).
7. Push to the Branch (`git push origin main`).
8. Open a Pull Request.
## License
This project is licensed under the GNU General Public License - see the [LICENSE](https://github.com/chiranjivikeshav/Road_Geometry_Software_Dev/blob/main/LICENSE) file for more details.

## Acknowledgments
- Thanks to the OpenStreetMap contributors for providing free access to road data.
- Thanks to all contributors who have helped to extend and improve this project.
