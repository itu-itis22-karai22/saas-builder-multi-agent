class Metrics:

    def __init__(self):
        self.calls = 0
        self.tokens = 0
        self.times = []

    def log(self, tokens, time):
        self.calls += 1
        self.tokens += tokens
        self.times.append(time)

    def print(self):

        total_time = sum(self.times)

        print("----- Metrics -----")
        print("total-llm-calls:", self.calls)
        print("e2e-response-time:", total_time)
        print("mean-response-time:", total_time / self.calls)
        print("total-tokens:", self.tokens)
        print("mean-token-per-call:", self.tokens / self.calls)