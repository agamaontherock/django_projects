Django Sample Project
==========

This is a set of Django sample apps



Setting up
-------------------------------------------
    pip install -r requirements.txt

App-specific configurations
-------------------------------------------

## Blog App
#### Sending email
To enable the "Share by Email" feature, you need to create a .env file in the root directory of your project. Below are the variables that must be specified in this file:

    EMAIL_HOST_PASSWORD="<your app password>"
    EMAIL_HOST_USER = "<your email address>"
    DEFAULT_FROM_EMAIL = "<your email address>"

### Social login
#### Google
To enable Google oAuth2.0 specify following parameters in your .env file:

    GOOGLE_OAUTH2_KEY=<>
    GOOGLE_OAUTH2_SECRET=