document.addEventListener('DOMContentLoaded', async function () {
    async function updateCigaretteCount() {
        try {
            const tg = window.Telegram.WebApp
            const response = await fetch('/api/v1/current_cigarettes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({id: tg.initDataUnsafe.user.id})
            });
            const data = await response.json();
            const cigaretteCountElement = document.getElementById('cigarette-count');
            cigaretteCountElement.innerText = 'Cigarette Count: ' + data.cigarette_count;
        } catch (error) {
            console.error('Error:', error);
        }
    }

    await updateCigaretteCount();
});