from schemas import CitizenRequest


request = CitizenRequest(
    message="How can I renew my passport?",
    location="Lagos",
    passport_type="renewal"
)


print(request)