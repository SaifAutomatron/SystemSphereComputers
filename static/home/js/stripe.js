// Your existing JavaScript code

var total = '{{order.get_cart_total}}';

// Render the Stripe button
var stripe = Stripe('ysk_test_51OIH6GHBgDnejRm5rXYoF7gXBVGEycApxU5ADDnpl5401faw5NnVHE5b4JUmeoMTNWrg9Td92SAPZdF6bKHQnArJ00CEzl1cCT');
var elements = stripe.elements();
var style = {
    base: {
        color: '#32325d',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4',
        },
    },
    invalid: {
        color: '#fa755a',
        iconColor: '#fa755a',
    },
};
var card = elements.create('card', { style: style });

card.mount('#card-element');

card.addEventListener('change', function (event) {
    var displayError = document.getElementById('card-errors');
    if (event.error) {
        displayError.textContent = event.error.message;
    } else {
        displayError.textContent = '';
    }
});

var form = document.getElementById('form');

form.addEventListener('submit', function (e) {
    e.preventDefault();
    stripe.createPaymentMethod({
        type: 'card',
        card: card,
    }).then(function (result) {
        if (result.error) {
            var errorElement = document.getElementById('card-errors');
            errorElement.textContent = result.error.message;
        } else {
            // Successful payment, handle the result.paymentIntent
            console.log(result.paymentMethod);
            // Call your function to submit form data
            submitFormData(result.paymentMethod.id);
        }
    });
});
