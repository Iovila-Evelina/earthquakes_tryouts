import argparse

def main():
    # 1. Initialize the Parser
    # This tool will read the command line inputs for us.
    parser = argparse.ArgumentParser(description="Earthquake search tool")

    # 2. Add the arguments as requested in the Manual (Page 3)
    # The manual says: "optional argument's names start with --"
    # But also says: "make them mandatory with required=True"

    # Argument 1: days (integer) - How many days back to search
    parser.add_argument('--days',
                        type=int,
                        required=True,
                        help="Number of days to search backwards")

    # Argument 2: K (integer) - The maximum number of earthquakes to show
    parser.add_argument('--K',
                        type=int,
                        required=True,
                        help="Number of strongest earthquakes to return")

    # Argument 3: magnitude (float) - The minimum magnitude (e.g., 2.5)
    parser.add_argument('--magnitude',
                        type=float,
                        required=True,
                        help="Minimum magnitude allowed")

    # 3. Parse the arguments
    # This line checks if the user typed the commands correctly.
    # If they didn't, the program stops here and shows an error automatically.
    args = parser.parse_args()

    # 4. Print the values to verify it works (Temporary Step)
    print(f"Searching for the top {args.K} earthquakes...")
    print(f"Over the last {args.days} days...")
    print(f"With a magnitude of at least {args.magnitude}.")

# This ensures the script runs only when executed directly
if __name__ == '__main__':
    main()