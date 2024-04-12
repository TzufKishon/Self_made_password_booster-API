from flask import Flask, request, jsonify
from flasgger import Swagger
import random
import string

app = Flask(__name__)
Swagger(app)

latest_password = None

def is_password_strong(password):
    """Check if the password meets the criteria for being strong."""
    return (len(password) >= 8 and
            any(char.isdigit() for char in password) and
            any(char.isupper() for char in password) and
            any(char.islower() for char in password) and
            any(char in string.punctuation for char in password))

def improve_password(password):
    """Improve the password until it meets the criteria for being strong."""
    while not is_password_strong(password):
        password += (random.choice(string.ascii_uppercase) +
                     random.choice(string.ascii_lowercase) +
                     random.choice(string.digits) +
                     random.choice(string.punctuation))
    return password

@app.route('/generate_password', methods=['POST'])
def generate_password():
    """
    Generate a Strong Password
    ---
    tags:
      - Password Operations
    parameters:
      - name: password
        in: body
        schema:
          type: object
          properties:
            password:
              type: string
              example: weakpass
        required: true
        description: Password to be evaluated or improved
    responses:
      200:
        description: A strong password
        schema:
          type: object
          properties:
            password:
              type: string
    """
    global latest_password  # Refer to the global variable to update it
    received_data = request.json
    password = received_data.get('password', '')

    improved_password = improve_password(password) if not is_password_strong(password) else password
    latest_password = improved_password  # Update the latest_password variable

    # Return the improved or original password without an ID
    return jsonify({'password': improved_password}), 200

@app.route('/get_password', methods=['GET'])
def get_password():
    """
    Get the Latest Generated Password
    ---
    tags:
      - Password Operations
    responses:
      200:
        description: The most recently generated strong password
        schema:
          type: object
          properties:
            password:
              type: string
      404:
        description: No password has been generated yet
    """
    if latest_password is not None:
        return jsonify({'password': latest_password}), 200
    else:
        return jsonify({'message': 'No password has been generated yet.'}), 404

if __name__ == '__main__':
    app.run(debug=True ,host="0.0.0.0", port=8089)
