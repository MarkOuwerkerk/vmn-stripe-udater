import argparse
import stripe

stripe.api_key = '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'
old_price_id = '' # Hier de oude price ID invullen
new_price_id = '' # Hier de nieuwe price ID invullen

def get_total_subscription_count():
    total_count = 0
    subscriptions = stripe.Subscription.list(limit=100)  # Adjust the limit as needed
    total_count += len(subscriptions.data)

    while subscriptions.has_more:
        subscriptions = stripe.Subscription.list(
            limit=100,
            starting_after=subscriptions.data[-1].id
        )
        total_count += len(subscriptions.data)

    return total_count


def update_subscriptions(total_subscriptions):
    # Set your Stripe API key
    if(new_price_id != ''):
        # Retrieve all subscriptions
        subscriptions = stripe.Subscription.list(limit=total_subscriptions)
        all_subscriptions = subscriptions.data

        # Check if there are more subscriptions
        while subscriptions.has_more:
            # Use the last subscription ID from the current list as starting_after
            starting_after = subscriptions.data[-1].id

            # Make the next request with starting_after to get the next set of subscriptions
            subscriptions = stripe.Subscription.list(starting_after=starting_after)

            # Add the subscriptions to the list
            all_subscriptions.extend(subscriptions.data)

        for subscription in all_subscriptions:
            items = subscription['items']['data']
            for item in items:
                if item['price']['id'] == old_price_id:
                    # Update the item with the new price
                    item['price']['id'] = new_price_id

            stripe.Subscription.modify(
                subscription['id'],
                items=[{'id': item['id'], 'price': new_price_id} for item in items],
                proration_behavior='none'
            )

        print("All subscriptions updated.")
    else:
        print("please specify the new_price_id")

def old(total_subscriptions):
        # Set your Stripe API key

    # Retrieve all subscriptions
    subscriptions = stripe.Subscription.list(limit=total_subscriptions)
    all_subscriptions = subscriptions.data

    # Check if there are more subscriptions
    while subscriptions.has_more:
        # Use the last subscription ID from the current list as starting_after
        starting_after = subscriptions.data[-1].id

        # Make the next request with starting_after to get the next set of subscriptions
        subscriptions = stripe.Subscription.list(starting_after=starting_after)

        # Add the subscriptions to the list
        all_subscriptions.extend(subscriptions.data)
    counter =0
    for subscription in all_subscriptions:
        items = subscription['items']['data']
        for item in items:
            if item['price']['id'] == old_price_id:
                counter+=1
    print(str(counter) + " subscriptions have the old price ID")
    


def main():
    parser = argparse.ArgumentParser(description='Update subscriptions.')
    parser.add_argument('--mode', required=True, help='update to update and old to see how many subscriptions have the old price ID')
    args = parser.parse_args()

    total_subscriptions = get_total_subscription_count()
    print(f'Total subscriptions: {total_subscriptions}')

    if args.mode == 'update':
        update_subscriptions(total_subscriptions)
    if args.mode == 'old':
        old(total_subscriptions)

if __name__ == "__main__":
    main()