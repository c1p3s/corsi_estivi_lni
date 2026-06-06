/* ==========================================================================
   1. STRUTTURA LOGICA PER APERTURA MODALI ORIGINALI (INDEX.HTML)
   ========================================================================== */
// Nota: Se avevi già delle funzioni per aprire le modali (es. cliccando sulle schede),
// assicurati che coesistano felicemente. Questo blocco gestisce l'ascolto dei click 
// sulle immagini SOLO dopo che sono state cliccate all'interno della modale.

document.addEventListener("DOMContentLoaded", () => {

    // ----------------------------------------------------------------------
    // 2. CREAZIONE DEL LIGHTBOX (IL CAROSELLO A SCHERMO INTERO)
    // ----------------------------------------------------------------------
    let lightbox = document.getElementById("custom-lightbox");
    if (!lightbox) {
        lightbox = document.createElement("div");
        lightbox.id = "custom-lightbox";
        
        // Stili per sovrapporsi alla modale aperta
        Object.assign(lightbox.style, {
            position: "fixed",
            top: "0",
            left: "0",
            width: "100%",
            height: "100%",
            backgroundColor: "rgba(0, 0, 0, 0.95)",
            display: "none",
            justifyContent: "center",
            alignItems: "center",
            zIndex: "999999", // Sopra a tutto
            userSelect: "none"
        });

        lightbox.innerHTML = `
            <span id="lightbox-close" style="position:absolute; top:20px; right:30px; color:#ffffff; font-size:45px; font-weight:bold; cursor:pointer; line-height:1; z-index:1000000;">&times;</span>
            <span id="lightbox-prev" style="position:absolute; left:25px; color:#ffffff; font-size:55px; font-weight:bold; cursor:pointer; padding:15px; z-index:1000000;">&#10094;</span>
            <img id="lightbox-img" src="" alt="Galleria Vela" style="max-width:90%; max-height:85%; border-radius:6px; box-shadow:0 0 25px rgba(0,0,0,0.8); object-fit:contain;">
            <span id="lightbox-next" style="position:absolute; right:25px; color:#ffffff; font-size:55px; font-weight:bold; cursor:pointer; padding:15px; z-index:1000000;">&#10095;</span>
        `;
        document.body.appendChild(lightbox);
    }

    const lightboxImg = lightbox.querySelector("#lightbox-img");
    const closeBtn = lightbox.querySelector("#lightbox-close");
    const prevBtn = lightbox.querySelector("#lightbox-prev");
    const nextBtn = lightbox.querySelector("#lightbox-next");

    let currentImagesArray = [];
    let currentIndex = 0;

    // Aggiunge la manina alle immagini della galleria nelle modali senza rompere l'HTML
    const style = document.createElement("style");
    style.textContent = `
        .gallery-grid img, .modal-inner-body img { cursor: pointer !important; }
        #lightbox-close:hover, #lightbox-prev:hover, #lightbox-next:hover { color: #ffcc00 !important; }
    `;
    document.head.appendChild(style);

    // ----------------------------------------------------------------------
    // 3. GESTORE DEI CLICK ISOLATO (NON COPRE/NON BLOCCA LE MODALI)
    // ----------------------------------------------------------------------
    // Invece di intercettare tutto il body bloccando gli eventi, ascoltiamo i click
    // e agiamo SOLO se l'utente sta cliccando specificamente su un'immagine dentro una galleria.
    document.addEventListener("click", (e) => {
        // Controlla se il click è avvenuto su un'immagine dentro la griglia della galleria (.gallery-grid)
        const galleryGrid = e.target.closest(".gallery-grid");
        
        if (e.target.tagName === "IMG" && galleryGrid) {
            // Se siamo dentro una galleria, allora attiviamo il carosello
            currentImagesArray = Array.from(galleryGrid.querySelectorAll("img"));
            currentIndex = currentImagesArray.indexOf(e.target);

            if (currentIndex !== -1) {
                lightboxImg.src = currentImagesArray[currentIndex].src;
                lightbox.style.display = "flex";
            }
        }
    });

    // ----------------------------------------------------------------------
    // 4. CONTROLLI DI NAVIGAZIONE DEL CAROSELLO
    // ----------------------------------------------------------------------
    function showNext() {
        if (currentImagesArray.length > 0) {
            currentIndex = (currentIndex + 1) % currentImagesArray.length;
            lightboxImg.src = currentImagesArray[currentIndex].src;
        }
    }

    // Corretto l'ordine logico del ciclo all'indietro
    function showPrev() {
        if (currentImagesArray.length > 0) {
            currentIndex = (currentIndex - 1 + currentImagesArray.length) % currentImagesArray.length;
            lightboxImg.src = currentImagesArray[currentIndex].src;
        }
    }

    function closeLightbox() {
        lightbox.style.display = "none";
        lightboxImg.src = "";
    }

    // Gestione eventi click sui controlli del Lightbox
    nextBtn.addEventListener("click", (e) => { e.stopPropagation(); showNext(); });
    prevBtn.addEventListener("click", (e) => { e.stopPropagation(); showPrev(); });
    closeBtn.addEventListener("click", (e) => { e.stopPropagation(); closeLightbox(); });
    
    // Chiude se clicchi fuori dall'immagine
    lightbox.addEventListener("click", (e) => {
        if (e.target === lightbox) closeLightbox();
    });

    // Controlli da tastiera
    window.addEventListener("keydown", (e) => {
        if (lightbox.style.display === "flex") {
            if (e.key === "ArrowRight") showNext();
            if (e.key === "ArrowLeft") showPrev();
            if (e.key === "Escape") closeLightbox();
        }
    });
});