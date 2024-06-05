
from app import create_app  

app = create_app()  # unpack both returned values

# this check ensures that the following code runs only when you execute this script directly (like python run.py)
# prevent certain code from being run accidentally when the module is imported.
if __name__ == "__main__":
    app.run(debug=True) # run the application server in debug mode
