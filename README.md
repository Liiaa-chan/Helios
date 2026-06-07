# Flask Project Setup Guide

Welcome to the Flask Project! This guide will help you clone and set up the project on your local machine, including activating the virtual environment and installing all dependencies to get you started.

## Prerequisites

Ensure you have the following installed on your system:

-   Python 3.x
-   Git
-   Virtualenv (optional, but recommended)
-   Node js (redesign with tailwindcss)
-   Npm

## Step 1: Clone the repository

Start by cloning the project from GitHub. Run the following command in your terminal:

```
git clone https://github.com/username/project-name.git
```

Replace `username` and `project-name` with the correct repository details.

Navigate to the project directory:

```
cd project-name
```

## Step 2: Set up a virtual environment (optional, but recommended)

To keep your dependencies isolated, it's best to use a virtual environment. If you don't have `virtualenv` installed, install it with the following command:

```
pyhton -m venv <folder_name>
```

`<folder_name>` can be replaced with any name you prefer, such as `venv` or `env`, or any other name you choose.

Now, create and activate your virtual environment:

-   On macOS/Linux:

```
<your_python_directory>
source venv/bin/activate
```

-   On Windows

```
<your_python_directory>
venv\Scripts\activate
```

## Step 3: Install dependencies

With your virtual environment active, install the required dependencies:

```
pip install -r requirements.txt
```

This will install Flask and any other necessary packages.

## Step 4: Install dependencies (Node Modules)

With your virtual environment active, install the required dependencies:

```
npm install
```

This will install necessary packages in node js.

## Step 5: Running node js for tailwindcss (Node Modules)

With your virtual environment active, install the required dependencies:

```
npx tailwindcss -i ./src/input.css -o ./src/output.css --watch 
```

To build simple command you can access package.json and adding this command.

```
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "dev" : "npx @tailwindcss/cli -i ./static/css/style.css -o ./static/dist/output.css --watch"
  },
```

Then you can just running tailwindcss with a simple command like.

```
npm run dev
```
## Step 6: Run the application

Finally, you can run the Flask application with the following command:

```
python <python_file.py>
```

If everything is set up correctly, the application should be accessible at http://127.0.0.1:5000.

