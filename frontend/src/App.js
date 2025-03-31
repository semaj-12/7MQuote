import React, { useState } from "react";
import FileUpload from "./components/FileUpload";

function App() {
    const [urn, setUrn] = useState(null);
    const [selectedFile, setSelectedFile] = useState(null);

    return (
        <div className="container">
            <h1>Blueprint Processing App</h1>
            <FileUpload setUrn={setUrn} setSelectedFile={setSelectedFile} />
        </div>
    );
}

export default App;
