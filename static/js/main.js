document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("nexusCanvas");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    let cw, ch;

    // Testo
    const rawText = "Siamo Nexus, un team universitario di robotica con base all'Innovation Lab di Asperastra a Trieste. Progettiamo e costruiamo robot combinando programmazione, elettronica e meccanica: dai robot a due ruote con sensori ottici, alle piattaforme di bilanciamento dinamico su più gradi di libertà, fino ai bracci robotici articolati. Il nostro obiettivo è imparare sperimentando direttamente sull'hardware, sviluppando software di controllo, algoritmi di cinematica e sistemi di visione artificiale. Questa griglia interattiva dimostra in tempo reale come un algoritmo può calcolare vettori di repulsione ed evitare ostacoli al tocco del cursore.";
    const words = rawText.split(" ");

    let anomX = 0, anomY = 0;
    let targetX = 0, targetY = 0;
    const anomRadius = 110;

    function resize() {
        cw = canvas.parentElement.clientWidth;
        ch = canvas.parentElement.clientHeight;
        canvas.width = cw;
        canvas.height = ch;
        if (anomX === 0) {
            anomX = targetX = cw / 2;
            anomY = targetY = ch / 2;
        }
    }
    window.addEventListener("resize", resize);
    resize();

    canvas.addEventListener("mousedown", (e) => {
        const rect = canvas.getBoundingClientRect();
        targetX = Math.max(anomRadius/2, Math.min(cw - anomRadius/2, e.clientX - rect.left));
        targetY = Math.max(anomRadius/2, Math.min(ch - anomRadius/2, e.clientY - rect.top));
    });

    function drawASCIIAnomaly(x, y, time) {
        ctx.font = "14px 'Share Tech Mono', monospace";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        
        const chars = ["#", "@", "%", "&", "M", "0", "1", "*"];
        const gridSize = 6;
        const spacing = 16;

        for (let i = -gridSize; i <= gridSize; i++) {
            for (let j = -gridSize; j <= gridSize; j++) {
                const dist = Math.sqrt(i*i + j*j);
                if (dist > gridSize + 1) continue;
                
                const wave = Math.sin(time * 0.005 - dist * 0.5);
                if (wave > 0) {
                    ctx.fillStyle = `rgba(0, 240, 255, ${wave})`;
                    const charIndex = Math.floor(Math.abs(Math.sin(dist + time*0.01)) * chars.length) % chars.length;
                    ctx.fillText(chars[charIndex], x + i * spacing, y + j * spacing);
                }
            }
        }
    }

    function animate(time) {
        anomX += (targetX - anomX) * 0.1;
        anomY += (targetY - anomY) * 0.1;

        ctx.clearRect(0, 0, cw, ch);

        ctx.font = "15px 'Share Tech Mono', monospace";
        ctx.fillStyle = "#dfdfe6";
        ctx.textAlign = "left";
        ctx.textBaseline = "top";

        let textX = 30;
        let textY = 30;
        const lineHeight = 30;

        for (let i = 0; i < words.length; i++) {
            const word = words[i];
            const wordWidth = ctx.measureText(word + " ").width;

            if (textX + wordWidth > cw - 30) {
                textX = 30;
                textY += lineHeight;
            }

            const wordCenterX = textX + wordWidth / 2;
            const wordCenterY = textY + lineHeight / 2;
            const dx = wordCenterX - anomX;
            const dy = wordCenterY - anomY;
            const dist = Math.sqrt(dx*dx + dy*dy);

            if (dist < anomRadius) {
                textX = anomX + Math.sqrt(Math.max(0, Math.pow(anomRadius, 2) - Math.pow(dy, 2))) + 5;
                if (textX + wordWidth > cw - 30) {
                    textX = 30;
                    textY += lineHeight;
                }
            }

            if (word.includes('Nexus') || word.includes('matematica') || word.includes('hardware')) {
                ctx.fillStyle = '#00f0ff';
            } else {
                ctx.fillStyle = '#dfdfe6';
            }

            if(textY < ch - 30) {
                ctx.fillText(word, textX, textY);
            }
            textX += wordWidth;
        }

        drawASCIIAnomaly(anomX, anomY, time);
        requestAnimationFrame(animate);
    }
    requestAnimationFrame(animate);
});

// Gestione rotazione video random nella Hero
document.addEventListener("DOMContentLoaded", () => {
    // Cerchiamo un possibile video sia in inde.html (heroVideo) che in project.html (projectVideo)
    const heroVideo = document.getElementById("heroVideo") || document.getElementById("projectVideo");
    if (!heroVideo) return;

    const videos = [
        "/static/videos/carousel.mp4",
        "/static/videos/carousel2.mp4",
        "/static/videos/carousel3.mp4",
        "/static/videos/carousel4.mp4"
    ];

    let currentVideo = "";
    
    // Funzione per impostare un nuovo video randomico
    function playRandomVideoSnippet() {
        let nextVideo = videos[Math.floor(Math.random() * videos.length)];
        
        // Evita di ripetere lo stesso video due volte di fila
        while(nextVideo === currentVideo && videos.length > 1) {
            nextVideo = videos[Math.floor(Math.random() * videos.length)];
        }
        
        currentVideo = nextVideo;
        heroVideo.src = currentVideo;
        heroVideo.play().catch(e => console.log("Auto-play prevented", e));
        
        // Scegli una durata random tra 2.5 e 4.5 secondi
        const snippetDuration = Math.random() * 2000 + 2500;
        
        setTimeout(() => {
            playRandomVideoSnippet();
        }, snippetDuration);
    }

    // Inizia la rotazione
    playRandomVideoSnippet();
});
