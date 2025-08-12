#!/usr/bin/env python3
"""
Example demonstrating concurrency controls in AsyncMediaWikiAPI.

This example shows how to configure and use the concurrency controls
for high-volume async requests to the MediaWiki API.
"""

import asyncio
import time
from mediawikiapi import AsyncMediaWikiAPI
from mediawikiapi.config import Config


async def search_articles(api, query):
    """Search for articles with the given query."""
    start = time.time()
    results = await api.search(query, results=5)
    duration = time.time() - start
    print(f"Search for '{query}' took {duration:.2f}s and found {len(results)} results")
    return results


async def main():
    """Main example function."""
    # Create a config with optimized concurrency settings
    config = Config(
        connection_pool_size=50,        # Total connections in the pool
        connections_per_host=10,        # Connections per host
        max_concurrent_requests=15,     # Concurrent requests limit
        rate_limit=100,                 # Milliseconds between requests
    )
    
    # Create the API with our custom config
    api = AsyncMediaWikiAPI(config)
    
    try:
        print("Initializing connection pool...")
        
        # Run multiple searches in parallel to demonstrate concurrency
        print("\n=== Running searches with concurrency controls ===")
        search_terms = [
            "Python programming",
            "Machine learning",
            "Artificial intelligence",
            "Data science",
            "Computer vision",
            "Natural language processing",
            "Neural networks",
            "Deep learning",
            "Reinforcement learning",
            "Quantum computing"
        ]
        
        # Create tasks for all searches
        tasks = [search_articles(api, term) for term in search_terms]
        
        # Run all searches concurrently
        start = time.time()
        results = await asyncio.gather(*tasks)
        total_time = time.time() - start
        
        print(f"\nCompleted {len(search_terms)} searches in {total_time:.2f}s")
        print(f"Average time per search: {total_time / len(search_terms):.2f}s")
        
        # Demonstrate backpressure by running a burst of searches
        print("\n=== Testing backpressure mechanism with request burst ===")
        burst_tasks = []
        for i in range(30):  # Create a burst of 30 requests
            burst_tasks.append(api.search(f"Topic {i}", results=3))
        
        # Run all burst tasks
        burst_start = time.time()
        burst_results = await asyncio.gather(*burst_tasks)
        burst_time = time.time() - burst_start
        
        print(f"Completed burst of {len(burst_tasks)} requests in {burst_time:.2f}s")
        print(f"Average time per request: {burst_time / len(burst_tasks):.2f}s")
        
    finally:
        # Always close the session when done
        await api.close()


if __name__ == "__main__":
    asyncio.run(main())