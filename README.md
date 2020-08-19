# Milestone Project 4 Django Project - Tech & Co

### Introduction
The project is an ecommerce site for an online store called Tech & Co. The website aims to bring you fun, but practical tech accessories to empower you in this tech world, with a range of tech accessories for the modern girl.

## UX
The website focuses on two types of users:
1. `Guests/New Customer` will be able to view the store's home page, place a custom order enquiry, view and search for different tech products, and add products to the shopping bag. 
2. `Existing/Returning Customer` will heed to register for an account if they plan on checking out their items in their bag, and view their profile for their order history.

The website's purpose is to provide a link to girls and women who love all things tech, and want to own some aesthetically pleasing tech accessories that also is practical for every day use.

The target audience for this website are girls and women who love gadgets and are looking for funky, fun and practical tech to own and use on the daily.

### User Stories

- Please see link here to [User Stories]("") and [Wireframes]("").

## Features
Some base features:
+ Account CRUD functionality
+ Browsing and filtering products by category, filter by search and by details
+ Storing products in the session for return users and for new users.
+ Authentication required for purchasing products from the site.

**Existing Features**

#### For users who are not logged in
### Existing Features

#### [Home Page](https://tech-and-co.herokuapp.com/)
This is the landing page for the online tech accessories store, which displays the navigation menu, a free delivery banner, the hero image with an enquiry form button linked, New Products to Tech & Co, and the footer with a brief description of the company, and navigation links. 

#### [Hero Banner: Custom Order Form Button](https://tech-and-co.herokuapp.com/customorder/customorder/)
Order Form for new and existing users to request custom made products.
The following needs to be filled in:
- Custom Item Request
- User's Email
- Describe Request via Text Area
- Send Button

#### [New In Tech Products]
New Products to Tech & Co is featured in this section"
- Product Image
- Product Name
- Price
- Shop Now Button (links to shop)

#### [Footer]
Lists:
- About Tech & Co 
- My Account
- Shop Link
- Social Media Links (fake links)
- Download App in the play store icons (fake links)

**Navigation Menu**
#### [Logo](https://tech-and-co.herokuapp.com)
- Links back to home page

#### Search Bar
- A Search bar to type in key search terms you're looking for, and press on magnifying glass button or press enter on keyboard, to search for keyword.

#### [Shop](https://tech-and-co.herokuapp.com/products/)
Takes you directly to the products page, where you can sort product page by Category, Name and Price.

