import React, { useState } from "react";
import axios from "axios";

const FileUpload = ({ setUrn, setSelectedFile }) => {
    const [file, setFile] = useState(null);
    const [progress, setProgress] = useState(0);
    const [statusMessage, setStatusMessage] = useState("");

    // Handle file selection
    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];
        setFile(selectedFile);
        setProgress(0);
        setStatusMessage("");

        // If it's a PDF, store it for processing in PdfProcessor
        if (selectedFile.type === "application/pdf") {
            setSelectedFile(selectedFile);
        }
    };

    // Handle file upload to backend
    const handleUpload = async () => {
        if (!file) {
            setStatusMessage("Please select a file to upload.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
            setStatusMessage("Uploading...");

            const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
                headers: { "Content-Type": "multipart/form-data" },
                onUploadProgress: (progressEvent) => {
                    const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    setProgress(percentCompleted);
                },
            });

            if (response.data.urn) {
                setUrn(response.data.urn); // Pass URN to App.js for Forge Viewer
                setStatusMessage("Upload complete! Processing file...");
            } else {
                setStatusMessage("Upload failed. No URN returned.");
            }
        } catch (error) {
            setStatusMessage("Error uploading file.");
        }
    };

    return (
        <div>
            <h2>Upload Blueprint or PDF</h2>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload</button>

            {progress > 0 && (
                <div style={{ width: "100%", backgroundColor: "#ddd", marginTop: "10px" }}>
                    <div style={{ width: `${progress}%`, backgroundColor: "green", height: "20px" }}></div>
                </div>
            )}

            <p>{statusMessage}</p>
        </div>
    );
};

export default FileUpload;
