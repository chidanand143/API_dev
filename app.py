from flask import Flask, request, jsonify

# --- In-Memory Data Store ---
# Using a dictionary to store users, where the key is the user_id
# and the value is a dictionary containing the user's details (name, email).
users = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"}
}
next_user_id = 3 # Start the next ID after the initial users

app = Flask(_name_)

# Helper function to get the next available ID
def get_next_id():
    global next_user_id
    current_id = next_user_id
    next_user_id += 1
    return current_id

# -----------------------------------------------------------------
# 1. POST /users (Create a new user)
# -----------------------------------------------------------------
@app.route('/users', methods=['POST'])
def create_user():
    """
    Creates a new user. Expects JSON data with 'name' and 'email'.
    """
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
        
    data = request.get_json()

    if 'name' not in data or 'email' not in data:
        return jsonify({"message": "Missing 'name' or 'email' in request body"}), 400

    new_user_id = get_next_id()
    new_user = {
        "name": data['name'],
        "email": data['email']
    }
    
    users[new_user_id] = new_user
    
    # Return the created user with their new ID
    return jsonify({
        "id": new_user_id,
        "name": new_user["name"],
        "email": new_user["email"]
    }), 201 # 201 Created

# -----------------------------------------------------------------
# 2. GET /users (Retrieve all users) and GET /users/<int:user_id> (Retrieve a specific user)
# -----------------------------------------------------------------
@app.route('/users', methods=['GET'])
def get_all_users():
    """
    Retrieves a list of all users.
    """
    # Format the users dictionary into a list of user objects for the response
    user_list = [{"id": uid, "name": u["name"], "email": u["email"]} for uid, u in users.items()]
    return jsonify(user_list), 200 # 200 OK

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retrieves a single user by ID.
    """
    user = users.get(user_id)
    if user:
        return jsonify({
            "id": user_id,
            "name": user["name"],
            "email": user["email"]
        }), 200
    else:
        return jsonify({"message": f"User with ID {user_id} not found"}), 404 # 404 Not Found

# -----------------------------------------------------------------
# 3. PUT /users/<int:user_id> (Update an existing user)
# -----------------------------------------------------------------
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Updates an existing user. Expects JSON data with fields to update ('name' or 'email').
    """
    if user_id not in users:
        return jsonify({"message": f"User with ID {user_id} not found"}), 404
        
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
        
    data = request.get_json()
    
    # Check if there are any fields to update
    if not data:
        return jsonify({"message": "No fields provided for update"}), 400
        
    user = users[user_id]
    
    # Update fields if they exist in the request data
    if 'name' in data:
        user['name'] = data['name']
    if 'email' in data:
        user['email'] = data['email']
        
    # Return the updated user object
    return jsonify({
        "id": user_id,
        "name": user["name"],
        "email": user["email"]
    }), 200

# -----------------------------------------------------------------
# 4. DELETE /users/<int:user_id> (Delete a user)
# -----------------------------------------------------------------
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a user by ID.
    """
    if user_id in users:
        del users[user_id]
        return jsonify({"message": f"User with ID {user_id} deleted successfully"}), 204 # 204 No Content
    else:
        return jsonify({"message": f"User with ID {user_id} not found"}), 404

# Run the application
if _name_ == '_main_':
    # Setting debug=True is good for development
    app.run(debug=True)
