// DOM elements
const form = document.getElementById('resumeForm');
const numResumesInput = document.getElementById('numResumes');
const contentTypeRadios = document.querySelectorAll('input[name="contentType"]');
const geminiKeyGroup = document.getElementById('geminiKeyGroup');
const geminiKeyInput = document.getElementById('geminiKey');
const generateBtn = document.getElementById('generateBtn');
const progressContainer = document.getElementById('progressContainer');
const resultContainer = document.getElementById('resultContainer');
const errorContainer = document.getElementById('errorContainer');
const progressText = document.getElementById('progressText');
const progressFill = document.getElementById('progressFill');
const progressDetails = document.getElementById('progressDetails');
const resultText = document.getElementById('resultText');
const downloadLink = document.getElementById('downloadLink');
const fileSize = document.getElementById('fileSize');
const generationTime = document.getElementById('generationTime');
const errorText = document.getElementById('errorText');

// State
let isGenerating = false;
let startTime = null;

// Event listeners
form.addEventListener('submit', handleFormSubmit);
contentTypeRadios.forEach(radio => {
    radio.addEventListener('change', handleContentTypeChange);
});

// Handle form submission
async function handleFormSubmit(e) {
    e.preventDefault();
    
    if (isGenerating) return;
    
    const formData = new FormData(form);
    const numResumes = parseInt(formData.get('numResumes'));
    const contentType = formData.get('contentType');
    const geminiKey = formData.get('geminiKey');
    
    // Validation
    if (numResumes < 1 || numResumes > 50) {
        showError('For Vercel deployment, please enter a number between 1 and 50.');
        return;
    }
    
    if (contentType === 'gemini' && !geminiKey.trim()) {
        showError('Please enter your Gemini API key.');
        return;
    }
    
    // Start generation
    startGeneration(numResumes, contentType, geminiKey);
}

// Handle content type change
function handleContentTypeChange() {
    const selectedType = document.querySelector('input[name="contentType"]:checked').value;
    geminiKeyGroup.style.display = selectedType === 'gemini' ? 'block' : 'none';
    
    if (selectedType === 'gemini') {
        geminiKeyInput.required = true;
    } else {
        geminiKeyInput.required = false;
    }
}

// Start generation process
async function startGeneration(numResumes, contentType, geminiKey) {
    isGenerating = true;
    startTime = Date.now();
    
    // Hide other containers
    hideAllContainers();
    
    // Show progress container
    progressContainer.style.display = 'block';
    
    // Disable form
    generateBtn.disabled = true;
    generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
    
    // Update progress
    updateProgress(0, numResumes, 'Starting generation...');
    
    try {
        // Prepare request data
        const requestData = {
            num_resumes: numResumes,
            content_type: contentType,
            gemini_key: contentType === 'gemini' ? geminiKey : null
        };
        
        // Start generation (synchronous for Vercel)
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to generate resumes');
        }
        
        // Get the result
        const result = await response.json();
        
        // Show success
        showSuccess(result, numResumes);
        
    } catch (error) {
        console.error('Generation error:', error);
        showError(error.message || 'An error occurred while generating resumes.');
    } finally {
        isGenerating = false;
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<i class="fas fa-magic"></i> Generate Resumes';
    }
}

// Show success
function showSuccess(result, numResumes) {
    hideAllContainers();
    resultContainer.style.display = 'block';
    
    const endTime = Date.now();
    const duration = Math.round((endTime - startTime) / 1000);
    
    resultText.textContent = `Successfully generated ${numResumes} resumes!`;
    generationTime.textContent = `${duration} seconds`;
    
    if (result.file_size) {
        fileSize.textContent = formatFileSize(result.file_size);
    }
    
    // Create download link from base64 data
    const zipData = result.zip_data;
    const filename = result.filename || 'resumes.zip';
    
    // Convert base64 to blob and create download link
    const byteCharacters = atob(zipData);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], { type: 'application/zip' });
    
    const url = window.URL.createObjectURL(blob);
    downloadLink.href = url;
    downloadLink.download = filename;
    
    // Scroll to result
    resultContainer.scrollIntoView({ behavior: 'smooth' });
}

// Show error
function showError(message) {
    hideAllContainers();
    errorContainer.style.display = 'block';
    errorText.textContent = message;
    
    // Scroll to error
    errorContainer.scrollIntoView({ behavior: 'smooth' });
}

// Hide all containers
function hideAllContainers() {
    progressContainer.style.display = 'none';
    resultContainer.style.display = 'none';
    errorContainer.style.display = 'none';
}

// Reset form
function resetForm() {
    hideAllContainers();
    form.reset();
    geminiKeyGroup.style.display = 'none';
    geminiKeyInput.required = false;
    isGenerating = false;
    generateBtn.disabled = false;
    generateBtn.innerHTML = '<i class="fas fa-magic"></i> Generate Resumes';
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Update progress
function updateProgress(current, total, details) {
    const percentage = Math.round((current / total) * 100);
    progressText.textContent = `${current} / ${total}`;
    progressFill.style.width = `${percentage}%`;
    progressDetails.textContent = details;
}

// Initialize form
document.addEventListener('DOMContentLoaded', function() {
    // Set default values
    numResumesInput.value = 10; // Lower default for Vercel
    numResumesInput.max = 50; // Set max for Vercel
    
    // Handle content type change on load
    handleContentTypeChange();
    
    // Add input validation
    numResumesInput.addEventListener('input', function() {
        const value = parseInt(this.value);
        if (value < 1) this.value = 1;
        if (value > 50) this.value = 50;
    });
});

// Add some visual feedback for form interactions
document.querySelectorAll('.form-input').forEach(input => {
    input.addEventListener('focus', function() {
        this.parentElement.classList.add('focused');
    });
    
    input.addEventListener('blur', function() {
        this.parentElement.classList.remove('focused');
    });
});
