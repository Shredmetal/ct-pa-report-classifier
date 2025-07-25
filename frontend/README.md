# CT-PA Report Classifier Frontend

A modern, dark-themed web interface for the CT-PA report classifier system.

## 🚀 Quick Start

### 1. Start the Backend Server
```bash
cd /Users/morganlee/PycharmProjects/ct-pa-report-classifier
python src/main.py
```
The API will be available at `http://localhost:8000`

### 2. Start the Frontend
```bash
cd frontend
python -m http.server 3000
```
Open your browser to `http://localhost:3000`

### 3. Alternative Frontend Setup
You can also use any HTTP server:
```bash
# Using Node.js
npx http-server . -p 3000

# Using PHP
php -S localhost:3000

# Or open index.html directly in browser (may have CORS issues)
```

## ✨ Features

### 📁 File Upload
- **Drag & Drop**: Drop CSV files directly onto the upload zone
- **Browse**: Click to select files using file browser
- **Multiple Files**: Upload multiple CSV files at once
- **Progress Tracking**: Visual progress bar during uploads
- **Validation**: Automatic CSV format and size validation

### 📋 Source File Management
- **File List**: View all uploaded files with metadata
- **Multi-Select**: Check boxes to select files for processing
- **Individual Actions**: Delete specific files
- **Bulk Operations**: Clear all source files at once
- **Real-time Updates**: Refresh file list anytime

### ⚡ Processing
- **Batch Processing**: Process multiple selected files
- **Custom Output**: Set custom output prefix for processed files
- **Real-time Status**: Visual processing indicator
- **Detailed Results**: See processing results for each file
- **Auto-refresh**: Processed files list updates automatically

### ✅ Processed File Management
- **Download**: Download individual processed files
- **File Information**: View file size and modification dates
- **Delete**: Remove specific processed files
- **Bulk Operations**: Clear all processed files

### 🔧 Additional Features
- **Dark Theme**: Modern, eye-friendly dark interface
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Toast Notifications**: User-friendly feedback messages
- **Error Handling**: Comprehensive error handling and user feedback
- **Confirmation Dialogs**: Safety confirmations for destructive operations

## 🔗 API Integration

The frontend integrates with these backend endpoints:
- `POST /api/upload-csv` - Upload CSV files
- `GET /api/source-files` - List source files
- `POST /api/process-files` - Process selected files
- `GET /api/processed-files` - List processed files
- `GET /api/download-file/{directory}/{filename}` - Download files
- `DELETE /api/delete-files` - Delete specific files
- `DELETE /api/clear-directory/{directory}` - Clear directories

## 🛠️ Troubleshooting

### CORS Issues
If you encounter CORS errors, make sure the backend is running with the CORS middleware enabled.

### File Downloads Not Working
Ensure the backend has the download endpoint (`/api/download-file`) available.

### Upload Failures
- Check file format (must be CSV)
- Verify file size (under 50MB limit)
- Ensure backend is running and accessible

### Connection Issues
- Verify backend is running on `http://localhost:8000`
- Check if `API_BASE_URL` in `script.js` matches your backend URL
- Ensure no firewall is blocking the connection

## 🎨 Customization

### Changing API URL
Edit the `API_BASE_URL` constant in `script.js`:
```javascript
const API_BASE_URL = 'http://your-backend-url:port';
```

### Theme Customization
Modify CSS custom properties in `styles.css`:
```css
:root {
    --bg-primary: #your-color;
    --accent-primary: #your-accent;
    /* ... other variables */
}
```

## 📱 Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge

## 🔒 Security Notes

- The current CORS configuration allows all origins (`*`) for development
- In production, update CORS settings to allow only specific domains
- File uploads are validated on both frontend and backend
- Directory traversal protection is implemented for file operations 