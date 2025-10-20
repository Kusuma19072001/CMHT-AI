# Database Setup Instructions

## 🗄️ Setting up the Feedback Table in Supabase

Since the Python client cannot automatically create tables, you need to create the feedback table manually in your Supabase dashboard.

### Step 1: Access Supabase Dashboard

1. Go to [https://supabase.com](https://supabase.com)
2. Sign in to your account
3. Select your project: `vowetzvwmlbwyjdvihsz`

### Step 2: Open SQL Editor

1. In your project dashboard, click on **"SQL Editor"** in the left sidebar
2. Click **"New query"** to create a new SQL query

### Step 3: Run the Table Creation Script

1. Copy the contents of `create_feedback_table.sql`
2. Paste it into the SQL editor
3. Click **"Run"** to execute the script

### Step 4: Verify Table Creation

1. Go to **"Table Editor"** in the left sidebar
2. You should see a new table called `feedback`
3. Click on it to see the structure and sample data

### Step 5: Test the System

After creating the table, you can test the feedback system:

```bash
# Test the Supabase connection
python test_supabase.py

# Start the application
python app.py
```

## 🔧 Alternative: Manual Table Creation

If you prefer to create the table manually through the interface:

### Using Table Editor

1. Go to **"Table Editor"** → **"New table"**
2. Table name: `feedback`
3. Add columns:
   - `id` (type: `int8`, primary key, identity)
   - `type` (type: `text`, not null)
   - `message` (type: `text`, not null)
   - `name` (type: `text`, nullable)
   - `email` (type: `text`, nullable)
   - `rating` (type: `text`, nullable)
   - `timestamp` (type: `timestamptz`, default: `now()`)
   - `updated_at` (type: `timestamptz`, nullable)

### Enable RLS (Row Level Security)

1. In the table settings, enable **"Enable Row Level Security (RLS)"**
2. Create a policy that allows all operations (for now)

## 🚨 Troubleshooting

### Table Not Found Error
- Make sure you've run the SQL script in the correct project
- Check that the table name is exactly `feedback` (lowercase)
- Verify the table is in the `public` schema

### Permission Denied Error
- Check that RLS policies are set correctly
- Verify your API key has the right permissions
- Make sure the table is accessible to anonymous users (if using anon key)

### Connection Issues
- Verify your Supabase URL and API key in `config.py`
- Check that your project is active and not paused
- Ensure your IP is not blocked by any firewall rules

## ✅ Verification

After setup, you should be able to:

1. ✅ Connect to Supabase
2. ✅ Insert feedback records
3. ✅ Retrieve feedback records
4. ✅ Update feedback records
5. ✅ Delete feedback records
6. ✅ View feedback statistics

## 🎯 Next Steps

Once the table is created:

1. **Test the system**: Run `python test_supabase.py`
2. **Start the app**: Run `python app.py`
3. **Access feedback form**: Go to `http://localhost:8080/feedback-form`
4. **Submit test feedback**: Use the web form to test the system

## 📞 Need Help?

If you encounter issues:

1. Check the Supabase project logs
2. Verify your API key permissions
3. Check the table structure matches the expected schema
4. Ensure RLS policies are configured correctly

---

**The feedback system will be fully functional once the table is created! 🎉** 