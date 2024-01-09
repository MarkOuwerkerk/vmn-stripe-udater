import stripe

# Set your Stripe API key
stripe.api_key = ''
# Specify the old and new price IDs
old_price_id = '' # Hier de oude price ID invullen
new_price_id = '' # Hier de nieuwe price ID invullen

# Retrieve all subscriptions
subscriptions = stripe.Subscription.list(limit=473) # de limiet moet het aantal subscriptions zijn
#print(subscriptions.data[0])
subcription = subscriptions.data[3]
items = subcription['items']['data']
print(subcription['id'])
all_subscriptions = []
all_subscriptions.extend(subscriptions.data)

# Check if there are more subscriptions
while subscriptions.has_more:
    # Use the last subscription ID from the current list as starting_after
    starting_after = subscriptions.data[-1].id

    # Make the next request with starting_after to get the next set of subscriptions
    subscriptions = stripe.Subscription.list(starting_after=starting_after)

    # Add the subscriptions to the list
    all_subscriptions.extend(subscriptions.data)
print(len(all_subscriptions))

for subscription in all_subscriptions:
    items = subscription['items']['data']
    for item in items:
        print(item['price']['id'])
        if item['price']['id'] == old_price_id:
                # Update the item with the new price
                item['price'] = new_price_id
    stripe.Subscription.modify(
        subscription['id'],
        items=[{'id': item['id'], 'price': new_price_id} for item in items],
        proration_behavior='none'
        )
print("All subscriptions updated.")
