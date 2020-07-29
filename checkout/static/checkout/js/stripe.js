// Create a Stripe client.
var stripe = Stripe('pk_test_51Gzgb6Dylq7SXtda0SSiCK2ZyB0YZaymhRH48n084NcO75BUYAcSJs9OSFleBhaO0oqOnDi4nWyFwHO8hb5gvIgd001MYSbJK6');

// Create an instance of Elements.
var elements = stripe.elements();

// Custom styling can be passed to options when creating an Element.
// (Note that this demo uses a wider set of styles than the guide below.)
var style = {
  base: {
    color: '#32325d',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#aab7c4'
    }
  },
  invalid: {
    color: '#fa755a',
    iconColor: '#fa755a'
  }
};

  $("#payment-form").submit(function() {
      var form = this;
      var card = {
          number: $("#id_credit_card_number").val(),
          expMonth: $("#id_expiry_month").val(),
          expYear: $("#id_expiry_year").val(),
          cvc: $("#id_cvv").val()
      };
  
  Stripe.createToken(card, function(status, response) {
      if (status === 200) {
          $("#credit-card-errors").hide();
          $("#id_stripe_id").val(response.id);

          // Prevent the credit card details from being submitted
          // to our server
          $("#id_credit_card_number").removeAttr('name');
          $("#id_cvv").removeAttr('name');
          $("#id_expiry_month").removeAttr('name');
          $("#id_expiry_year").removeAttr('name');

          form.submit();
      } else {
          $("#stripe-error-message").text(response.error.message);
          $("#credit-card-errors").show();
          $("#submit-button").attr("disabled", false);
      }
  });
  return false;
  });

  
// Create an instance of the card Element.
var card = elements.create('card', {style: style});

// Add an instance of the card Element into the `card-element` <div>.
card.mount('#card-element');

// Handle real-time validation errors from the card Element.
card.on('change', function(event) {
  var displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

var form = document.getElementById("payment-form");
form.addEventListener("submit-button", function(event) {
  event.preventDefault();
  // Complete payment when the submit button is clicked
  payWithCard(stripe, card, data.clientSecret);
});


// Calls stripe.confirmCardPayment
// If the card requires authentication Stripe shows a pop-up modal to
// prompt the user to enter authentication details without leaving your page.
var payWithCard = function(stripe, card, clientSecret) {
  loading(true);
  stripe
    .confirmCardPayment(clientSecret, {
      payment_method: {
        card: card
      }
    })
    .then(function(result) {
      if (result.error) {
        // Show error to your customer
        showError(result.error.message);
      } else {
        // The payment succeeded!
        orderComplete(result.paymentIntent.id);
      }
    });
};
/* ------- UI helpers ------- */
// Shows a success message when the payment is complete
var orderComplete = function(paymentIntentId) {
  loading(false);
  document
    .querySelector(".result-message a")
    .setAttribute(
      "href",
      "https://dashboard.stripe.com/test/payments/" + paymentIntentId
    );
  document.querySelector(".result-message").classList.remove("hidden");
  document.querySelector("button").disabled = true;
};
// Show the customer the error from Stripe if their card fails to charge
var showError = function(errorMsgText) {
  loading(false);
  var errorMsg = document.querySelector("#card-error");
  errorMsg.textContent = errorMsgText;
  setTimeout(function() {
    errorMsg.textContent = "";
  }, 4000);
};