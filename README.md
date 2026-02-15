# FlavorHive - Recipe Sharing Platform

A professional, production-ready recipe sharing web application built with Flask, featuring a premium light-mode UI/UX design, user authentication, recipe management, admin dashboard, and eSewa payment integration.

## 🎨 Features

### Landing Page
- Modern hero section with animated recipe grid
- Smooth scroll navigation
- About Us section
- Features showcase
- Premium subscription information
- Contact form
- Responsive footer

### User Features
- User registration and authentication
- Dashboard with personalized recommendations
- Upload recipes with images
- Edit and delete own recipes
- Explore approved recipes
- Comment on recipes
- Premium membership upgrade via eSewa
- Profile management
- Password change functionality

### Admin Features
- Admin dashboard with statistics
- Manage all recipes (approve/reject/delete)
- User management
- Comment moderation
- Payment transaction overview
- Recipe status filtering
- Admin profile management

### Technical Features
- Flask backend with Blueprint architecture
- SQLAlchemy ORM for database management
- Flask-Login for authentication
- Werkzeug password hashing
- File upload with validation
- eSewa Test Mode payment integration
- Responsive Bootstrap 5 UI
- Custom CSS with animations
- JavaScript interactions
- Premium light-mode color scheme

## 🎨 Color Palette

- **Primary**: Rich Blue (#1E73BE)
- **Secondary**: Soft Emerald (#2ECC71)
- **Accent**: Warm Orange (#FF8C42)
- **Background**: Ultra Soft White (#F8FAFC)
- **Text**: Charcoal (#1A1A1A)
- **Card Background**: Pure White (#FFFFFF)
- **Borders**: Soft Gray (#E5E7EB)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Installation & Setup

### 1. Clone or Download the Project

```bash
cd FlavorHive
```

### 2. Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python run.py
```

The application will start on `http://localhost:5000`

## 🔐 Default Admin Credentials

**Email**: admin@flavorhive.com  
**Password**: admin123

## 📁 Project Structure

```
FlavorHive/
│
├── app/
│   ├── __init__.py                 # App initialization
│   ├── models/
│   │   ├── user.py                 # User model
│   │   ├── recipe.py               # Recipe model
│   │   ├── comment.py              # Comment model
│   │   └── payment.py              # Payment model
│   ├── routes/
│   │   ├── auth.py                 # Authentication routes
│   │   ├── main.py                 # Landing page routes
│   │   ├── user.py                 # User dashboard routes
│   │   ├── admin.py                # Admin routes
│   │   └── payment.py              # Payment routes
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css           # Custom CSS
│   │   ├── js/
│   │   │   └── main.js             # Custom JavaScript
│   │   ├── images/                 # Static images
│   │   └── uploads/                # User uploaded images
│   └── templates/
│       ├── base.html               # Base template
│       ├── index.html              # Landing page
│       ├── auth/                   # Authentication templates
│       ├── user/                   # User templates
│       ├── admin/                  # Admin templates
│       └── includes/               # Reusable components
│
├── config.py                       # Configuration
├── run.py                          # Application entry point
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables
└── README.md                       # Documentation
```

## 🗄️ Database Models

### User
- Full name, email, password
- Role (user/admin)
- Premium status
- Relationships: recipes, comments, payments

### Recipe
- Title, description, ingredients, steps
- Image, cooking time, servings
- Difficulty, category
- Status (pending/approved/rejected)
- Relationship: user, comments

### Comment
- Comment text
- Relationships: user, recipe

### Payment
- Amount, status, payment method
- Transaction ID
- Relationship: user

## 🌐 Routes

### Public Routes
- `/` - Landing page
- `/login` - User login
- `/register` - User registration

### User Routes (Authentication Required)
- `/user/dashboard` - User dashboard
- `/user/upload-recipe` - Upload new recipe
- `/user/my-recipes` - View user's recipes
- `/user/explore` - Browse approved recipes
- `/user/recipe/<id>` - Recipe details
- `/user/comments` - User's comments
- `/user/profile` - User profile
- `/payment/premium` - Premium subscription

### Admin Routes (Admin Only)
- `/admin/dashboard` - Admin dashboard
- `/admin/recipes` - Manage recipes
- `/admin/users` - Manage users
- `/admin/comments` - Manage comments
- `/admin/payments` - View payments
- `/admin/profile` - Admin profile

## 💳 eSewa Payment Integration

The application includes eSewa Test Mode integration for premium subscriptions:

1. Navigate to Premium page
2. Click "Pay with eSewa"
3. Use eSewa test credentials
4. Complete payment
5. Get redirected back with success/failure status

**Test Configuration**:
- Merchant Code: EPAYTEST
- Test Mode URL: https://uat.esewa.com.np/epay/main

## 🎯 Features in Detail

### Recipe Management
- Users can upload recipes with images
- Admin approval system for quality control
- Edit and delete functionality for own recipes
- Status tracking (pending/approved/rejected)

### Comment System
- Users can comment on approved recipes
- Real-time comment display
- Comment moderation by admin

### Premium Membership
- eSewa payment integration
- NPR 500/month subscription
- Premium badge display
- Exclusive features access

### Authentication
- Secure password hashing with Werkzeug
- Flask-Login session management
- Role-based access control
- Remember me functionality

## 🎨 UI/UX Features

- Smooth scroll animations
- Hover effects and transitions
- Card-based layouts
- Responsive design (mobile/tablet/desktop)
- Interactive recipe grid on landing page
- Auto-hiding alerts
- Form validation
- Image preview on upload
- Loading states
- Professional color scheme

## 🔧 Configuration

Edit `.env` file to configure:

```env
SECRET_KEY=your-secret-key
DATABASE_URI=sqlite:///flavorhive.db
UPLOAD_FOLDER=app/static/uploads
MAX_CONTENT_LENGTH=16777216
ESEWA_MERCHANT_CODE=EPAYTEST
```

## 📝 Usage Guide

### For Users
1. Register an account
2. Login with credentials
3. Upload recipes with images
4. Wait for admin approval
5. Explore and comment on recipes
6. Upgrade to premium (optional)

### For Admins
1. Login with admin credentials
2. Review pending recipes
3. Approve or reject submissions
4. Manage users and comments
5. Monitor payments
6. Delete inappropriate content

## 🛡️ Security Features

- Password hashing with Werkzeug
- CSRF protection (can be enhanced with Flask-WTF)
- File upload validation
- SQL injection prevention (SQLAlchemy ORM)
- XSS protection (Jinja2 auto-escaping)
- Role-based access control

## 🚀 Deployment Considerations

For production deployment:

1. Change `SECRET_KEY` to a strong random value
2. Set `DEBUG=False` in run.py
3. Use production database (PostgreSQL/MySQL)
4. Configure proper WSGI server (Gunicorn/uWSGI)
5. Set up reverse proxy (Nginx/Apache)
6. Enable HTTPS
7. Configure real eSewa merchant credentials
8. Set up proper file storage (AWS S3/CDN)
9. Add email notifications
10. Implement rate limiting

## 🐛 Troubleshooting

**Database Issues**:
```bash
# Delete the database and recreate
rm flavorhive.db
python run.py
```

**Upload Issues**:
- Ensure `app/static/uploads` directory exists
- Check file permissions
- Verify file size < 16MB

**eSewa Payment**:
- Use test credentials in UAT mode
- Check network connectivity
- Verify callback URLs are accessible

## 📦 Dependencies

- Flask==3.0.0
- Flask-SQLAlchemy==3.1.1
- Flask-Login==0.6.3
- Werkzeug==3.0.1
- email-validator==2.1.0
- Pillow==10.1.0
- python-dotenv==1.0.0

## 🤝 Contributing

This is a complete production-ready project. For modifications:

1. Follow the existing code structure
2. Maintain the color scheme
3. Test all features before committing
4. Update documentation as needed

## 📄 License

This project is created for educational and demonstration purposes.

## 👨‍💻 Support

For issues or questions:
- Check the troubleshooting section
- Review the code comments
- Verify all dependencies are installed
- Ensure database is properly initialized

## 🎉 Acknowledgments

Built with:
- Flask - Web framework
- Bootstrap 5 - UI framework
- Font Awesome - Icons
- Google Fonts - Typography
- eSewa - Payment gateway

---

**FlavorHive** - Share Your Culinary Masterpieces 🍳
