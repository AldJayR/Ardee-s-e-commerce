# ARDEE'S: RESTAURANT APP
#### Video Demo:  <https://www.youtube.com/watch?v=N7bSaIYVkkI&feature=youtu.be>
#### Description:
This is a restaurant ordering website that has HTML, CSS, JavaScript, Bootstrap, Python, SQL (from SQLite3) and uses Flask. On the homepage, there are ten (10) food options that you can order. There's a nice carousel from Boostrap that has three images. I took some templates from Canva to make this like a real restaurant.

Ardee is simply just the name of a close friend, I took inspiration from Wendy's since they sound similar. The logo on the navigation bar is made by him. Credits to him.

Let's go to the homepage (index.html):
    On the homepage, we have a navigation bar that links you to the homepage and to the contact us footer. There, you'll find two social links, which doesn't really link to anything as Ardee's is not a real restaurant.

    There's a login page, where you can login, more on that later.

    We have our menu, which is dynamically generated using Jinja2 loops from a SQL table. It is organized in cards provided by Bootstrap. You can see the image of the food, the name, the price and the description. There's also a button that allows you to add the item of your choosing to your own cart.

    I was a bit hesitant on whether to have 10 or 12 foods to make the cards symmetrical, but I went for 10, since I feel like it's easier.

Now, let's go to the login page (login.html):
    This is just a simple login page, no frills or anything. It allows the user to login with the username they've signed up with and a password. There's also a link to resetting your password (although not implemented) and registering an account (More on that later).

    I had some trouble with the flash feature of flask not showing up on the page because I wasn't really experienced with it. But ultimately, I managed through.

    Most of the code here, I gathered from PSET9's "FINANCE". That was really the gateway for me into user authorizatization and stuff.

    There's extra validation here, if you entered the wrong username or password, you don't log-in. Simple as that.

Now, onto the registration page(register.html)
    Here, it's just a simple registration form. It asks you for a username, email, password and a confirmation password. There's also server-sided validation here so that the client just doesn't "hack" there way into the server or use SQL injection attacks. I think I've managed to sanitize my data inputs correctly.

    Most of the code here, I borrowed from my own implementation of the registration route in PSET9's "FINANCE". I really had fun implementing the registration route there so I had fun implementing it there too.

    I tried using Flask-Mail here for email verification, but whenver it does send an email, it brings out a localhost link which my browser doesn't load, so I can't really verify my emails, but nonetheless, you can still use your account despite it not being verified.

Now, onto the cart page(checkout.html):
    When developing this, this felt like the climax of my final project. I had to get some help since I was still unfamiliar with Asynchronous JavaScript. Despite me, having previous programming experience before CS50 which helped me with the problem sets SO MUCH (I had some previous experience with JavaScript and C++ already before I started CS50x), I was still unfamiliar with Asynchronous JavaScript, so I really had to resort to the duck and ChatGPT for it. (Add "Understanding Asynchronous JS to my TO-DO LIST")

    Each cart item is rendered dynamically from the shopping_cart table from my database "restaurants.db". What's rendered here is the price, the name, the item quantity. It's rendered dynamically. And the info, their data, can be updated by the increase and decrease buttons which update them asynchronously, in real time using AJAX. You can delete items, increase their quantity amount, etc.

    There's the subtotal tab, which calculates the subtotal and items. Nothing much happening here.

    Then there's the checkout button which leads you.. TO THE CHECKOUT PAGE!

Checkout page(checkout.html):
    Here, it's just a simple form that asks you for personal info. Since I do not have an actual business permit nor is this an actual restaurant, I cannot accept payments. But I will in the future, might add a payment option, like through card, cash-on-delivery and GCash (which is a mobile wallet app here in the Philippines)

    There's some validation here, if any of the fields are not filled out or valid, it prompts you again to fill out the right info.

    If you fill out the right info, success! You have ordered your items! And it redirects you back to the homepage

layout.html:
    This is just my page where my other pages will extend from. It links to Bootstrap, Font Awesome and my own written script.js.

static:
    this just includes some images that i included in my carousel. Nothing much to see here.

This was CS50x and this is my final project
