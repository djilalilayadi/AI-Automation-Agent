from agent_core import AICore
from skills.web_scraper import WebScraper
from skills.spreadsheet import SpreadsheetManager

class AIAgent:
    def __init__(self):
        self.brain = AICore()
        self.scraper = WebScraper()
        self.spreadsheet = SpreadsheetManager()
    
    def execute_task(self, user_command: str):
        """Main workflow"""
        # Step 1: Understand the task
        task = self.brain.understand_task(user_command)
        print(f"Interpreted task: {task}")
        
        # Step 2: Execute based on task type
        if task["action"] == "scrape":
            results = self.scraper.scrape_jobs(task["target"])
            if task["output"] == "spreadsheet":
                self.spreadsheet.save_to_excel(results)
                return "Task completed successfully!"
        
        return "Sorry, I couldn't complete this task yet."

if __name__ == "__main__":
    agent = AIAgent()
    
    # Example usage
    while True:
        user_input = input("\nWhat should I do? (or 'quit' to exit)\n> ")
        if user_input.lower() == 'quit':
            break
        
        result = agent.execute_task(user_input)
        print(result)