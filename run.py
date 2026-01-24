import sys
from app import create_app, db
from app.models import User

print("--- Starting ShikshyaHub ---")

try:
    app = create_app()
    print("✅ App instance created successfully!")
except Exception as e:
    print(f"❌ Error during app creation: {e}")
    sys.exit(1)

if __name__ == '__main__':
    try:
        with app.app_context():
            print("⏳ Checking Database...")
            db.create_all()
            
            # Create a default admin if it doesn't exist
            admin = User.query.filter_by(email='admin@shikshyahub.com').first()
            if not admin:
                print("⏳ Creating default Admin user...")
                admin = User(name='System Admin', email='admin@shikshyahub.com', role='admin')
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("✅ Database & Admin ready!")
            else:
                print("✅ Admin user already exists.")

        print("🚀 Launching Server at http://127.0.0.1:5000")
        app.run(debug=True)
    except Exception as e:
        print(f"❌ Critical Error: {e}")