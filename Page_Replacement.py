import collections


class PageReplacementSimulator:
    def __init__(self, frames, reference_string):
        """
        Initialize the simulator with the number of frames and the reference string.
        """
        self.frames = frames
        self.reference_string = reference_string
        self.page_faults = 0
        self.page_hits = 0
        self.log = []

    def fifo(self):
        """
        First-In-First-Out (FIFO) page replacement algorithm.
        """
        queue = collections.deque()
        self.reset_metrics()

        for page in self.reference_string:
            if page in queue:
                self.page_hits += 1
            else:
                self.page_faults += 1
                if len(queue) >= self.frames:
                    removed = queue.popleft()
                    self.log.append(f"Page {removed} replaced by {page}")
                queue.append(page)
            self.log_state(queue)

    def lru(self):
        """
        Least Recently Used (LRU) page replacement algorithm.
        """
        cache = collections.OrderedDict()
        self.reset_metrics()

        for page in self.reference_string:
            if page in cache:
                self.page_hits += 1
                cache.move_to_end(page)
            else:
                self.page_faults += 1
                if len(cache) >= self.frames:
                    removed, _ = cache.popitem(last=False)
                    self.log.append(f"Page {removed} replaced by {page}")
                cache[page] = True
            self.log_state(cache.keys())

    def lfu(self):
        """
        Least Frequently Used (LFU) page replacement algorithm.
        """
        cache = {}
        frequency = collections.Counter()
        self.reset_metrics()

        for page in self.reference_string:
            frequency[page] += 1
            if page in cache:
                self.page_hits += 1
            else:
                self.page_faults += 1
                if len(cache) >= self.frames:
                    least_used = min(cache, key=lambda k: (frequency[k], cache[k]))
                    del cache[least_used]
                    self.log.append(f"Page {least_used} replaced by {page}")
                cache[page] = len(self.log)  # Track insertion order
            self.log_state(cache.keys())

    def optimal(self):
        """
        Optimal page replacement algorithm.
        """
        cache = set()
        self.reset_metrics()

        for i, page in enumerate(self.reference_string):
            if page in cache:
                self.page_hits += 1
            else:
                self.page_faults += 1
                if len(cache) >= self.frames:
                    # Determine the page to replace
                    future_indices = {p: self.reference_string[i + 1:].index(p) if p in self.reference_string[i + 1:] else float('inf') for p in cache}
                    to_replace = max(future_indices, key=future_indices.get)
                    cache.remove(to_replace)
                    self.log.append(f"Page {to_replace} replaced by {page}")
                cache.add(page)
            self.log_state(cache)

    def log_state(self, state):
        """
        Log the current state of memory.
        """
        self.log.append(f"Memory State: {list(state)}")

    def reset_metrics(self):
        """
        Reset metrics for a new simulation.
        """
        self.page_faults = 0
        self.page_hits = 0
        self.log.clear()

    def display_results(self, algorithm_name):
        """
        Display the results of the simulation.
        """
        print(f"\n--- {algorithm_name} Page Replacement Simulation ---")
        for entry in self.log:
            print(entry)
        print("\nPerformance Metrics:")
        print(f"Total Page Faults: {self.page_faults}")
        print(f"Total Page Hits: {self.page_hits}")
        print(f"Page Fault Percentage: {self.page_faults / len(self.reference_string) * 100:.2f}%")
        print(f"Page Hit Percentage: {self.page_hits / len(self.reference_string) * 100:.2f}%")


def main():
    print("Memory Management Simulator: Page Replacement Algorithms")
    
    # Input number of frames and page reference string
    frames = int(input("Enter the number of frames in memory: "))
    reference_string = list(map(int, input("Enter the sequence of page references (space-separated): ").split()))

    simulator = PageReplacementSimulator(frames, reference_string)

    # Run FIFO simulation
    simulator.fifo()
    simulator.display_results("FIFO")

    # Run LRU simulation
    simulator.lru()
    simulator.display_results("LRU")

    # Run LFU simulation
    simulator.lfu()
    simulator.display_results("LFU")

    # Run Optimal simulation
    simulator.optimal()
    simulator.display_results("Optimal")


if __name__ == "__main__":
    main()