The product categories are:
- **[Accessories](https://tech-and-co.herokuapp.com/products/?category=tech_accessories)**
- **[Apparel](https://tech-and-co.herokuapp.com/products/?category=apparel)**
- **[Bags](https://tech-and-co.herokuapp.com/products/?category=bags)**
- **[Mugs](https://tech-and-co.herokuapp.com/products/?category=mugs)**
- **[Stationery](https://tech-and-co.herokuapp.com/products/?category=stationery)**

When a user clicks on any one of the categories, the page will show only products belonging in that particular categorys. On this page, it will show the same information that is shown on **Products Pagee**.

#### [Product Detail](https://tech-and-co.herokuapp.com/products/3/) - (example)
When a user clicks on the image of the product, the user is taken to a new page with more details of the product:
- Product Image
- Product Name
- Price
- Category
- Brief Description
- Quantity
- Buttons: 
    - Keep Shopping and Add To Bag

#### [Button: Keep Shopping](https://tech-and-co.herokuapp.com/products/) 
Takes you bag to products page

#### [Button: Add To Bag]
Adds product to shopping bag, and a popup appears on top right to confirm your bag has been updated, and shopping bag on navigation menu will update total.

#### [My Account: Register](https://tech-and-co.herokuapp.com/accounts/signup/) 
Sign up for an account with:
- Email
- Confirm Email
- Username
- Password
- Confirm Password
- Sign Up Button

#### [Verify Your Email Address](https://tech-and-co.herokuapp.com/accounts/confirm-email/) 
User will see this page once they sign up for an account, which asks user to check their email and follow link provided to verify their email address. A popup also will appear on top right to confirm.

#### [My Account: Login](https://tech-and-co.herokuapp.com/accounts/login/) 
Promots you to sign up if user doesn't have account, otherise if existing, they may login eitg the following:
- Username
- Password
- Check Box to Remember Me
- Home Button and Sign up button
- Forgot Password Link

#### [Password Reset](https://tech-and-co.herokuapp.com/accounts/password/reset/) 
If user has forgotten password, they will need to enter valid email address and click on Reset My Passwors Button. An email will be sent to the email address provided with a link to reset password.

#### [Change Password](https://tech-and-co.herokuapp.com/accounts/password/reset/key/q-set-password/) 
Only will see link if received email to change password.

#### [Shopping Bag]
This page shows you the items in your shopping bag, along with:
- Product Info
- Product Image
- Product Name
- Product Size (if applicable)
- SKU
- Price
- Quantity (Update and remove links)
- Sub Total
- Bag Total
- Delivery charge
- Final Total
- Keep shopping buttom and Secure Checkout button

#### [Checkout]
Displays checkout form, and shopping bag summary:
**Checkout Form**
- Full Name
- Email
- Phone
- Address
- Alternative Address
- Country
- Town or City
- Postcode
- Checkbox to save delivery information
- Stripe Payment form: Card Number, Month/Year/CVV/Postcode

**Bag Summary**
- Product Info
- Product Image
- Product Name
- Total Price
- Delivery charge
- Final Total
- Keep shopping buttom and Secure Checkout button


#### For users who are logged in
### Existing Features

#### [Home Page](https://tech-and-co.herokuapp.com/)
This is the landing page for the online tech accessories store, which displays the navigation menu, a free delivery banner, the hero image with an enquiry form button linked, New Products to Tech & Co, and the footer with a brief description of the company, and navigation links. 

#### [Hero Banner: Custom Order Form Button](https://tech-and-co.herokuapp.com/customorder/customorder/)
Order Form for new and existing users to request custom made products.
The following needs to be filled in:
- Custom Item Request
- User's Email
- Describe Request via Text Area
- Send Button

#### [New In Tech Products]
New Products to Tech & Co is featured in this section"
- Product Image
- Product Name
- Price
- Shop Now Button (links to shop)

#### [Footer]
Lists:
- About Tech & Co 
- My Account
- Shop Link
- Social Media Links (fake links)
- Download App in the play store icons (fake links)

**Navigation Menu**
#### [Logo](https://tech-and-co.herokuapp.com)
- Links back to home page

#### Search Bar
- A Search bar to type in key search terms you're looking for, and press on magnifying glass button or press enter on keyboard, to search for keyword.

#### [Shop](https://tech-and-co.herokuapp.com/products/)
Takes you directly to the products page, where you can sort product page by Category, Name and Price.

The product categories are:
- **[Accessories](https://tech-and-co.herokuapp.com/products/?category=tech_accessories)**
- **[Apparel](https://tech-and-co.herokuapp.com/products/?category=apparel)**
- **[Bags](https://tech-and-co.herokuapp.com/products/?category=bags)**
- **[Mugs](https://tech-and-co.herokuapp.com/products/?category=mugs)**
- **[Stationery](https://tech-and-co.herokuapp.com/products/?category=stationery)**

When a user clicks on any one of the categories, the page will show only products belonging in that particular categorys. On this page, it will show the same information that is shown on **Products Pagee**.

#### [Product Detail](https://tech-and-co.herokuapp.com/products/3/) - (example)
When a user clicks on the image of the product, the user is taken to a new page with more details of the product:
- Product Image
- Product Name
- Price
- Category
- Brief Description
- Quantity
- Buttons: 
    - Keep Shopping and Add To Bag

#### [Button: Keep Shopping](https://tech-and-co.herokuapp.com/products/) 
Takes you back to products page

#### [Button: Add To Bag]
Adds product to shopping bag, and a popup appears on top right to confirm your bag has been updated, and shopping bag on navigation menu will update total.

#### [My Account: My Profile](https://tech-and-co.herokuapp.com/profile/) 
Takes you bag to your profile page, displaying:
- My Information
    - Username
    - Email
- Order History
    - Order Number
    - Date
    - Time
    - Order Total

#### [Shopping Bag]
This page shows you the items in your shopping bag, along with:
- Product Info
- Product Image
- Product Name
- Product Size (if applicable)
- SKU
- Price
- Quantity (Update and remove links)
- Sub Total
- Bag Total
- Delivery charge
- Final Total
- Keep shopping buttom and Secure Checkout button

#### [Checkout]
Displays checkout form, and shopping bag summary:
**Checkout Form**
- Full Name
- Email
- Phone
- Address
- Alternative Address
- Country
- Town or City
- Postcode
- Checkbox to save delivery information
- Stripe Payment form: Card Number, Month/Year/CVV/Postcode

**Bag Summary**
- Product Info
- Product Image
- Product Name
- Total Price
- Delivery charge
- Final Total
- Keep shopping buttom and Secure Checkout button

#### [Checkout Success]
Confirmation of successful order, with order summary.

### Features Left to Implement

1) To allow users to add ratings and reviews for the products
2) Add subscription for a tech service


## Technologies Used

The following technologies were used in the making of this project.

- [HTML](https://www.w3schools.com/html/) was used for constructing the base of the project.
- [CSS](https://www.w3schools.com/css/) for simple styling.
- [Boostrap](https://getbootstrap.com/) the main CSS framework used to build the responsive front-end design of the website.
- [JQuery](https://jquery.com) was used to enhance website.
- [Google Fonts](https://fonts.google.com/) used as main fonts on website.
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) is the database used to store the music library.
- [Flask](https://www.fullstackpython.com/flask.html) is the framework that was used to route python functions and link to the html pages.
- [Python](https://www.python.org/) was used to build the functions that rendered the songs from the mongodb database.
- [python-dotenv](https://pypi.org/project/python-dotenv/) was used to store configuration in the .env file and add them to the environment variables, separate from my code.
- [flask-share](https://flask-share.readthedocs.io/en/latest/) is used as a means to share any song on social media via the View Song Page. (this suggestion was made by my mentor Seun Owonikoko)
- [Visual Studio Code](https://code.visualstudio.com/) was used to predominately build the code on Mac.
- [GitHub](https://github.com/) was used for version control and repository housing.
- [Heroku](https://heroku.com) was used for the deployment of website.


## Testing
#### Manual Testing
Manual testing conducted were as follows:


#### Technologies Used For Testing
- [HTML Validator](https://validator.w3.org/) 
- [CSS Validator](https://jigsaw.w3.org/css-validator) 
    - -moz-transition
    - webkit-transition
    - -o-transitions


**Browsers and Devices**
- [Google Chrome](https://www.google.com/chrome/) was used predominately for testing and for Inspecting via Development Tools
- [Mozilla Firefox](https://www.mozilla.org/en-US/exp/) was used for testing only
- [Safari](https://www.apple.com/au/safari/) was used for testing only.
- [Samsung Galaxy S10 5g and S20 Ultra](https://www.samsung.com.au) used to test mobile responsiveness
- [iPad mini](https://www.apple.com/au/ipad-mini/) was used to test alternate device responsiveness.
- [MacBook Pro 13 inch 2017](https://support.apple.com/kb/SP754?locale=en_AU) was the main device used for building the project and testing
- [HP Elitebook 14 inch](https://en.wikipedia.org/wiki/HP_EliteBook) was used as another device to check responsiveness

## Deployment
### GitHub Deployment

My code was written using AWS Cloud9. AWS Cloud9 serves as the local repository which was then deployed to GitHub. Whenever a new commit is done to the master branch, the deployed site will be updated accordingly. 

This repository can also be deployed locally by cloning the repository. This can be done by going to the main page of the repository to clone/download directly into the editor of choice by pasting git clone into terminal.

I deployed the site to Github with the following steps:
1. Go to this repository in Github [link](https://github.com/aleesang/milestone-project-final)
2. Click on settings --> Github Pages
3. Select "none" for the Source and then select "master branch"

To deploy the page locally:
1.	Go to the github [link](https://github.com/aleesang/milestone-project-final)
2.	Click on the Clone/download button and copy the URL 
3.	Set up and install your own Stripe and uploadcare accounts, and also install crispy forms
5.	To run the application locally, type `python3 manage.py runserver 8000` in bash

### Heroku Deployment

The website has been deployed to Heroku. <br>

- The following steps are instructions for deployment to Heroku in the terminal:

1. Go to [Heroku](https://dashboard.heroku.com/) and register for an account

2. Install Heroku in your system with this command (for mac users)
 `brew tap heroku/brew && brew install heroku`

3. Install these one by one following using pip3:
````
pip3 install gunicorn 
pip3 install psycopg2
pip3 install Pillow
pip3 install whitenoise
pip3 install dj_database_url
** Additional Installations **
pip3 install boto3
pip3 install django-crispy-forms
pip3 install django-bootstrap-form
pip3 install python-dotenv
pip3 install stripe
pip3 install stripe

````

4. In the `settings.py` file, add Whitenoise to the middleware:
````
MIDDLEWARE = [ 
..... 
'whitenoise.middleware.WhiteNoiseMiddleware'
]
````

5. Create a repository in Github

6. Create a hidden file named `.gitignore` and add `.c9` in the file. Also add the following django files to be ignored taken from [here](https://gitignore.io/api/django)

7. In your terminal, type these commands to add the repository origin from Github:
````
git init 
git add . 
git commit -m "Your commit message" 
````

8. Login to Heroku from your terminal by using this command `heroku login`

9. Create a new app with a unique name with this command `heroku create <app_name>` replacing the <app_name> with a name of your choice

10. To check if the correct github repository and heroku app are connected to this project, use this command: 
`git remote -v`

11. In your app in Heroku in the settings tab, click on the 'Reveal Config Vars' button. Copy the exported variables from the `.bashrc` in Cloud9 over to Heroku Config Vars (omit quotes)

12. The Procfile contains a command that Heroku will run when the app starts. In the root folder, create a file named Procfile. Open the file and put the following:

```
web: gunicorn coffee.wsgi:application
```

where 'coffee' in my project name in this project.


13. Inside the `settings.py` add the URL of the heroku app into the ALLOWED_HOST section (without the https)

```
ALLOWED_HOSTS = ["lzq-django-coffee.herokuapp.com/", "*"]
```

14. Use this command to create a `requirements.txt` file which lists all the required packages needed for this project:
````
pip3 freeze --local > requirements.txt
````

15. At the project directory level, create a `Static` folder, which should  be on the same level as the `manage.py` file. Place some files inside here like images or text files

16. Add STATIC_ROOT to your settings.py file
We need this for Whitenoise to work (so that it can serve static files properly):

```
milestone_project_final/settings.py
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

Make sure when you use static files in your template, you make use of the {% static .... %} helper.

Example
```
{% load static %}
<img src="{% static "images/hi.jpg" %}" alt="Hi!" />
```

17. Commit all files to Heroku with these commands
````
git add . 
git commit -m "deploy to Heroku" 
git push heroku master
````

18. To use the PostgresSQL database, type this to your terminal 
````
heroku addons:create heroku-postgresql
````

19. To check the URL to the database created, run this command
`heroku config` and copy this URL to be used later

20. In the `.bashrc` file, add the following
`export DATABASE_URL="database_url"` and restart the bash terminal

21. In the `settings.py` add `import dj_database_url` after all the other import statements

22. In the `settings.py` file, comment out the `DATABASES` section and add the URL copied from Heroku here
````
DATABASES = {'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))}
````

23. Save and restart the terminal

24. Make migrations with this command
````
python3 manage.py makemigrations
python3 manage.py migrate
````

25. Commit all files to Heroku with these commands
````
git add . 
git commit -m "Updated settings.py" 
git push heroku master
````

26. Make a superuser with this command
`python manage.py createsuperuser`

27. At the very top right hand side of the page in Heroku, click "Open App". You will now be able to view the project in Heroku


## Credits

1) Images 

2) Product images, names and descriptions taken from [illy]()

3) [Stack Overflow](https://stackoverflow.com/)


### Acknowledgements
A big thanks to the following for their support and guidance on this project.
- **Seun Owonikoko** - Mentor on this project who was extremely encouraging, provided many helpful tips, and guidance and suggestions for consideration.
- **Code Institute** - Re-visited Python modules to help direct me on how to create the functionality of this project.
