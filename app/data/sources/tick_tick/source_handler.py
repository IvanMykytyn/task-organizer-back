

import json

import requests
from pydantic import BaseModel
from app.api.deps import SessionDep
from app.clients.credentials.client import CredentialsHandler
from app.data.models import Task
from app.data.sources.abstract_source_handler import SourceHandler

class TickTickTokenData(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    scope: str

BASE_URL = "https://ticktick.com/open/v1"
SOURCE_ID = 'tick_tick'
WEBSITE_BASE_URL = "https://ticktick.com/webapp/#p"

class TickTickSourceHandler(SourceHandler):
    def __init__(self, user_id: str, user_email: str) -> None:
        self.user_id = user_id
        self.user_email = user_email
        self.source_id = SOURCE_ID
        self._access_token: str = None
    
    def get_auth(self):
        if self._access_token:
            return self._access_token
        response = CredentialsHandler().get_credentials(user_email=self.user_email, source_id=self.source_id)
        data = TickTickTokenData(**json.loads(response.secret_value))
        access_token = f'{data.token_type} {data.access_token}'
        self._access_token = access_token
        return access_token
    
    def get_user_projects(self):
        access_token = self.get_auth()
        url = f'{BASE_URL}/project'
        response = requests.get(url, headers={'Authorization': access_token })
        response.raise_for_status()
        projects = response.json()
        return projects
    
    
    def get_project_data(self, project_id: str):
        access_token = self.get_auth()
        
        url = f'{BASE_URL}/project/{project_id}/data'
        response = requests.get(url, headers={'Authorization': access_token })
        response.raise_for_status()
        data = response.json()
        return data
        
    def get_tasks(self, session: SessionDep, q: str):
        tasks = []
        projects = self.get_user_projects()
        for project in projects:
            project_data = self.get_project_data(project_id=project['id'])
            project_tasks = project_data.get('tasks', [])
            project_id_to_title = { item['id']:item['title'] for item in project_tasks}
            for task in project_tasks:
                parent_id = task.get('parentId')
                parent=None
                if parent_id:
                    parent = project_id_to_title[parent_id]
                if q:
                   if not (q.lower() in (project['name'].lower() + " " + task['title'].lower()) or (task.get('description') and q.lower() in task["description"].lower())):
                        continue

                tasks.append(Task(
                    title=task['title'] if bool(task["title"]) else "Untitled",
                    description=task["description"] if task.get("description") else task.get("content"),  
                    parent=parent,
                    source=self.source_id,
                    priority=task["priority"],
                    tags=task.get('tags', []),
                    project=project['name'],
                    url=f"{WEBSITE_BASE_URL}/{project['id']}/tasks/{task['id']}", 
                    color= project['color'],
                ))        
        return tasks
        