import React, { useEffect, useRef } from "react";

const ForgeViewer = ({ urn }) => {
    const viewerRef = useRef(null);

    useEffect(() => {
        let viewer;
        const options = {
            env: "AutodeskProduction",
            getAccessToken: async (onSuccess) => {
                const response = await fetch("http://127.0.0.1:5000/authenticate");
                const data = await response.json();
                onSuccess(data.access_token, data.expires_in);
            },
        };

        window.Autodesk.Viewing.Initializer(options, () => {
            if (!viewerRef.current) return;

            const viewerDiv = viewerRef.current;
            viewer = new window.Autodesk.Viewing.GuiViewer3D(viewerDiv);
            viewer.start();

            const documentId = `urn:${urn}`;
            window.Autodesk.Viewing.Document.load(documentId, (doc) => {
                const defaultViewable = doc.getRoot().getDefaultGeometry();
                viewer.loadDocumentNode(doc, defaultViewable);
            });
        });

        return () => {
            if (viewer) viewer.finish();
        };
    }, [urn]);

    return <div ref={viewerRef} style={{ width: "100%", height: "600px" }} />;
};

export default ForgeViewer;
