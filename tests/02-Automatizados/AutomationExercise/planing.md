


Planing tests para Automation Exercise

**1.- POMs necesarios:**

    - HomePage
    - SignUpPage
    - LoginPage
    - ProductPage
    - CartPage
    - CheckoutPage

**2.- Fixtures necesarias:**

    - Fixture home page
    - Fixture registered user
    - Fixture logged in user


**3.- Tests a automatizar:**

    -Test Case 1: Register User                                     <---Primero>
    -Test Case 2: Login User with correct email and password        <---Segundo>
    -Test Case 3: Login User with incorrect email and password      <---Tercero>
    -Test Case 4: Logout User                                       <---Cuarto>
    -Test Case 5: Register User with existing email                 <---Quinto>
    -Test Case 6: Contact Us Form
    -Test Case 7: Verify Test Cases Page
    -Test Case 8: Verify All Products and product detail page
    -Test Case 9: Search Product
    -Test Case 10: Verify Subscription in home page
    -Test Case 11: Verify Subscription in Cart page
    -Test Case 12: Add Products in Cart                              <--Sexto>
    -Test Case 13: Full checkout process                             <---Séptimo>
    -Test Case 14: Verify Product quantity in Cart
    -Test Case 15: Place Order: Register while Checkout
    -Test Case 16: Place Order: Register before Checkout
    -Test Case 17: Place Order: Login before Checkout
    -Test Case 18: Remove Products From Cart
    -Test Case 19: View Category Products
    -Test Case 20: View & Cart Brand Products
    -Test Case 21: Search Products and Verify Cart After Login
    -Test Case 22: Add review on product
    -Test Case 23: Add to cart from Recommended items
    -Test Case 24: Verify address details in checkout page
    -Test Case 25: Download Invoice after purchase order
    -Test Case 26: Verify Scroll Up using 'Arrow' button and Scroll Down functionality
    -Test Case 27: Verify Scroll Up without 'Arrow' button and Scroll Down functionality

**4.- Requisitos:**

    - Uso de constants.py para URLs y datos de prueba
    - Uso de fixtures para setup y teardown
    - Screenshots para errores
    - Reportes de ejecución
    - Datos de prueba separados, no hard-coded
    - Tests independientes, sin orden requerido