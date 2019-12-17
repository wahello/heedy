from typing import Dict
from .base import APIObject, Session

from . import apps
from . import objects
from .notifications import Notifications

class User(APIObject):
    props = {"name", "username","description","icon"}
    def __init__(self, username: str,session : Session):
        super().__init__(f"api/heedy/v1/users/{username}",{"user": username},session)

        # Apps represents a list of the user's active apps. Apps can be accessed by ID::
        #   myapp = await u.apps["appid"]
        # They can also by queried, which will return a list::
        #   myapp = await u.apps(plugin="myplugin")
        # Finally, they can be created::
        #   myapp = await u.apps.create()
        self.apps = apps.Apps({"owner": username},self.session)
        self.objects = objects.Objects({"owner": username},self.session)

    
    
class Users(APIObject):
    def __init__(self, constraints : Dict, session : Session):
        super().__init__("api/heedy/v1/users",constraints,session)
    def __getitem__(self,item):
        return self._getitem(item,f=lambda x : User(x["id"],session=self.session))

    def __call__(self,**kwargs):
        return self._call(f=lambda x :  [User(xx["id"],session=self.session) for xx in x],**kwargs)

    def create(self,username,password,**kwargs):
        return self._create(f= lambda x :  User(x["id"],session=self.session) ,**{'username': username,'password': password, **kwargs})