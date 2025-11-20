def decide(x):
    # A simple decision boundary: if x > 0.5, classify as 1 else 0
    return 1 if x > 0.5 else 0


print(decide(0.2))  # 0
print(decide(0.8))  # 1
