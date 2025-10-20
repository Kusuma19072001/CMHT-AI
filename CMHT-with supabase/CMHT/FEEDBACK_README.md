# CMHT Feedback System with Supabase

This project now includes a comprehensive feedback system that stores feedback data in Supabase, a powerful backend-as-a-service platform.

## 🚀 Features

- **Store feedback** with type, message, name, email, and rating
- **Retrieve feedback** with filtering and pagination
- **Update feedback** records
- **Delete feedback** records
- **View statistics** and analytics
- **Web interface** for easy feedback submission and management

## 📋 Prerequisites

1. **Python 3.7+** installed
2. **Supabase account** and project
3. **Supabase URL and API key** (already configured)

## 🛠️ Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Supabase connection:**
   ```bash
   python test_supabase.py
   ```

## 🗄️ Database Schema

The feedback table will be automatically created in Supabase with the following structure:

```sql
CREATE TABLE feedback (
    id BIGSERIAL PRIMARY KEY,
    type TEXT NOT NULL,
    message TEXT NOT NULL,
    name TEXT,
    email TEXT,
    rating TEXT,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);
```

## 🚀 Usage

### 1. Start the Application

```bash
python app.py
```

The application will be available at `http://localhost:8080`

### 2. Access Feedback System

- **Main app**: `http://localhost:8080` (voice assistant)
- **Feedback form**: `http://localhost:8080/feedback-form`

### 3. API Endpoints

#### Submit Feedback
```http
POST /feedback
Content-Type: application/json

{
    "type": "general",
    "message": "Your feedback message",
    "name": "Your Name",
    "email": "your@email.com",
    "rating": "5"
}
```

#### Get All Feedback
```http
GET /feedback?limit=100
```

#### Get Feedback by Type
```http
GET /feedback?type=general&limit=50
```

#### Get Feedback Statistics
```http
GET /feedback/stats
```

#### Update Feedback
```http
PUT /feedback/{id}
Content-Type: application/json

{
    "message": "Updated message"
}
```

#### Delete Feedback
```http
DELETE /feedback/{id}
```

## 📊 Feedback Types

The system supports these feedback types:
- `general` - General feedback
- `technical` - Technical issues
- `suggestion` - Suggestions for improvement
- `complaint` - Complaints
- `praise` - Positive feedback
- `bug` - Bug reports
- `feature` - Feature requests

## 🔧 Configuration

The Supabase configuration is stored in `config.py`:

```python
SUPABASE_URL = "https://vowetzvwmlbwyjdvihsz.supabase.co"
SUPABASE_KEY = "your-api-key-here"
```

## 🧪 Testing

Run the test script to verify everything works:

```bash
python test_supabase.py
```

This will test:
- ✅ Supabase connection
- ✅ Feedback storage
- ✅ Feedback retrieval
- ✅ Feedback updates
- ✅ Feedback deletion
- ✅ Statistics generation
- ✅ Type-based filtering

## 📱 Web Interface

The feedback form (`/feedback-form`) provides:

- **Feedback submission form** with all fields
- **Real-time statistics** display
- **Recent feedback** viewing
- **Responsive design** for mobile and desktop

## 🔒 Security Features

- **Input validation** on all endpoints
- **Error handling** with meaningful messages
- **Rate limiting** considerations (implement as needed)
- **Data sanitization** before storage

## 📈 Monitoring and Analytics

The system provides:

- **Total feedback count**
- **Feedback by type** breakdown
- **Timestamp tracking** for all records
- **Update tracking** for modified records

## 🚨 Troubleshooting

### Common Issues

1. **Supabase connection failed**
   - Check your URL and API key in `config.py`
   - Verify your Supabase project is active
   - Check network connectivity

2. **Table not found**
   - The table is created automatically on first insert
   - Check Supabase dashboard for table creation

3. **Permission denied**
   - Verify your API key has the correct permissions
   - Check Supabase RLS (Row Level Security) policies

### Debug Mode

Enable debug logging by modifying the Flask app:

```python
app.run(debug=True, port=8080)
```

## 🔄 Integration with Voice Assistant

The feedback system is integrated with your existing voice assistant:

- **Voice queries** can trigger feedback collection
- **Email alerts** for urgent feedback
- **Seamless user experience** across platforms

## 📚 API Documentation

For detailed API documentation, see the inline comments in:
- `feedback_manager.py` - Core feedback operations
- `app.py` - API endpoints and routing

## 🤝 Contributing

To add new features:

1. **Extend the feedback schema** in `feedback_manager.py`
2. **Add new API endpoints** in `app.py`
3. **Update the web interface** in `feedback.html`
4. **Add tests** in `test_supabase.py`

## 📄 License

This project is part of the CMHT Voice Assistant system.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Run the test script to verify functionality
3. Check Supabase dashboard for database issues
4. Review application logs for error details

---

**Happy feedback collecting! 🎉** 