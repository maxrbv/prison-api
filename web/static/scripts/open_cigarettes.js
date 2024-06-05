document.getElementById('cigarette-pack').addEventListener('click', async () => {
    const tg = window.Telegram.WebApp
    fetch('/api/v1/open_cigarettes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({id: tg.initDataUnsafe.user.id})
    })
        .then(response => response.json())
        .then(data => {
            const cigaretteCountElement = document.getElementById('cigarette-count');
            let currentCount = parseInt(cigaretteCountElement.innerText.split(': ')[1]);
            currentCount += data.cigarette_count;
            cigaretteCountElement.innerText = 'Cigarette Count: ' + currentCount;
        })
        .catch(error => {
            console.error('Error:', error);
        });
});