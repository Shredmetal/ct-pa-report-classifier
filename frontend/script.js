// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const uploadZone = document.getElementById('uploadZone');
const fileInput = document.getElementById('fileInput');
const uploadProgress = document.getElementById('uploadProgress');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const sourceFilesList = document.getElementById('sourceFilesList');
const processedFilesList = document.getElementById('processedFilesList');
const processSection = document.getElementById('processSection');
const processingSection = document.getElementById('processingSection');
const processingStatus = document.getElementById('processingStatus');
const processingResults = document.getElementById('processingResults');
const outputPrefix = document.getElementById('outputPrefix');
const llmBaseUrl = document.getElementById('llmBaseUrl');
const toastContainer = document.getElementById('toastContainer');

// Buttons
const refreshSourceBtn = document.getElementById('refreshSourceBtn');
const clearSourceBtn = document.getElementById('clearSourceBtn');
const refreshProcessedBtn = document.getElementById('refreshProcessedBtn');
const clearProcessedBtn = document.getElementById('clearProcessedBtn');
const processBtn = document.getElementById('processBtn');

// State Management
let sourceFiles = [];
let processedFiles = [];
let selectedFiles = [];

// Utility Functions
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    toastContainer.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }, 4000);
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatDate(timestamp) {
    return new Date(timestamp * 1000).toLocaleString();
}

// API Functions
async function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/upload-csv`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Upload failed');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Upload error:', error);
        throw error;
    }
}

async function loadSourceFiles() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/source-files`);
        if (!response.ok) throw new Error('Failed to load source files');
        
        const data = await response.json();
        sourceFiles = data.files || [];
        renderSourceFiles();
    } catch (error) {
        console.error('Error loading source files:', error);
        showToast('Failed to load source files', 'error');
        sourceFilesList.innerHTML = '<div class="loading">Error loading files</div>';
    }
}

async function loadProcessedFiles() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/processed-files`);
        if (!response.ok) throw new Error('Failed to load processed files');
        
        const data = await response.json();
        processedFiles = data.files || [];
        renderProcessedFiles();
    } catch (error) {
        console.error('Error loading processed files:', error);
        showToast('Failed to load processed files', 'error');
        processedFilesList.innerHTML = '<div class="loading">Error loading files</div>';
    }
}

async function processFiles() {
    if (selectedFiles.length === 0) {
        showToast('Please select files to process', 'warning');
        return;
    }
    
    const prefix = outputPrefix.value.trim() || 'processed_reports';
    const llmUrl = llmBaseUrl.value.trim() || 'http://localhost:5001/v1/';
    
    try {
        processingSection.classList.remove('hidden');
        processingStatus.classList.remove('hidden');
        processingResults.classList.add('hidden');
        
        const response = await fetch(`${API_BASE_URL}/api/process-files`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filenames: selectedFiles,
                output_prefix: prefix,
                llm_base_url: llmUrl
            })
        });
        
        const data = await response.json();
        
        processingStatus.classList.add('hidden');
        processingResults.classList.remove('hidden');
        
        if (!response.ok) {
            throw new Error(data.detail || 'Processing failed');
        }
        
        // Display results
        displayProcessingResults(data, llmUrl);
        showToast('Files processed successfully!', 'success');
        
        // Refresh processed files list and clear selection
        await loadProcessedFiles();
        selectedFiles = [];
        renderSourceFiles();
        updateProcessSection();
        
    } catch (error) {
        console.error('Processing error:', error);
        processingStatus.classList.add('hidden');
        processingResults.innerHTML = `
            <div class="result-item result-error">
                <strong>Processing Failed:</strong> ${error.message}
            </div>
        `;
        processingResults.classList.remove('hidden');
        showToast('Processing failed: ' + error.message, 'error');
    }
}

async function deleteFiles(filenames, directory) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/delete-files`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filenames: filenames,
                directory: directory
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Delete failed');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Delete error:', error);
        throw error;
    }
}

async function clearDirectory(directory) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/clear-directory/${directory}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Clear failed');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Clear error:', error);
        throw error;
    }
}

// Rendering Functions
function renderSourceFiles() {
    if (sourceFiles.length === 0) {
        sourceFilesList.innerHTML = '<div class="loading">No source files found</div>';
        return;
    }
    
    const html = sourceFiles.map(file => `
        <div class="file-item ${selectedFiles.includes(file.filename) ? 'selected' : ''}">
            <div class="file-info">
                <input type="checkbox" class="file-checkbox" 
                       ${selectedFiles.includes(file.filename) ? 'checked' : ''}
                       onchange="toggleFileSelection('${file.filename}')">
                <div class="file-details">
                    <h4>${file.filename}</h4>
                    <div class="file-meta">
                        ${formatFileSize(file.size)} • Modified ${formatDate(file.modified)}
                    </div>
                </div>
            </div>
            <div class="file-actions">
                <button class="btn btn-danger btn-small" onclick="deleteSourceFile('${file.filename}')">
                    🗑️ Delete
                </button>
            </div>
        </div>
    `).join('');
    
    sourceFilesList.innerHTML = html;
}

function renderProcessedFiles() {
    if (processedFiles.length === 0) {
        processedFilesList.innerHTML = '<div class="loading">No processed files found</div>';
        return;
    }
    
    const html = processedFiles.map(file => `
        <div class="file-item">
            <div class="file-info">
                <div class="file-details">
                    <h4>${file.filename}</h4>
                    <div class="file-meta">
                        ${formatFileSize(file.size)} • Modified ${formatDate(file.modified)}
                    </div>
                </div>
            </div>
            <div class="file-actions">
                <button class="btn btn-secondary btn-small" onclick="downloadFile('${file.filename}', 'output')">
                    📥 Download
                </button>
                <button class="btn btn-danger btn-small" onclick="deleteProcessedFile('${file.filename}')">
                    🗑️ Delete
                </button>
            </div>
        </div>
    `).join('');
    
    processedFilesList.innerHTML = html;
}

