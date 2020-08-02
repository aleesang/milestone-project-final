// A reference to Stripe.js initialized with your real test publishable API key.
var stripePublishableKey = $('#id_stripe_publishable_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);x

// Disable the button until we have Stripe set up on the page
document.querySelector("submit-button").disabled = true;
fetch("/create-payment-intent", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(purchase)
})
  .then(function(result) {
    return result.json();
  })
  .then(function(data) {
    var elements = stripe.elements();
    var style = {
      base: {
          color: '#000',
          fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
          fontSmoothing: 'antialiased',
          fontSize: '16px',
          '::placeholder': {
              color: '#aab7c4'
          }
      },
      invalid: {
          color: '#dc3545',
          iconColor: '#dc3545'
      }
    };

    var card = elements.create('card', {style: style});
    card.mount('#card-element');
    
    // Handle realtime validation errors on the card element
    card.addEventListener('change', function (event) {
        var errorDiv = document.getElementById('card-errors');
        if (event.error) {
            var html = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${event.error.message}</span>
            `;
            $(errorDiv).html(html);
        } else {
            errorDiv.textContent = '';
        }
    });

    var form = document.getElementById("payment-form");
    form.addEventListener("submit-button", function(event) {
      event.preventDefault();
      // Complete payment when the submit button is clicked
      payWithCard(stripe, card, data.clientSecret);
    });
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

var saveInfo = Boolean($('#id-save-info').attr('checked'));
// From using {% csrf_token %} in the form
var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
var postData = {
    'csrfmiddlewaretoken': csrfToken,
    'client_secret': clientSecret,
    'save_info': saveInfo,
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
  document.querySelector("submit-button").disabled = true;
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

// Show a spinner on payment submission
var loading = function(isLoading) {
  if (isLoading) {
    // Disable the button and show a spinner
    document.querySelector("submit-button").disabled = true;
    document.querySelector("#spinner").classList.remove("hidden");
    document.querySelector("#button-text").classList.add("hidden");
  } else {
    document.querySelector("submit-button").disabled = false;
    document.querySelector("#spinner").classList.add("hidden");
    document.querySelector("#button-text").classList.remove("hidden");
  }
};