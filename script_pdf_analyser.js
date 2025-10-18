// Get DOM elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const uploadBtn = document.getElementById('uploadBtn');
const uploadSection = document.getElementById('uploadSection');
const displaySection = document.getElementById('displaySection');
const removeFileBtn = document.getElementById('removeFileBtn');
const backBtn = document.getElementById('backBtn');
const loadingScreen = document.getElementById('loadingScreen');

// Store selected file
let selectedFile = null;

// Click to upload
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

// File input change
fileInput.addEventListener('change', (e) => {
    handleFile(e.target.files[0]);
});

// Drag over
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

// Drag leave
uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

// Drop file
uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    handleFile(e.dataTransfer.files[0]);
});

// Handle file selection
function handleFile(file) {
    if (file) {
        selectedFile = file;
        fileName.textContent = file.name;
        fileSize.textContent = formatFileSize(file.size);
        fileInfo.classList.add('active');
        uploadBtn.disabled = false;
    }
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Upload button click
uploadBtn.addEventListener('click', () => {
    if (selectedFile) {
        // Show loading screen
        loadingScreen.classList.add('active');
        
        // Simulate processing time (1.5 seconds)
        setTimeout(() => {
            loadingScreen.classList.remove('active');
            showDisplay();
        }, 1500);
    }
});

// Show display section
function showDisplay() {
    uploadSection.style.display = 'none';
    displaySection.classList.add('active');
}

// Show upload section
function showUpload() {
    displaySection.classList.remove('active');
    uploadSection.style.display = 'block';
}

// Remove file
function removeFile() {
    selectedFile = null;
    fileInput.value = '';
    fileName.textContent = '';
    fileSize.textContent = '';
    fileInfo.classList.remove('active');
    uploadBtn.disabled = true;
}

// Event listeners for buttons
removeFileBtn.addEventListener('click', removeFile);
backBtn.addEventListener('click', showUpload);