from src.RandomPicker import RandomPicker
import time

def detailed_test():
    print("Advanced Random Number Generator Test")
    print("=" * 60)

    # Initialize with a small range for better visualization
    picker = RandomPicker(1, 20)

    print("\nGenerating 5 numbers with detailed steps:")
    print("-" * 60)

    for i in range(5):
        number = picker.pick()
        print(f"\nRandom Number {i+1}:")
        print(f"Final Result: {number}")
        print("-" * 30)

        # Add a small delay for readability
        time.sleep(1)

if __name__ == "__main__":
    try:
        detailed_test()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
