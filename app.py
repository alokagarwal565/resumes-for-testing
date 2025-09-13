#!/usr/bin/env python3
"""
Vercel-compatible Flask Web Application for Resume Generator
Modified for serverless deployment on Vercel.
"""

import os
import json
import time
import zipfile
import tempfile
import shutil
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename
import io
import base64

# Import our resume generator
from resume_generator import ResumeGenerator

app = Flask(__name__)

# For Vercel, we'll use in-memory processing and return files directly
# No persistent file storage in serverless environment

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_resumes():
    """Generate resumes synchronously for Vercel"""
    try:
        data = request.get_json()
        
        # Validate input
        num_resumes = data.get('num_resumes', 100)
        content_type = data.get('content_type', 'template')
        gemini_key = data.get('gemini_key')
        
        if not isinstance(num_resumes, int) or num_resumes < 1 or num_resumes > 100:
            return jsonify({'error': 'Number of resumes must be between 1 and 1000'}), 400
        
        if content_type not in ['template', 'gemini']:
            return jsonify({'error': 'Invalid content type'}), 400
        
        if content_type == 'gemini' and not gemini_key:
            return jsonify({'error': 'Gemini API key required for Gemini content type'}), 400
        
        # For Vercel, we'll limit the number of resumes to prevent timeout
        if num_resumes > 50:
            return jsonify({'error': 'For Vercel deployment, maximum 50 resumes per request'}), 400
        
        # Initialize generator
        use_gemini = content_type == 'gemini' and gemini_key
        generator = ResumeGenerator(use_gemini=use_gemini, gemini_api_key=gemini_key)
        
        # Create in-memory ZIP file
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for i in range(num_resumes):
                try:
                    # Generate resume data
                    resume_data = generator.generate_resume_data()
                    
                    # Create PDF in memory
                    pdf_buffer = io.BytesIO()
                    generator.create_pdf_resume_memory(resume_data, pdf_buffer)
                    pdf_buffer.seek(0)
                    
                    # Add to ZIP
                    safe_name = "".join(c for c in resume_data['name'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    filename = f"resume_{i+1:03d}_{safe_name.replace(' ', '_')}.pdf"
                    zipf.writestr(filename, pdf_buffer.getvalue())
                    
                except Exception as e:
                    print(f"Error generating resume {i+1}: {e}")
                    continue
        
        zip_buffer.seek(0)
        
        # Encode ZIP file as base64 for transmission
        zip_data = zip_buffer.getvalue()
        zip_base64 = base64.b64encode(zip_data).decode('utf-8')
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"resumes_{timestamp}.zip"
        
        return jsonify({
            'status': 'completed',
            'zip_data': zip_base64,
            'filename': zip_filename,
            'file_size': len(zip_data),
            'num_resumes': num_resumes,
            'message': f'Successfully generated {num_resumes} resumes'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download_zip():
    """Download ZIP file from base64 data"""
    try:
        data = request.get_json()
        zip_data = data.get('zip_data')
        filename = data.get('filename', 'resumes.zip')
        
        if not zip_data:
            return jsonify({'error': 'No ZIP data provided'}), 400
        
        # Decode base64 data
        zip_bytes = base64.b64decode(zip_data)
        
        # Create file-like object
        zip_buffer = io.BytesIO(zip_bytes)
        
        return send_file(
            zip_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/zip'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large'}), 413

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

# This is the entry point for Vercel
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
