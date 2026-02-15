from app import create_app

app = create_app()

# For Vercel
if __name__ != '__main__':
    # Production mode for Vercel
    app.config['DEBUG'] = False

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)