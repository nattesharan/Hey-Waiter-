# Hey-Waiter-
A waiter caller web application that allows restaurant patrons to easily call a waiter to their table.

We will dive even deeper into the Flask world, taking a look at some Flask extensions
to help us with user account control and web forms, and we'll look at how to use
template inheritance in Jinja, too. We'll also use the Bootstrap frontend framework so
that we don't have to do so much of the HTML and CSS code from scratch.We will be using MongoDB as our database.
The application works as follows:
* The restaurant manager signs up a new account on our web application
* The restaurant manager provides basic information about how many tables the restaurant has
* The web application provides a unique URL for each table
* The restaurant manager prints out these URLs and ensures that the relevant URL is easily accessible from
each table
* The restaurant staff should be able to log into the web application from a centralized screen and see a simple notification page.
* Some patrons would want service and visit the URL relevant to their tableon a smartphone, so this should be possible.
* In real time, the waiters should see a notification appear on a centralized
screen. The waiter will then acknowledge the notification on the screen and
attend to the patrons.
* If more notifications arrive before the first one is acknowledged, the later ones should appear beneath the earlier ones.