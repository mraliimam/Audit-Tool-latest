document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('uploadForm');
    const fileInput = document.getElementById('file');
    const loader = document.getElementById('loader');
    const submitButton = form.querySelector('button[type="submit"]');
    const fileLabel = document.querySelector('.file-text');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    form.appendChild(errorDiv);

    function showError(message) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        loader.style.display = 'none';
        submitButton.disabled = false;
    }

    function updateFileName(file) {
        if (file) {
            fileLabel.textContent = file.name;
        } else {
            fileLabel.textContent = 'Choose a file or drag it here';
        }
    }

    // Handle drag and drop
    const dropZone = document.querySelector('.upload-area');

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        dropZone.classList.add('drag-over');
    }

    function unhighlight(e) {
        dropZone.classList.remove('drag-over');
    }

    dropZone.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const file = dt.files[0];
        fileInput.files = dt.files;
        handleFileSelect(file);
    }

    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        handleFileSelect(file);
    });

    function handleFileSelect(file) {
        if (file) {
            const extension = file.name.split('.').pop().toLowerCase();
            if (!['xlsx', 'xls'].includes(extension)) {
                fileInput.value = '';
                showError('Please select an Excel file (.xlsx or .xls)');
                updateFileName(null);
            } else {
                errorDiv.style.display = 'none';
                updateFileName(file);
            }
        }
    }

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        if (!fileInput.files[0]) {
            showError('Please select a file');
            return;
        }

        errorDiv.style.display = 'none';
        loader.style.display = 'flex';
        submitButton.disabled = true;

        const formData = new FormData(form);

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                // Handle successful file download
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'files.zip';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                
                // Reset form
                form.reset();
                updateFileName(null);
            } else {
                const data = await response.json();
                showError(data.error || 'An error occurred during processing');
            }
        } catch (error) {
            showError('An error occurred during processing');
        } finally {
            loader.style.display = 'none';
            submitButton.disabled = false;
        }
    });
});