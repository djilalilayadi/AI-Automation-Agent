import importlib
import json
import time
from pathlib import Path
from core.logger import setup_logger

class TaskRunner:
    def __init__(self):
        self.logger = setup_logger('task_runner')
        self.tasks = []
        
    def load_tasks(self, config_path='config/tasks.json'):
        try:
            with open(config_path) as f:
                tasks_config = json.load(f)
                
            for task_config in tasks_config:
                module = importlib.import_module(f"tasks.{task_config['type']}")
                task_class = getattr(module, task_config['class'])
                self.tasks.append(task_class(**task_config['params']))
                
            self.logger.info(f"Loaded {len(self.tasks)} tasks")
        except Exception as e:
            self.logger.error(f"Error loading tasks: {e}")

    def execute_all(self):
        for task in self.tasks:
            try:
                self.logger.info(f"Executing task: {task.name}")
                task.execute()
                self.logger.info(f"Completed task: {task.name}")
            except Exception as e:
                self.logger.error(f"Error executing task {task.name}: {e}")

class BaseTask:
    def __init__(self, name, **params):
        self.name = name
        self.params = params
        
    def execute(self):
        raise NotImplementedError("Subclasses must implement execute()")