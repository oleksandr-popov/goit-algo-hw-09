import timeit

# Define the available coin denominations
denominations = [50, 25, 10, 5, 2, 1]


def find_coins_greedy(amount):
    """
    Finds the coin count using a simple greedy approach.
    It takes as many of the largest coin as possible, then moves to the next largest.
    """
    coin_counts = {}
    remaining_amount = amount
    
    # Iterate through denominations from largest to smallest
    for coin in denominations:
        if remaining_amount >= coin:
            # Calculate how many of the current coin can be used
            count = remaining_amount // coin
            coin_counts[coin] = count
            
            # Update the remaining amount
            remaining_amount %= coin
            
    return coin_counts


def find_min_coins(amount):
    """
    Finds the minimum number of coins for a given amount using Dynamic Programming.
    It builds up the solution from 1 up to the target amount.
    """

    # min_coins[x] stores the minimum number of coins needed to make amount x
    # We use amount + 1 size because we index from 0 up to 'amount'.
    min_coins = [0] + [float("inf")] * amount
    
    # coin_count[x] stores the actual dictionary of coins used to make amount x
    coin_count = [{} for _ in range(amount + 1)]

    # Iterate through each coin denomination
    for coin in denominations:
        # Iterate through all amounts from the coin's value up to the target amount
        for x in range(coin, amount + 1):
            
            if min_coins[x - coin] + 1 < min_coins[x]:
                # Update the minimum number of coins for amount x
                min_coins[x] = min_coins[x - coin] + 1
                
                # Update the actual coin composition for amount x
                # Copy the coin composition for the remainder (x - coin)
                coin_count[x] = coin_count[x - coin].copy()
                
                # Increment the count of the current coin
                coin_count[x][coin] = coin_count[x].get(coin, 0) + 1
    return coin_count[amount]


if __name__ == "__main__":
    # Amounts to test
    amounts_to_test = [10, 55, 113, 207, 505, 1001]
    results = []
    
    # Number of times to run each function for accurate timing
    NUM_RUNS = 1000

    for amount in amounts_to_test:
        # Time the Greedy function
        time_greedy = timeit.timeit(
            lambda: find_coins_greedy(amount), 
            number=NUM_RUNS
        )
        
        # Time the Dynamic Programming function
        time_dp = timeit.timeit(
            lambda: find_min_coins(amount), 
            number=NUM_RUNS
        )
        
        results.append([amount, time_greedy, time_dp])

    # Print the results in a formatted table
    print("\nPerformance Comparison (1000 runs):")
    print("-" * 43)
    print(" Amount | Greedy Time (s)| DP Time (s)")
    print("-" * 43)
    for result in results:
        print(f"{result[0]:>6} | {result[1]:>15.8f} | {result[2]:>10.8f}")
    print("-" * 43)

    # Example of the difference in output for a single amount
    sample_amount = amounts_to_test[-1]
    print(f"\nCoin Counts for Amount {sample_amount}:")
    print(f"  Greedy Result: {find_coins_greedy(sample_amount)}")
    print(f"  DP Result:     {find_min_coins(sample_amount)}")