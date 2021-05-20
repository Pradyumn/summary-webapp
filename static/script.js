const talkBtn = document.getElementById("talk");
const summBtn = document.getElementById("summarize");
const textField = document.getElementById("text");
const loader = document.getElementById("loader");
const summaryField = document.getElementById("summary");

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

const getSummary = async (text) => {
    loader.style.display = "";
    let cleanedText = text.toLowerCase();
    cleanedText = cleanedText.replaceAll(/[0-9]+/g, "#");
    cleanedText = cleanedText.replaceAll(/[,.]/g, "");
    console.log(cleanedText)
    const res = await fetch("/summary", {
        method: 'POST', 
        body: JSON.stringify({
            text: cleanedText
        })
    });

    const  { summary } = await res.json();
    summaryField.value = summary;
    loader.style.display = "none";
}

recognition.onstart = () => {
    console.log("Listening"); 
};

recognition.onresult = (event) => {
    const current = event.resultIndex;
    const transcript = event.results[current][0].transcript;
    textField.value = transcript;
};

talkBtn.addEventListener("click", () => {
    recognition.start();
});

summBtn.addEventListener("click", () => {
    const transcript = textField.value;
    getSummary(transcript);
});
