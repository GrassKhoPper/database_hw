from store import app

# run flask application
if __name__ == '__main__':
  # ssl_context = ('store.crt', 'store.key')
  app.run('0.0.0.0', port=5000, debug=True)
