const btn = document.getElementById("talk");
const textField = document.getElementById("text");
const summaryField = document.getElementById("summary");

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

const getSummary = async (text) => {
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
    summaryField.innerText = summary;
}

recognition.onstart = () => {
    console.log("Listening"); 
};

recognition.onresult = (event) => {
    const current = event.resultIndex;
    const transcript = event.results[current][0].transcript;
    textField.innerText = transcript;
    getSummary(transcript);
};

btn.addEventListener("click", () => {
    recognition.start();
});