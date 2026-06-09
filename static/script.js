const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const uploadDropzone = document.getElementById('uploadDropzone');
const loadingState = document.getElementById('loading');
const resultSection = document.getElementById('resultSection');
const mediaContainer = document.getElementById('mediaContainer');
const downloadCsvBtn = document.getElementById('downloadCsvBtn');

uploadBtn.addEventListener('click', () => {
    fileInput.click();
});

uploadDropzone.addEventListener('click', (e) => {
    if (e.target !== uploadBtn) {
        fileInput.click();
    }
});

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    uploadDropzone.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    uploadDropzone.addEventListener(eventName, () => {
        uploadDropzone.classList.add('dragover');
    }, false);
});

['dragleave', 'drop'].forEach(eventName => {
    uploadDropzone.addEventListener(eventName, () => {
        uploadDropzone.classList.remove('dragover');
    }, false);
});

uploadDropzone.addEventListener('drop', (e) => {
    let dt = e.dataTransfer;
    let files = dt.files;

    if (files.length > 0) {
        fileInput.files = files;
        handleFileSelect({ target: fileInput });
    }
});

fileInput.addEventListener('change', handleFileSelect);

async function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    uploadDropzone.classList.add('hidden');
    loadingState.classList.remove('hidden');
    resultSection.classList.add('hidden');
    mediaContainer.innerHTML = '';

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.error || 'An error occurred during processing.');
            resetUploadState();
        } else {
            downloadCsvBtn.href = data.csv_url;
            displayResult(data.url, data.type);
        }
    } catch (error) {
        alert('Network error. Ensure the Flask server is running.');
        console.error(error);
        resetUploadState();
    } finally {
        loadingState.classList.add('hidden');
    }
}

function resetUploadState() {
    uploadDropzone.classList.remove('hidden');
    loadingState.classList.add('hidden');
}

function displayResult(url, type) {
    if (type === 'video') {
        mediaContainer.innerHTML = `
            <video controls autoplay loop>
                <source src="${url}" type="video/mp4">
                Your browser does not support the video tag.
            </video>`;
    } else {
        mediaContainer.innerHTML = `<img src="${url}" alt="Neural Network Output">`;
    }

    resultSection.classList.remove('hidden');
    uploadDropzone.classList.remove('hidden'); // Allow uploading more easily
}