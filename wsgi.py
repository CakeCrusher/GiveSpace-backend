from app.main import app
import os
from dotenv import load_dotenv
load_dotenv()

if __name__ == '__main__':
  if os.environ.get('IS_PRODUCTION') == 'false':
    app.run(debug=True)
  else:
    app.run()
