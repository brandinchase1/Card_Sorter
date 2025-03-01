const video = document.getElementById("video");
        const canvas = document.getElementById("img_canvas");
        const context = canvas.getContext("2d");
        const textBox = document.getElementById("cardData");
        const log = document.getElementById("log");
        const start_stop_btn = document.getElementById("start_stop");
        const cards = {};
        let stream = null;
        let start = true;


        function toggle_camera() {
            if (start) {
                startCamera();
                start_stop_btn.textContent = "Stop Camera";
            }
            else {
                stopCamera();
                start_stop_btn.textContent = "Start Camera";
            }
            start = !start;
        }

        // Start the camera
        async function startCamera() {
            stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
        }

        function stopCamera() {
            if (stream !== null) {
            stream.getTracks().forEach(function(track) {
                track.stop();
              });
            }
        }

        function clearLog() {
            log.value = "TO START:\n1) Allow Camera Access\n2) Display Card in the Frame\n3) Click Capture or Press Enter to Begin\n\n";
        }

        function displayCardData(data) {
            textBox.value = "";

            for (let key in data) {
                textBox.value += `${data[key]} ${key}\n`;
            }
        }

        async function captureFrame() {
            log.value += `Query Started\n`;
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            
            canvas.toBlob(blob => {
            
                if (blob === null) {log.value += `No Camera in use\n`; return;}
                let formData = new FormData();
                formData.append("file", blob, "frame.jpg");

                fetch("http://127.0.0.1:5000/upload", {
                    method: "POST",
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    let text = data.text.join(" ");
                    if (text) {
                        if (text in cards) {cards[text] += 1;}
                        else {cards[text] = 1;}
                        displayCardData(cards)
                    }
                    log.value += `Query Complete. Found: ${text}\n`;
                })
                .catch(error => log.value += ("Error:", error));
            }, "image/jpeg");
        }

        document.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {captureFrame()}
        });
        clearLog();
        toggle_camera();
