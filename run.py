from orchestrator import run_system

idea = input("Enter SaaS idea: ")

result = run_system(idea)

print("\n--- Architecture ---")
print(result["architecture"])

print("\n--- Roadmap ---")
print(result["roadmap"])

print("\n--- Critique ---")
print(result["critique"])