# 📊 Cloud-Powered CSV Filter Tool

A Streamlit application that filters CSV files of any size, with cloud backend support for large datasets.

![App Screenshot](https://example.com/screenshot.png) *(replace with actual screenshot URL)*

## 🌟 Features

- **Dual Processing Modes**:
  - Local processing for files <200MB
  - Cloud backend processing for large files
- **Flexible Filtering**:
  - Exact matches or contains matches (case-insensitive)
  - Regex support (advanced mode)
  - Wildcard support (`*` for pattern matching)
- **Interactive UI**:
  - Dynamic filter addition/removal
  - Filter reordering
  - Real-time previews
- **Smart Features**:
  - Automatic header detection
  - Column type awareness
  - Progress indicators

## 🚀 Quick Start

1. **Install requirements**:
   ```bash
   pip install streamlit pandas requests
Run the app:

bash
streamlit run filter-data-v2.py
Configure backend (optional):

bash
export BACKEND_URL="http://your-backend:8000"
export BACKEND_TOKEN="your-auth-token"
🛠️ Usage
Upload your CSV file:

Drag and drop any CSV file

Specify if it has headers

Set filter criteria:

Add multiple filters with + button

Reorder with ↑↓ buttons

Remove with × button

Choose match type:

Exact match (supports wildcards)

Contains match (case-insensitive)

Regex mode (advanced)

View & download results:

Preview first 5 matching rows

Download full filtered dataset

⚙️ Configuration
Environment Variable	Default	Description
BACKEND_URL	http://localhost:8000	Cloud processing endpoint
BACKEND_TOKEN	-	Authentication token
MAX_STREAMLIT_SIZE	209715200 (200MB)	Max file size for local processing
REQUEST_TIMEOUT	30	Backend request timeout in seconds
🌐 Backend API Requirements
If using cloud processing, your backend should implement:

http
POST /filter-csv
Content-Type: multipart/form-data

Parameters:
- file: CSV file
- has_header: boolean
- match_type: "Exact Match" or "Contains Match"
- regex_mode: boolean
- filters: JSON array of {col, val} objects

Response:
{
  "original_count": int,
  "match_count": int,
  "csv_data": "filtered,csv,data\n..."
}
💡 Tips & Tricks
Use [value] for exact matches in "Contains Match" mode

* acts as a wildcard in "Exact Match" mode

Enable regex for powerful pattern matching

Start with 1-2 filters and add more as needed

🐛 Known Limitations
Very wide CSV files may display poorly in preview

Complex regex patterns may impact performance

Non-UTF8 encoded files may require manual handling

📜 License
MIT License - see LICENSE file for details

Note: For production use with large files, ensure your backend is properly scaled and secured.

text

This README includes:

1. **Visual appeal** with emojis and clear sections
2. **Comprehensive feature list** highlighting key capabilities
3. **Setup instructions** for different scenarios
4. **Configuration details** for customization
5. **Backend API specs** for cloud processing
6. **Usage tips** to help users get the most from the app
7. **Transparency** about limitations

You may want to:

1. Add actual screenshots
2. Include a demo GIF/video
3. Add a "Development" section for contributors
4. Expand the troubleshooting section
5. Add CI/CD badges if applicable

The README is designed to be informative yet concise, helping users quickly understand and use your application effectively.
