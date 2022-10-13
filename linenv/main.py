
from multipage import MultiApp
from apps import public,pro_login  # import your app modules here
 
app = MultiApp()

app.add_app("LINKEDIN PUBLIC", public.app)
app.add_app("LINKEDIN RECRUITER", pro_login.app)
# The main app
app.run()



