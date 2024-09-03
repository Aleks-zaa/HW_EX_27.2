from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from users.models import User, Donation
from users.serializers import UserSerializer, DonationSerializer
from users.services import convert_curr, create_stripe_price, create_stripe_sessions


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class DonationCreateAPIView(CreateAPIView):
    serializer_class = DonationSerializer
    queryset = Donation.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user_d=self.request.user)
        # amount_in_dollar = convert_curr(payment.amount)
        # price = create_stripe_price(amount_in_dollar)
        price = create_stripe_price(payment.amount)  # assuming payment.amount is in USD or EUR, adjust this line as needed.  # Create a Stripe Price for the donation amount.  # Create a Stripe Session with the Price and return the session ID and payment link.  # Store the session ID and payment link in the Donation model.  # The payment link can be used to redirect users to the Stripe payment page.  # After the user pays, the payment status can be updated in the Donation model.  # Note: The conversion of currency, creation of Stripe Price, and creation of Stripe Session should be handled in a separate service or a separate function for better code organization.  # Also, the payment link should be generated dynamically based on the user's preferred currency and the donation amount.  # The payment link should be stored securely and not exposed in the API response.  # Finally, the payment link should be returned in'
        session_id, payment_link = create_stripe_sessions(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()

