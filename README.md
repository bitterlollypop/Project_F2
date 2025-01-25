This is a simple online store built with Python that requires users to log in to access its services. 
Regular customers have access to customer services, while admins can access the admin menu. 
Customers can browse products, add them to their shopping cart, view prices, and finalize their purchase. After completing a purchase, customers can choose whether to generate an invoice. The system then reduces both the user's account balance and product stock. Customers can also update their profiles. 
Admins, on the other hand, can update store products and monitor user activity.


The challenge of this project:
One of the main challenges in this project was that customers could not finalize their purchases. They were unable to complete their purchase because the login system had a variable initialization issue, which prevented proper user identification. As a result, the website could not deduct money from the user's account. This issue was later fixed by properly initializing the variable and ensuring accurate user identification.
