import streamlit as st
import streamlit.components.v1 as components

# Define the HTML and JavaScript for accessing the webcam
html_code = """
<!DOCTYPE html>
<html>
<head>
    <title>Webcam Stream</title>
</head>
<body>
    <h1>Webcam Stream</h1>
    <video id="webcam" width="640" height="480" autoplay></video>
    <script>
        async function startWebcam() {
            const video = document.getElementById('webcam');
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                video.srcObject = stream;
            } catch (err) {
                console.error('Error accessing webcam: ', err);
            }
        }
        startWebcam();
    </script>
</body>
</html>
"""

# Use Streamlit components to render the HTML
components.html(html_code, height=600)
