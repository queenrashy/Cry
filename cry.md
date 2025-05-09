**Endpoint**: /signup

**Methods**: POST

**Authentication Require**: No

**Description**:
	Registers a new user by validating the email, checking uniqueness, enforcing password strength, generating username and profile image, and saving the new user to the database.

**Request Headers**:
	Content-Type: application/json

**Request Body Parameters**:

| Field    | Type   | Required | Description                                          |
| -------- | ------ | -------- | ---------------------------------------------------- |
| email    | string | Yes      | User's email. Must be a valid and unique email.      |
| password | string | Yes      | User's password. Must be at least 8 characters long. |

**Example Request**:
json:
```
{
"email": "user@gmail.com",
"password": "strongpassword123"
}
```

**Successful Response**:
1. Status Code: 200 Ok
2. Content:
json:
```
{
"success": true,
"Created" : "Account created Successfully."
}
```


| Scenario              | Status Code | Error Message (json)                                          |
| --------------------- | ----------- | ------------------------------------------------------------- |
| Invalid Email         | 400         | error: Please enter a valid email address                     |
| Email Already Exists  | 400         | error: Email already exists                                   |
| Invalid Password      | 400         | error: Password is invalid, please enter 8 or more characters |
| Internal Server Error | 400         | error: User signup error: <error_message>                     |

**Internal Notes**:
1. ==Username==: Randomly generate using random_username()
2. ==Database==: New user added to the User table
3. ==Password==: Stored securely using set_password(password)
4. ==Profile Image==: Randomly generated and saved to static/uploads/<username>.png


--login--
**Endpoint**:
	/login

**Method**:
	GET

**Description**:
	log in with email and password. Returns JWT token on successful login and deletes any previously stored token.

**Request body**:
json:
```
{
	"email": "adebisiqueen231@gmail.com",
	"password": "1234567"
}
```

**Validation Rules**:
1. ==email==: required, must be valid email format, must already exists in the database.
2. ==password==: required, must match the user's saved password.

**Response**:
json:
```
{
"success": True,
"token": "Jwt_token_here"
}
```

Status code: 200 Ok

**Error Response**:

| Scenario                  | Status Code | Error Message                          |
| ------------------------- | ----------- | -------------------------------------- |
| Missing email or password | 400         | Please enter a valid email or password |
| Invalid email format      | 400         | Please enter a valid email address     |
| Email not found           | 401         | User with this email does not exist    |
| Incorrect password        | 400         | Invalid email or password              |


-- logout --
**Endpoint**:
	/logout

**Method**:
	GET

**Description**:
	Log out the currently authenticated user. Deletes the active JWT token and sends a logout confirmation email to the user's registration email address.

**Authentication Required:**
	Yes- JWT Via ==token==


**Request body**:
	No request body required. The JWT token must be sent in the headers for authentication.

Response:
json:
```
{
	"success": true,
	"message": "User logout successfully"
}
```

Error Responses:

| Scenario              | Status Code | Error Message(JSON)                         |
| --------------------- | ----------- | ------------------------------------------- |
| Missing/Invalid Token | 401         | Authentication required or token is invalid |


-- forget password --
**Endpoint**:
	/forget-password

**Methods**:
	POST

**Description**:
	Initiates the password reset process by generating a unique token and sending it to the user's registered email address.

**Request Body**:
json:
```
{
"email": "adebisiqueen@gmail.com"
}
```

**Validation Rules**:
	==email==: required, must be a valid email format, and must exist in the database.

**Response**:
json:
```
{
"success": true,
"message": "Password reset email sent"
}
```
Status code: 200 ok

**Error Response**:

| Scenario             | Status Code | Error Message                       |
| -------------------- | ----------- | ----------------------------------- |
| Missing email        | 400         | Please enter email                  |
| Email not registered | 400         | User with this email does not exist |


-- reset password --
**Endpoint**:
	/reset-password

**Method**:
	POST

**Description**:
	Allows users to reset their password using a valid reset token sent to their email.

Request Body:
json:
```
{
"token": "ADKDF34MCM",
"new_password" "Queen33tti"
"comfirm_password" "Queen33tti"
}
```

Validation Rules:
1. ==token==: required, must exist in database, must not be previously used.
2. ==new_password==: reuqired, must match ==comfirm_password==, minimum 8 characters (if enforced).
3. ==confirm_password==: must match ==new_password==.

**Response**:
json:
```
{
"success": true,
"message": "Password reset successfully"
}
```
Status Code: 200 OK

**Error Responses:**

| Scenario                       | Status Code | Error Message(JSON)         |
| ------------------------------ | ----------- | --------------------------- |
| Missing or mismatched password | 400         | Password does not match     |
| Missing token                  | 400         | Please enter token          |
| Invalid token                  | 400         | Invalid token               |
| Token already used             | 400         | Token has been used already |
| User not found                 | 400         | User not found              |


delete account --
**Endpoint**:
	/<int:did>

**Methods**:
	DELETE

**Authentication Required:**
	Yes- JWT Via ==token==

Description:
	Deletes a user account by ID if it exist. Returns confirmation upon successful deletion.

**Path Parameter**:

| Parameter | Type | Description              |
| --------- | ---- | ------------------------ |
| did       | int  | ID of the user to delete |

**Success Reponse**:
```
{
"done": true,
"message": "adebisiqueen@gmail.com Account deleted successfully!"
}
```

**Error Response**:

| Scenario            | Status Code | Error Message(JSON) |
| ------------------- | ----------- | ------------------- |
| User does not exist | 404         | User does not exist |



**Endpoint**: 
	/post-story

**Method**:
	POST

**Authentication**:
	Yes- JWT Via ==token==

**Description**:
	This endpoint allows authenticated users to post a story. If the story content is provided, a new post is created and added to the database. If no content is provided, an error is returned.

**Request Body**:
json:
```
{
"post": "Your story content here"
}

```

**Response**:
	**Satus code**: 200 Ok
json:
```
{
"done" true,
"message": "Post successful"
}
```


| Scenrio       | Status | error message(Json) |
| ------------- | ------ | ------------------- |
| invalid input | 400    | error: input words  |

--post comment--
**Endpoint**:
	/comment

**Method**:
	POST

**Authentication**:
	Yes- JWT Via ==token==

**Description**:
	This endpoint allows authenticated users to post a comment on an existing post. Both the ==post_id== and ==content== fields are required. If the post does not exist, an error is returned.


**Request Body**:
json:
```
{
"post_id": "1",
"content": "your comment here"
}

```

**Response**:
	**Satus code**: 200 Ok
json:
```
{
"done": true,
"message": "Comment added successfully"
}

```


| Scenrio             | Status Code | error message (json)                    |
| ------------------- | ----------- | --------------------------------------- |
| Invalid input       | 400         | error: Post ID and content are required |
| post does not exist | 400         | error: Post not found                   |
