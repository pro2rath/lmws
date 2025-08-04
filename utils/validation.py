# lwms/utils/validation.py

def is_valid_aadhaar(number_str):
    """Checks if the Aadhaar number is 12 digits long."""
    return number_str.isdigit() and len(number_str) == 12

def allowed_file(filename, allowed_extensions):
    """Checks if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions