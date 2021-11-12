from main import app
#import os

if __name__ == "__main__":
  #port = int(os.environ.get("PORT", 80))
  app.jinja_env.cache = {}
  app.run()
