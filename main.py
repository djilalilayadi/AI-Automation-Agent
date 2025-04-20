import json
from pathlib import Path
from core.task_runner import TaskRunner

def get_user_input():
    """Allow user to configure the target website"""
    print("\n" + "="*40)
    print("Website Scraper Configuration")
    print("="*40)
    
    url = input("Enter target URL (leave empty for default): ").strip()
    delay = input("Request delay in seconds (default 2): ").strip()
    respect_robots = input("Respect robots.txt? (y/n, default y): ").strip().lower()
    
    # Load default config
    config_path = Path('config/tasks.json')
    with open(config_path) as f:
        config = json.load(f)
    
    # Update with user input
    if url:
        config[0]['params']['url'] = url
    if delay:
        config[0]['params']['request_delay'] = float(delay)
    if respect_robots in ('n', 'no'):
        config[0]['params']['respect_robots'] = False
    
    # Save updated config
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    return config

def main():
    # Get user configuration
    config = get_user_input()
    
    # Run tasks
    runner = TaskRunner()
    runner.load_tasks()
    runner.execute_all()

if __name__ == "__main__":
    main()