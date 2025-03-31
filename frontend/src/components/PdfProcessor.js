import React, { useState, useEffect } from "react";
import * as pdfjsLib from "pdfjs-dist/build/pdf";

const PdfProcessor = ({ file }) => {
    const [text, setText] = useState("");
    const [imageURLs, setImageURLs] = useState([]);

    useEffect(() => {
        if (file) {
            extractTextAndImages(file);
        }
    }, [file]);

    const extractTextAndImages = async (pdfFile) => {
        const fileReader = new FileReader();
        fileReader.readAsArrayBuffer(pdfFile);

        fileReader.onload = async () => {
            const pdfData = new Uint8Array(fileReader.result);
            pdfjsLib.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.js`;

            const pdfDoc = await pdfjsLib.getDocument({ data: pdfData }).promise;
            let extractedText = "";
            let images = [];

            for (let pageNum = 1; pageNum <= pdfDoc.numPages; pageNum++) {
                const page = await pdfDoc.getPage(pageNum);
                const textContent = await page.getTextContent();
                extractedText += textContent.items.map(item => item.str).join(" ") + "\n";

                const viewport = page.getViewport({ scale: 1.5 });
                const canvas = document.createElement("canvas");
                const context = canvas.getContext("2d");
                canvas.width = viewport.width;
                canvas.height = viewport.height;

                await page.render({ canvasContext: context, viewport }).promise;
                images.push(canvas.toDataURL("image/png"));
            }

            setText(extractedText);
            setImageURLs(images);
        };
    };

    return (
        <div>
            <h3>Extracted Text:</h3>
            <p>{text}</p>
            <h3>Extracted Images:</h3>
            {imageURLs.map((img, index) => (
                <img key={index} src={img} alt={`Extracted Image ${index + 1}`} style={{ maxWidth: "100px", margin: "5px" }} />
            ))}
        </div>
    );
};

export default PdfProcessor;
