document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById('file');
    if (!fileInput.files[0]) {
        alert('Please select a file to upload.');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
    });

    const result = await response.json();
    if (response.ok) {
        alert('Image uploaded successfully!');
        document.getElementById('filters').classList.remove('hidden');
        localStorage.setItem('uploadedFilePath', result.filepath);
    } else {
        alert(result.error || 'Failed to upload image.');
    }
});

document.getElementById('applyFilter').addEventListener('click', async () => {
    const selectedFilter = document.getElementById('filterSelect').value;
    const filePath = localStorage.getItem('uploadedFilePath');

    if (!filePath) {
        alert('No uploaded file found.');
        return;
    }

    const response = await fetch('/filter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filepath: filePath, filter: selectedFilter }),
    });

    const result = await response.json();
    if (response.ok) {
        alert('Filter applied successfully!');
        const filteredFilePath = result.filtered_filepath;
        document.getElementById('filteredImage').src = filteredFilePath;
        document.getElementById('downloadLink').href = `/download?filepath=${filteredFilePath}`;
        document.getElementById('result').classList.remove('hidden');
    } else {
        alert(result.error || 'Failed to apply filter.');
    }
});
