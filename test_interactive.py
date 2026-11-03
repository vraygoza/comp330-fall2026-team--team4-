from src.core.parser import handle_food_message, parse_message

test_cases = [
    "2 tacos",        # Step 1: turns into item & quantity
    "banana",         # Step 2: missing quantity -> asks how many
    "taco",           # Step 2: missing quantity -> asks how many
    "2 dragonfruit",  # Step 3: unknown food -> friendly reply
    "an egg",         # Article -> quantity 1.0
    "1.5 bananas",    # Decimal quantity
    "25 eggs",        # Out of range (> 20)
    "eggs 2",         # Unsupported format
]

print("=" * 60)
print("TESTING K2 PARSER & REPLIES")
print("=" * 60)

for msg in test_cases:
    res = parse_message(msg)
    reply = handle_food_message(msg)
    print(f"Input:   {msg}")
    print(f"Outcome: {res.outcome} | Food: {res.food} | Quantity: {res.quantity}")
    print(f"Reply:   {reply}")
    print("-" * 60)

