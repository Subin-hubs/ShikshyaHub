# FlavorHive - Quick Start Guide

## 🚀 Get Started in 3 Minutes

### Step 1: Setup Environment

```bash
# Navigate to project folder
cd FlavorHive

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Run the Application

```bash
python run.py
```

### Step 3: Access the Application

Open your browser and go to: `http://localhost:5000`

## 🔑 Login Credentials

### Admin Account
- **Email**: admin@flavorhive.com
- **Password**: admin123

### User Account
- Create your own by clicking "Register" on the landing page

## ✨ What to Try First

### As a User:
1. **Register** - Create a new account
2. **Upload Recipe** - Add your first recipe with an image
3. **Explore** - Browse approved recipes
4. **Comment** - Share your thoughts on recipes
5. **Go Premium** - Try the eSewa payment flow (test mode)

### As an Admin:
1. **Login** with admin credentials
2. **Review Recipes** - Approve or reject pending recipes
3. **Manage Users** - View all registered users
4. **Monitor Payments** - Check payment transactions
5. **Moderate Comments** - Delete inappropriate comments

## 📸 Key Pages to Visit

- **Landing Page**: http://localhost:5000/
- **Login**: http://localhost:5000/login
- **Register**: http://localhost:5000/register
- **User Dashboard**: http://localhost:5000/user/dashboard (after login)
- **Admin Dashboard**: http://localhost:5000/admin/dashboard (admin only)

## 🎨 UI Features to Explore

- **Smooth Animations** - Scroll the landing page
- **Hover Effects** - Hover over cards and buttons
- **Recipe Grid** - Click on hero section recipe images
- **Responsive Design** - Resize your browser window
- **Auto-hide Alerts** - Watch success messages fade out

## 💡 Tips

1. **Upload Images**: Supported formats - PNG, JPG, JPEG, GIF, WEBP (max 16MB)
2. **Recipe Approval**: User recipes need admin approval before appearing in Explore
3. **Premium Features**: Use eSewa test mode to activate premium membership
4. **Admin Control**: Admin can approve, reject, or delete any recipe

## 🐛 Common Issues

**Port Already in Use**:
```bash
# Change port in run.py or kill the process using port 5000
```

**Database Error**:
```bash
# Delete and recreate database
rm flavorhive.db
python run.py
```

**Import Error**:
```bash
# Make sure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

## 📝 Project Structure Overview

```
FlavorHive/
├── app/                    # Main application package
│   ├── models/            # Database models
│   ├── routes/            # URL routes/views
│   ├── static/            # CSS, JS, images
│   └── templates/         # HTML templates
├── config.py              # Configuration
├── run.py                 # Application entry point
└── requirements.txt       # Dependencies
```

## 🎯 Next Steps

1. **Customize**: Modify colors in `app/static/css/style.css`
2. **Add Features**: Extend models and routes
3. **Deploy**: Follow deployment guide in README.md
4. **Enhance**: Add email notifications, search, etc.

## 📚 Documentation

For detailed documentation, see `README.md`

---

**Happy Cooking!** 🍳✨