function displayProcessingResults(data, llmUrl) {
    const results = data.file_results || [];
    
    const headerInfo = `
        <div class="result-item result-success">
            <strong>Processing Summary:</strong><br>
            LLM Endpoint: ${llmUrl}<br>
            Total Files: ${data.total_files_processed || 0}<br>
            Total Reports: ${data.total_reports_processed || 0}<br>
            Status: ${data.overall_status || 'Unknown'}
        </div>
    `;
    
    const html = results.map(result => {
        let className = 'result-success';
        if (result.status === 'failed') className = 'result-error';
        if (result.status === 'skipped') className = 'result-warning';
        
        return `
            <div class="result-item ${className}">
                <strong>${result.filename}:</strong> ${result.message || result.status}
                ${result.reports_processed ? `<br>Reports processed: ${result.reports_processed}` : ''}
                ${result.error ? `<br>Error: ${result.error}` : ''}
            </div>
        `;
    }).join('');
    
    processingResults.innerHTML = headerInfo + html;
}

function updateProcessSection() {
    if (selectedFiles.length > 0) {
        processSection.classList.remove('hidden');
        processBtn.textContent = `⚡ Process ${selectedFiles.length} Selected File${selectedFiles.length > 1 ? 's' : ''}`;
    } else {
        processSection.classList.add('hidden');
    }
}

// Event Handlers
function toggleFileSelection(filename) {
    if (selectedFiles.includes(filename)) {
        selectedFiles = selectedFiles.filter(f => f !== filename);
    } else {
        selectedFiles.push(filename);
    }
    renderSourceFiles();
    updateProcessSection();
}

async function deleteSourceFile(filename) {
    if (!confirm(`Are you sure you want to delete "${filename}"?`)) return;
    
    try {
        await deleteFiles([filename], 'source');
        showToast(`File "${filename}" deleted successfully`, 'success');
        await loadSourceFiles();
        selectedFiles = selectedFiles.filter(f => f !== filename);
        updateProcessSection();
    } catch (error) {
        showToast('Failed to delete file: ' + error.message, 'error');
    }
}

async function deleteProcessedFile(filename) {
    if (!confirm(`Are you sure you want to delete "${filename}"?`)) return;
    
    try {
        await deleteFiles([filename], 'output');
        showToast(`File "${filename}" deleted successfully`, 'success');
        await loadProcessedFiles();
    } catch (error) {
        showToast('Failed to delete file: ' + error.message, 'error');
    }
}

function downloadFile(filename, directory) {
    // Use the proper download endpoint
    const url = `${API_BASE_URL}/api/download-file/${directory}/${filename}`;
    
    // Create a temporary link element for download
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showToast(`Downloading ${filename}...`, 'success');
}

// File Upload Handlers
function handleFiles(files) {
    const fileArray = Array.from(files);
    const csvFiles = fileArray.filter(file => file.name.toLowerCase().endsWith('.csv'));
    
    if (csvFiles.length === 0) {
        showToast('Please select CSV files only', 'warning');
        return;
    }
    
    if (csvFiles.length !== fileArray.length) {
        showToast('Some files were skipped (only CSV files are supported)', 'warning');
    }
    
    uploadFiles(csvFiles);
}

async function uploadFiles(files) {
    if (files.length === 0) return;
    
    uploadProgress.classList.remove('hidden');
    let uploaded = 0;
    
    for (const file of files) {
        try {
            progressText.textContent = `Uploading ${file.name}...`;
            await uploadFile(file);
            uploaded++;
            
            const progress = (uploaded / files.length) * 100;
            progressFill.style.width = `${progress}%`;
            
        } catch (error) {
            showToast(`Failed to upload ${file.name}: ${error.message}`, 'error');
        }
    }
    
    progressText.textContent = `Upload complete! ${uploaded}/${files.length} files uploaded.`;
    
    setTimeout(() => {
        uploadProgress.classList.add('hidden');
        progressFill.style.width = '0%';
    }, 2000);
    
    if (uploaded > 0) {
        showToast(`Successfully uploaded ${uploaded} file${uploaded > 1 ? 's' : ''}`, 'success');
        await loadSourceFiles();
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Load initial data
    loadSourceFiles();
    loadProcessedFiles();
    
    // Upload zone events
    uploadZone.addEventListener('click', () => fileInput.click());
    
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });
    
    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('dragover');
    });
    
    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
        handleFiles(e.dataTransfer.files);
    });
    
    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
        e.target.value = ''; // Reset input
    });
    
    // Button events
    refreshSourceBtn.addEventListener('click', loadSourceFiles);
    refreshProcessedBtn.addEventListener('click', loadProcessedFiles);
    processBtn.addEventListener('click', processFiles);
    
    clearSourceBtn.addEventListener('click', async () => {
        if (!confirm('Are you sure you want to delete ALL source files?')) return;
        
        try {
            await clearDirectory('source');
            showToast('All source files deleted successfully', 'success');
            await loadSourceFiles();
            selectedFiles = [];
            updateProcessSection();
        } catch (error) {
            showToast('Failed to clear source files: ' + error.message, 'error');
        }
    });
    
    clearProcessedBtn.addEventListener('click', async () => {
        if (!confirm('Are you sure you want to delete ALL processed files?')) return;
        
        try {
            await clearDirectory('output');
            showToast('All processed files deleted successfully', 'success');
            await loadProcessedFiles();
        } catch (error) {
            showToast('Failed to clear processed files: ' + error.message, 'error');
        }
    });
});

// Add slide out animation for toasts
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
