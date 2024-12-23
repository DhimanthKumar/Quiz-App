import Math;
    const start = new Date();
    const time = document.getElementById('timer');
    const timeout = Number(time.textContent)*60*1000
// Simulate a delay
setInterval(() => {
    const end = new Date();
    const elapsed = end - start; // Difference in milliseconds
    const curtimer= timeout-(end-start);
    console.log(`Elapsed time: ${math.floor(curtimer/(1000*60)) }ms`);
}, 500);